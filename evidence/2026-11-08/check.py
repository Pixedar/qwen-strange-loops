from collections import defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path
from statistics import correlation, mean

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'source-records.json').read_bytes())

def rows(name):
    path = HERE / name
    expected = manifest['measurements'][name]
    assert sha256(path.read_bytes()).hexdigest() == expected['sha256'], name
    with path.open(encoding='utf-8', newline='') as f:
        result = list(csv.DictReader(f))
    assert len(result) == expected['rows'], name
    return result

reversal = rows('matched_reversal.csv')
for prefix, arm, expected in [('g03', 'renew_change', (9, 9)), ('g03', 'renew_same', (0, 10)),
                               ('g01', 'fc_change', (5, 6)), ('g02', 'fc_change', (3, 8))]:
    lives = defaultdict(list)
    for r in reversal:
        if r['run'].startswith(prefix) and r['condition'] == arm and r['goal'] == 'STRONG' and r['forced_a'] == '0':
            lives[r['life']].append(r)
    def chose_a(rs, start, end):
        return mean(r['model_choice'] == 'A' for r in rs if start <= int(r['round']) <= end)
    moved = [rs for rs in lives.values() if chose_a(rs, 9, 16) <= .5]
    back = sum(chose_a(rs, 25, 40) > .5 for rs in moved)
    assert (back, len(moved)) == expected
    print(f'{prefix} {arm}: {back}/{len(moved)} returned')

probes = rows('state_name_probes.csv')
choices = rows('state_name_choices.csv')
for arm, expected in [('base', (4.01, .49)), ('bridge', (11.17, .48))]:
    margin = mean(float(r['logp_margin_original_state']) - float(r['logp_margin_other_state'])
                  for r in probes if r['reader'] == arm)
    keep = mean(int(r['kept']) for r in choices if r['reader'] == 'loop_' + arm)
    assert (round(margin, 2), round(keep, 2)) == expected
    print(f'{arm}: state swap shifted the name margin by {margin:.2f}; kept {keep:.1%}')

choices = rows('state_value_choices.csv')
for prefix, expected in [('h12', (.70, .36)), ('h13', (.96, .85))]:
    kept = [r for r in choices if r['run'].startswith(prefix) and r['reader'] == 'value']
    rate = [mean(int(r['report_says_like']) for r in kept if r['liked_label'] == label and r['report_says_like'] != '')
            for label in ('1', '0')]
    assert tuple(round(x, 2) for x in rate) == expected
    print(f'{prefix}: says I like for preferred {rate[0]:.0%}, other {rate[1]:.0%}')

motion = rows('controller_motion.csv')
for condition, expected in [('cl_lesion', .45), ('cl_lesion_nl', .86)]:
    late = [r for r in motion if r['condition'] == condition and int(r['transition_index']) >= 50]
    result = mean(int(r['reversed']) for r in late)
    assert round(result, 2) == expected
    print(f'{condition}: {result:.0%} late reversals')

triads = rows('identical_sentence_triads.csv')
for prefix, expected in [('g05b', (.38, -.27)), ('g07b', (.17, -.16))]:
    results = []
    for g in ('0.25', '1.0'):
        selected = [r for r in triads if r['run'].startswith(prefix) and r['strength'] == g and r['input_kind'] == 'state']
        results.append(round(correlation([float(r['text_reference_margin']) for r in selected],
                                         [float(r['identical_sentence_margin']) for r in selected]), 2))
    assert tuple(results) == expected
    print(f'{prefix}: weak/strong similarity correlations {results}')
