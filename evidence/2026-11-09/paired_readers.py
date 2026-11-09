"""Paired value decoding from archived E29/E30 measurements. No model execution."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

RUNS = {
    'e29': ('h12_bridge5_8b_s0', 'bridge5_8b_s0'),
    'e30': ('h13_bridge6_8b_s0', 'bridge6_8b_s0'),
}
MAX_GAP = 4
MIN_RATING_GAP = 0.5
CONTROL_SEED = 1819


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(root, name, split):
    folder, tag = RUNS[name]
    source = root / folder
    p = source / f'{tag}_{split}.npz'
    j = source / f'{tag}.json'
    data = json.loads(j.read_bytes())
    with np.load(p, allow_pickle=False) as archive:
        vals = archive['vals']
        unit = archive['units']
        states = {
            'dictionary_24': unit[:, :, data['layers'].index(24)].reshape(vals.size, -1).astype('float32'),
            'raw_24': archive['hp'].reshape(vals.size, -1).astype('float32'),
        }
        rows = None
        arms = ['train'] * len(vals)
        if split == 'lives':
            rows = [row for life in data['lives'] for row in life['rounds']]
            arms = list(archive['arms'])
            assert len(rows) == vals.size
            assert np.allclose([row['val'] for row in rows], vals.flatten(), atol=.00051, rtol=0)
        else:
            assert np.allclose([r['vals'] for r in data['train']], vals, atol=.00051, rtol=0)
    return {'vals': vals, 'arms': arms, 'states': states, 'rows': rows,
            'med': data['median_rating'], 'hashes': {p.name: digest(p), j.name: digest(j)}}


def pairs(data):
    vals = data['vals']
    med = data['med']
    left, right, signed, life = [], [], [], []
    for i, row in enumerate(vals):
        for j, a in enumerate(row):
            for k in range(j + 1, min(len(row), j + MAX_GAP + 1)):
                b = row[k]
                if (a >= med) == (b >= med) or abs(a - b) < MIN_RATING_GAP:
                    continue
                left.append(i * len(row) + j)
                right.append(i * len(row) + k)
                signed.append(1 if a > b else -1)
                life.append(i)
    return tuple(np.array(x) for x in (left, right, signed, life))


def normalize(train, test, left, right):
    delta = train[left] - train[right]
    squared = delta.multiply(delta).sum(axis=1) if hasattr(delta, 'multiply') else (delta**2).sum(axis=1)
    scale = np.sqrt(np.mean(squared))
    assert scale > 0
    return train / scale, test / scale


def state_features(train, test, a, b):
    tr, te = {}, {}
    for name in train['states']:
        tr[name], te[name] = normalize(train['states'][name], test['states'][name], a, b)
    tr['raw_and_dictionary'] = np.column_stack((tr['raw_24'], tr['dictionary_24'])) / np.sqrt(2)
    te['raw_and_dictionary'] = np.column_stack((te['raw_24'], te['dictionary_24'])) / np.sqrt(2)
    return tr, te


def text_features(train, test, tr, te, a, b):
    for kind in ('lens_words', 'passage_words'):
        def sentences(rows):
            if kind == 'lens_words':
                return [' '.join(r['jw_pass']) for r in rows]
            return [r['text'] for r in rows]
        enc = CountVectorizer(min_df=3, binary=True, max_features=6000, token_pattern=r"(?u)\b[a-zA-Z]{3,}\b")
        x = enc.fit_transform(sentences(train['rows'])).astype('float32')
        y = enc.transform(sentences(test['rows'])).astype('float32')
        tr[kind], te[kind] = normalize(x, y, a, b)
    from scipy.sparse import hstack
    for name in ('raw_and_lens', 'text_and_lens'):
        first = tr['raw_24'] if name == 'raw_and_lens' else tr['passage_words']
        second = te['raw_24'] if name == 'raw_and_lens' else te['passage_words']
        tr[name] = hstack((csr_matrix(first), tr['lens_words']), format='csr') / np.sqrt(2)
        te[name] = hstack((csr_matrix(second), te['lens_words']), format='csr') / np.sqrt(2)


def statistics(margin, life):
    points = np.where(margin > 0, 1., np.where(margin < 0, 0., .5))
    per_life = np.array([points[life == i].mean() for i in np.unique(life)])
    rng = np.random.default_rng(CONTROL_SEED)
    samples = rng.choice(per_life, (4000, len(per_life)), replace=True).mean(axis=1)
    return {'accuracy': float(per_life.mean()), 'ci95': np.quantile(samples, (.025, .975)).tolist(),
            'lives': len(per_life), 'pairs': len(points)}


def run(train, test, use_text):
    a, b, sign, train_life = pairs(train)
    c, d, target, test_life = pairs(test)
    tr, te = state_features(train, test, a, b)
    if use_text:
        text_features(train, test, tr, te, a, b)
    chronological = np.sign(np.mean([sign[train_life == i].mean() for i in np.unique(train_life)]))
    groups = np.asarray(test['arms'])[test_life]
    metrics = {}
    outputs = {}
    for name, x in tr.items():
        delta = x[a] - x[b]
        # With no intercept, (delta,y) and (-delta,-y) produce identical gradients.
        # Weight lives equally so a trajectory with many viable pairs cannot dominate.
        life_weights = np.bincount(train_life)[train_life]
        weight = 1 / life_weights
        weight /= weight.mean()
        classifier = LogisticRegression(fit_intercept=False, C=1.0, solver='liblinear')
        classifier.fit(delta, sign, sample_weight=weight)
        delta_test = te[name][c] - te[name][d]
        margin = classifier.decision_function(delta_test) * target
        assert np.allclose(classifier.decision_function(-delta_test) * target, -margin)
        outputs[name] = margin
    outputs['no_state_tie'] = np.zeros(len(target))
    outputs['time_order'] = chronological * target
    for name in ('raw_24', 'dictionary_24'):
        generator = np.random.default_rng(CONTROL_SEED)
        order = np.arange(test['vals'].size).reshape(test['vals'].shape)
        for indices in order:
            generator.shuffle(indices)
        x = tr[name]
        clf = LogisticRegression(fit_intercept=False, C=1.0, solver='liblinear')
        clf.fit(x[a] - x[b], sign, sample_weight=weight)
        permuted = te[name][order.flatten()]
        outputs[name + '_within_life_shuffle'] = clf.decision_function(permuted[c] - permuted[d]) * target
    for name, margin in outputs.items():
        metrics[name] = {'all': statistics(margin, test_life)}
        for arm in sorted(set(groups)):
            keep = groups == arm
            metrics[name][arm] = statistics(margin[keep], test_life[keep])
    improvements = {}
    for name in tr:
        differences = []
        for i in np.unique(test_life):
            select = test_life == i
            correct = lambda score: (1 + np.sign(score[select])) / 2
            differences.append(np.mean(correct(outputs[name]) - correct(outputs['time_order'])))
        rng = np.random.default_rng(CONTROL_SEED)
        scores = rng.choice(differences, (4000, len(differences)), replace=True).mean(axis=1)
        improvements[name] = {'gain': float(np.mean(differences)), 'ci95': np.quantile(scores, (.025, .975)).tolist()}
    return {'training_pairs': len(sign), 'training_lives': len(np.unique(train_life)),
            'test': metrics, 'paired_gain_over_time_order': improvements}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    datasets = {(run_name, split): load(args.runs, run_name, split)
                for run_name in RUNS for split in ('train', 'lives')}
    comparisons = [
        ('e29_train_to_e30_lives', ('e29', 'train'), ('e30', 'lives'), False),
        ('e30_train_to_e29_lives', ('e30', 'train'), ('e29', 'lives'), False),
        ('e29_lives_to_e30_lives', ('e29', 'lives'), ('e30', 'lives'), True),
        ('e30_lives_to_e29_lives', ('e30', 'lives'), ('e29', 'lives'), True),
    ]
    results = {}
    for key, source, target, use_text in comparisons:
        results[key] = run(datasets[source], datasets[target], use_text)
        print(key, flush=True)
        for name, metrics in results[key]['test'].items():
            summary = ', '.join(f"{arm} {group['accuracy']:.3f} ({group['lives']} lives, {group['pairs']} pairs)"
                                for arm, group in metrics.items() if arm in ('all','none'))
            print(f'  {name:26s} {summary}', flush=True)
    payload = {'method': {'max_round_gap': MAX_GAP, 'min_rating_gap': MIN_RATING_GAP,
                          'threshold': 'Original training median of each run',
                          'interval': '95% percentile bootstrap over whole test lives'},
               'sources': {f'{run}.{split}': data['hashes'] for (run, split), data in datasets.items()},
               'results': results}
    args.out.mkdir(exist_ok=True, parents=True)
    (args.out / 'paired_results.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    with (args.out / 'paired_results.csv').open('w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(['comparison','reader','arm','accuracy','ci_low','ci_high','lives','pairs'])
        for name, result in results.items():
            for reader, metrics in result['test'].items():
                for arm, group in metrics.items():
                    writer.writerow([name, reader, arm, group['accuracy'], *group['ci95'], group['lives'], group['pairs']])


if __name__ == '__main__':
    main()
