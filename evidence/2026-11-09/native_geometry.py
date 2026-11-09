"""Compare compact native J-space and matched projections on the same saved states."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import numpy as np
from safetensors import safe_open
import torch
from transformers import AutoTokenizer
from wordfreq import zipf_frequency

from paired_readers import load, run

QWEN8 = 'b968826d9c46dd6066d109eabc6255188de91218'
WIDTH = 128
BASIS_SEED = 8463


def load_inputs(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ck = torch.load(args.assets / 'Qwen3-8B_jacobian_lens.pt', weights_only=True, map_location='cpu', mmap=True)
    transform = ck['J'][24].float().to(device)
    assert transform.shape == (4096,4096)
    norm = torch.frombuffer(bytearray((args.assets/'norm.bf16').read_bytes()), dtype=torch.bfloat16).float().to(device)
    tok = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)
    with safe_open(args.checkpoint/'model-00005-of-00005.safetensors',framework='pt',device='cpu') as shard:
        head = shard.get_tensor('lm_head.weight')
        n = min(head.shape[0], len(tok))
        words = tok.convert_ids_to_tokens(list(range(n)))
        initial = [i for i, token in enumerate(words) if token and re.fullmatch(r'Ġ[A-Za-z]{3,}', token)]
        sizes = torch.cat([head[chunk].float().norm(dim=1) for chunk in np.array_split(initial, 20)])
        cutoff = float(torch.quantile(sizes, .02))
        indices = [i for i, size in zip(initial, sizes) if float(size) >= cutoff and
                   re.fullmatch(r'[a-z]+', words[i][1:]) and zipf_frequency(words[i][1:], 'en') >= 3.]
        center = sum(block.float().sum(0) for block in head[:n].split(4096)) / n
        chunks = [(head[ids].float().to(device) - center.to(device)) * norm
                  for ids in np.array_split(indices, 20)]
    return device, transform, chunks, len(indices)


def basis(rows):
    torch.manual_seed(BASIS_SEED)
    return torch.pca_lowrank(rows, q=WIDTH + 16, center=False, niter=2)[2][:,:WIDTH].cpu().numpy()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--runs', type=Path, required=True)
    p.add_argument('--assets', type=Path, required=True)
    p.add_argument('--checkpoint', type=Path, required=True)
    args = p.parse_args()
    assert args.checkpoint.name == QWEN8
    torch.set_num_threads(6)
    torch.set_float32_matmul_precision('highest')
    with torch.inference_mode():
        device, transform, rows, vocab_size = load_inputs(args)
        jlens = basis(torch.cat([torch.nn.functional.normalize(r @ transform, dim=1) for r in rows]))
        plain = basis(torch.cat([torch.nn.functional.normalize(r, dim=1) for r in rows]))
        random = np.linalg.qr(np.random.default_rng(BASIS_SEED).standard_normal((4096, WIDTH)))[0].astype('float32')
    print(f'{vocab_size} lower-case vocabulary atoms, {WIDTH} projection coordinates',flush=True)
    results = {}
    datasets = {(key, split): load(args.runs, key, split)
                for key in ('e29','e30') for split in ('train','lives')}
    for data in datasets.values():
        raw = data['states']['raw_24']
        for name, projection in [('jspace128',jlens),('plain_unembedding128',plain),('random128',random)]:
            data['states'][name] = raw @ projection
        data['states']['jspace_residual'] = raw - data['states']['jspace128'] @ jlens.T
    for source, target in [('e29','e30'),('e30','e29')]:
        name = f'{source}_train_to_{target}_lives'
        result = run(datasets[source,'train'], datasets[target,'lives'], False)
        results[name] = result
        for key in ['jspace128','plain_unembedding128','random128','jspace_residual','raw_24','time_order']:
            stats = result['test'][key]['all']
            print(name, key, round(stats['accuracy'],4),[round(i,4) for i in stats['ci95']], flush=True)
    payload = {'assets':json.loads((args.assets/'assets.json').read_bytes()),
               'head_sha256': hashlib.sha256((args.checkpoint/'model-00005-of-00005.safetensors').read_bytes()).hexdigest(),
               'width': WIDTH, 'basis_seed': BASIS_SEED, 'layer': 24, 'vocab_atoms': vocab_size,
               'sources':{f'{run_name}.{split}':v['hashes'] for (run_name,split),v in datasets.items()},
               'results':results}
    (args.assets.parent/'native_geometry_results.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
