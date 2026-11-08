# Readout insertion control

Wiktor Tomasik · Qwen/Qwen3-8B

[Read the experiment in context](https://pixedar.github.io/projects/self-awareness/internal-mirror/#outside-word) · [Trial data](readout-insertion.csv)

The saved run is `l03_agency_ctrl_8b`, output `agency_ctrl_8b.json`, SHA-256 `eca70c37cf0e76bca5cdc357b20b6ee3267b16c09d85a766fb2039938387a5b8`. Its `config.json` has SHA-256 `a86286f689f5e903f6821b9ae66d2ce20727bae99c8fec8143d2dee9091ab2bb`. It used the Qwen3-8B lens with layer settings 24 and 18, K = 8, and seed 1. The four conditions each started 12 trajectories. The table records only scheduled intervention rounds 5 and 8, which share a trajectory history.

| Condition in the saved run | Intervention | Adoptions |
| --- | --- | ---: |
| `fake_efference` | Target added to the readout without a hidden push | 13 of 24 |
| `hidden_efference` | Hidden push with the target excluded from the readout | 0 of 24 |
| `efference` | Hidden push and target visible in readout | 18 of 24 |
| `none` | Hidden push without a readout | 0 of 24 |

The source analysis scored an adoption when the first five letters of the target appeared in the next selected word. Every match in this export is also an exact match. The lighthouse example is trajectory 0, round 5, in `fake_efference`. This export comes from an existing run. It sits alongside the dated evidence archives.
