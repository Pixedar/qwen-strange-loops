"""Reaggregate the original fixed-prompt report swaps by whole trajectory."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

def summarize(rows):
    names = ['rank_correct', 'both_label_signs_correct', 'both_say_like', 'both_say_dislike', 'on_correct', 'swapped_correct']
    arrays = np.array(rows,dtype=float)
    rng = np.random.default_rng(337)
    mean = arrays.mean(0)
    bootstrap = arrays[rng.integers(0, len(arrays), size=(4000,len(arrays)))].mean(1)
    interval = np.quantile(bootstrap,[.025,.975],axis=0)
    return {key:{'fraction':float(mean[i]),'ci95':[float(x) for x in interval[:,i]]} for i,key in enumerate(names)}

def analyze(file):
    raw = file.read_bytes()
    data = json.loads(raw)
    arms = {}
    for life in data['lives']:
        pairs = []
        for row in life['rounds']:
            if 'read' not in row or not isinstance(row['read'],dict) or 'swap' not in row['read']:
                continue
            on = row['read']['on']
            sw = row['read']['swap']
            signed_label = 2*row['label']-1
            pairs.append((on>sw, on>0 and sw<0, on*signed_label>0 and sw*signed_label>0,
                          on*signed_label<0 and sw*signed_label<0, on>0, sw<0))
        if pairs:
            arms.setdefault(life['arm'],[]).append(pairs)
    return {'sha256':hashlib.sha256(raw).hexdigest(),'arms':{
        arm:{'lives':len(lives),'pairs':sum(len(x) for x in lives),
             'outcomes':summarize([np.mean(x,axis=0) for x in lives])}
        for arm,lives in arms.items()}}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--runs',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    data={}
    for key, relative in [('e29','h12_bridge5_8b_s0/bridge5_8b_s0.json'),('e30','h13_bridge6_8b_s0/bridge6_8b_s0.json')]:
        data[key]=analyze(args.runs/relative)
        print(key,flush=True)
        for arm,stats in data[key]['arms'].items():
            print(arm,stats['lives'],stats['pairs'],{k:round(v['fraction'],3) for k,v in stats['outcomes'].items()},flush=True)
    args.out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
if __name__ == '__main__':
    main()
