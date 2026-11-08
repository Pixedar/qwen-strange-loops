# Two ways to feed a measurement back into a model

Wiktor Tomasik · external-reader snapshot 3 November 2026 · Qwen feedback results through 8 November 2026

An attached reader predicts what its next selection will emphasize and feeds that forecast directly into its next attention weights. In **Strange Loops in Qwen**, Qwen can read words decoded from its activity and choose an intervention. Both routes can change what happens next. The difference is where the information enters the calculation.

[Read the comparison in the full study](https://pixedar.github.io/projects/self-awareness/internal-mirror/#compare) · [External reader architecture](https://pixedar.github.io/projects/self-awareness/attention-reader/study/index.html#architecture)

| | External attention reader | Strange Loops in Qwen |
|---|---|---|
| What is measured | Recent Qwen activations and what the attached reader selected | Qwen activity while writing, translated into short lists of candidate words |
| Who interprets it | A learned controller predicts what its own next selection will emphasize | Qwen interprets the list and can describe what the measurements show |
| How it acts | The prediction helps set the reader's next selection. In live mode, a writer feeds selected native content back into Qwen. | A readout or conclusion enters Qwen's context. Tool choices can add activation biases or concept-to-concept rules. |
| What stood out | Different selection habits survived even when the compact pictures were mostly alike. | Calling a readout “your own workspace” changed whether its words entered the next passage. When forecasts and choices disagreed, displaying the forecast or conclusion could change the choice. |

## A way of looking can persist without a distinctive picture

In the external-reader recordings, copies developed distinct selection habits. Much of the compact picture, however, followed the category of the text they were all reading. In one displayed start, copy identity accounted for 95% of variation on the displayed stance axis, while text category accounted for 92% of the picture axis. These are descriptive axes fitted for that start. The broader control result is that a coarse or fixed picture can preserve substantial selection organization, while weakening responses to changes in the text. It separates *what gets picked out* from *the picture formed from it*. [External reader study](https://pixedar.github.io/projects/self-awareness/attention-reader/study/index.html#self-models)

In live tests, restoring a specific evidence-related direction inside Qwen removed part of the difference between two controllers' answer preferences. This shows a route by which selection changes how strongly Qwen favors an answer. The effects were usually shifts in preference strength. The swap controls leave ownership of the forecast open as an explanation. [Meaning chapter](https://pixedar.github.io/projects/self-awareness/attention-reader/study/index.html#meaning)

## Where the two routes meet

In the Qwen study, a trained reader distinguished active patterns with the text held fixed, yet its report scarcely changed which pattern the model kept. In a different task, a sentence saying “I like” strongly steered a choice, even though a fresh reader gave nearly the same report about high- and low-rated states. The study follows this distinction from the [surprising “strangers” case](https://pixedar.github.io/projects/self-awareness/internal-mirror/#strangers) to the [choice reversals](https://pixedar.github.io/projects/self-awareness/internal-mirror/#choice) and [fixed-text controls](https://pixedar.github.io/projects/self-awareness/internal-mirror/#activity).

A hybrid experiment learned a direct route like the one used by the external reader. After the controller’s map was scrambled, letting it relearn reduced late reversals in the measured direction of activity from 86% to 45%. With the accurate map intact, 41% reversed. Qwen’s own description rarely named the next measured direction. The controller’s measured recovery and the verbal account were separate outcomes. [Controller setup and results](https://pixedar.github.io/projects/self-awareness/internal-mirror/#compare)
