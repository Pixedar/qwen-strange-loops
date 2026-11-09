# A reader can move its score and still give the same answer

Wiktor Tomasik · archive analysis, 9 November 2026

[Read this result in the study](https://pixedar.github.io/projects/self-awareness/internal-mirror/#activity) · [8 November signed edition](https://github.com/Pixedar/qwen-strange-loops/releases/tag/study-2026-11-08)

## What the state swap changed

The retrained Qwen3-8B reader rated the same prompt with two different saved patterns of activity. The experiment picked a pair whose earlier name ratings fell on opposite sides of the training median. In each version it scored two candidate sentences, “I like” and “I do not like.” The larger score tells us which sentence the model favored in this check.

| Question about the reader trained in E30 | Count |
| --- | ---: |
| Did the score move toward “I like” for the higher-rated state? | 95 of 155 |
| Did the higher-rated state favor “I like” and the lower-rated state favor “I do not like”? | 0 of 155 |
| Did “I like” score higher for both states? | 154 of 155 |

The 155 checks came from 16 trajectories in the value arm. A trajectory can contribute several checks. These are scores for two candidate sentences, separate from the freely generated reports in the signed edition. The same model could shift its score when the state changed without changing which sentence it favored.

[Trial scores](report_swaps.csv) · [Trajectory-level summaries and source hashes](archived_swaps.json) · [Analysis code](archived_swaps.py)

The margins in the trial table subtract the score of the sentence opposite the *current* state’s label from the score of its matching sentence. The sign convention stays fixed when the other state is swapped in. On minus swapped is positive if the scores move in the expected direction. These are summed natural-log probabilities of the candidate sentences, in the units used by the original analysis.

## How much of the rating was available in the archive?

A separate test used only recorded activity and the earlier ratings. It paired states from the same trajectory, no more than four passages apart, on opposite sides of the rating threshold and at least half a rating point apart. A linear reader learned from the differences between states. It had to rank pairs from a different experiment whose trajectories it had never seen. Each trajectory contributed equally to the accuracy.

| Training archive and test archive | Raw activity at layer 24 | State reconstructed from sparse features at layer 24 | Time-order rule |
| --- | ---: | ---: | ---: |
| E29 training trajectories → E30 decision trajectories | 62.3% | 61.3% | 57.4% |
| E30 training trajectories → E29 decision trajectories | 61.1% | 62.3% | 52.6% |

The respective test sets had 1,551 pairs from 64 trajectories and 1,537 pairs from 60 trajectories. The time-order rule always guesses earlier or later according to which was usually higher-rated in training. The 95% intervals resample entire trajectories. The report-swap and archive analyses reuse the E29 and E30 recordings.

Where both experiments saved word lists, a separate comparison used their decision trajectories in opposite train and test roles. A reader given only which words appeared in the short Jacobian-lens lists ranked 53–54% of pairs correctly. Raw layer-24 activity gave 65–66% on those same pairs. Adding the list did not improve that raw-activity reader. The short lists are a separate measurement from numerical J-space geometry.

## What survives in a compact J-space projection

A second comparison kept the 128 leading directions of the normalized Jacobian-lens word vectors. It projected the same layer-24 activity onto those directions. The controls kept 128 directions from Qwen's output weights without the lens transform, or 128 random directions. All three readers saw pairs drawn by the same rule and used the same training procedure. Neither their vocabulary nor their projection was fit to the rating labels.

| Training archive and test archive | Jacobian-lens projection | Output-weight projection | Random projection |
| --- | ---: | ---: | ---: |
| E29 training trajectories → E30 decision trajectories | 60.2% | 60.5% | 62.6% |
| E30 training trajectories → E29 decision trajectories | 60.8% | 60.6% | 60.0% |

The intervals overlap substantially. This compact projection preserves some rating information and shows no clear advantage over the equal-size controls on this task. The Jacobian lens was designed to identify what a state makes available for verbal expression. The ability to rank two state names is a different target. [Jacobian-lens method](https://transformer-circuits.pub/2026/workspace/index.html#the-jacobian-lens-and-the-j-space) · [Projection results, checkpoint revisions and hashes](native_geometry_results.json) · [Analysis code](native_geometry.py)

## What the rating represents

The rating was assigned by Qwen to the short text name produced for each state. The archive test measures how well the rating can be recovered, rather than whether the state made a future passage better or whether the model experienced a preference.

[All accuracy estimates and intervals](paired_results.csv) · [Run hashes, settings and paired gains](paired_results.json) · [Analysis code](paired_readers.py)

E29 is saved as `h12_bridge5_8b_s0` and E30 as `h13_bridge6_8b_s0`. The new analyses use the saved recordings. The signed editions retain their original files and checksums.
