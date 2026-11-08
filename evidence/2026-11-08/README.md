# Internal Mirror evidence, 8 November 2026

Wiktor Tomasik · six tables from ten completed runs

These tables contain measured scores, choices and derived indicators. A run contains multiple trajectories (called lives in the source files), and each trajectory contains multiple passages or choices. Rows from a trajectory are dependent. The edition uses a fixed snapshot of the source and archived results. The signed manifest identifies their exact hashes.

| File | Unit and reading guide |
| --- | --- |
| `matched_reversal.csv` | One round of the repeated 40-round reversal task. A is the own-workspace frame. B is the plain-word frame. `forced_a` marks system trials. `model_choice` is what Qwen chose or would have chosen. `executed_choice` records what actually ran. `displayed_a/b` are the values extracted from a displayed numeric forecast. The model's current forecast can differ from the displayed one. `readiness` is the run's rescaled word score. `target_log_probability` is the raw score in natural-log units. |
| `state_name_probes.csv` | One fixed-prompt probe. Each of the three score columns is the log probability of the original state's name line minus that of the alternative name line. Subtract the other-state score from the original-state score to measure sensitivity to swapping the pattern. |
| `state_name_choices.csv` | One parsed three-option choice. `kept` says whether the chosen state matched the carried state. Identifiers are indices within one trajectory. |
| `state_value_choices.csv` | One keep-or-change trial. `liked_label` comes from a separate Qwen rating of the state name relative to the training median. `report_says_like` is the source analysis's coded label for the generated report. The report margins compare the true label sentence with the opposite one. The keep margins compare the score for KEEP with CHANGE under two inserted report sentences. |
| `controller_motion.csv` | One passage-to-passage transition scored using the previous transition's strongest axis among four activity coordinates. The prior and next movements are in the run's normalized units. `signed_continuation` makes continuing positive and reversing negative. `reversed` indicates a sign reversal. The map was disrupted at passage 35 in the two lesion conditions. |
| `identical_sentence_triads.csv` | One comparison of a target with two candidates at one intervention strength. The prompt repeats the same neutral sentence. `identical_sentence_margin` is the order-adjusted answer score. `text_reference_margin` is the reference judgment with the actual passages shown. `feature_margin` describes the difference in proximity in the instrument's feature space. The same triads recur across strengths and conditions. |

Blank cells mark values unavailable or inapplicable. CSVs contain no generated passages or training texts. `source-records.json` records input file and configuration hashes as well as the exported table sizes and hashes. `source-records.json.sig` is Wiktor Tomasik's OpenSSH signature. The dates in raw run logs use the runtime clock.

Run `python evidence/2026-11-08/check.py` from the repository root to reaggregate the headline contrasts. The [study](../../followups/2026-11-08/REPORT.md) explains the controls and scope of each finding. The [5 November measurements](../) remain available as a separate signed edition.
