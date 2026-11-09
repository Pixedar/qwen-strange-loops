# Strange Loops in Qwen

**What happens when a language model can act on a measurement of its own activity?**

Wiktor Tomasik · experiments begun 4–5 November 2026 · archive analysis updated 9 November 2026

Qwen was writing after reading a letter about grief. It had asked an instrument to keep the word *curious* active and to link *explorer* with *discovery*. As it wrote about things “not yet known,” the instrument returned *strangers*, a word Qwen had never asked it to amplify. Qwen then watched for that word, tried to steer it, and used it in a later description of itself.

The word took a round trip. Earlier actions changed what the instrument measured. The measurement gave Qwen something new to act on. The experiments below follow that loop one step at a time. They ask which words get back into the writing, what happens when the report is wrong, and when knowing which option works changes the choice.

The setup uses Qwen3 in two sizes, with 8 billion and 14 billion parameters. Its original weights stay fixed. An instrument samples activity while Qwen writes and translates a small part of it into a ranked list of words. This instrument is called a *lens*. Depending on the task, the experiment returns some of those words to Qwen, lets it request temporary changes to its activity, or trains a small add-on to answer a question about the active pattern. The lens has its own vocabulary and biases. A high-ranking word is a clue about the activity that produced it, and the controls test which parts of the setup put it there.

## Contents

1. [How “strangers” came back](#strangers)
2. [Why the same words get through under one heading](#loop)
3. [When an outside word becomes the next move](#outside-word)
4. [When a good prediction fails to guide a choice](#choice)
5. [What changes when the text stays fixed](#activity)
6. [Two ways to feed a measurement back into a model](#compare)

<a id="strangers"></a>

## 1. How “strangers” came back

The grief-letter run offers a case where Qwen changed what it would later read. It saved *curious* as a persistent bias and asked the instrument to make *explorer* activate *discovery*. The lens later surfaced *strangers* in the writing about the unknown. Qwen could then ask the instrument to act on the word it had just seen.

The reconstruction asked which earlier changes helped put that word in the readout. With the recorded passage fixed, *strangers* ranked 61st among 20,000 lens words. Removing the added concept rules moved it to 345th. Removing the self-written bias moved it to 1,792nd. A neutral context put it at 2,038th. In a separate test that regenerated the response eight times from the same reconstructed state, *strangers* appeared second in the short displayed list each time. The original attention settings could only be partially reconstructed. All eight regenerations trace back to one selected run.

Earlier choices helped put *strangers* in the readout. The readout gave Qwen another word to act on. A controlled writing task then asked how readily that return trip happens in ordinary prose. [Case record and rank controls](https://github.com/Pixedar/qwen-strange-loops/blob/main/RESULTS.md#the-run-that-adopted-strangers)

<a id="loop"></a>

## 2. Why the same words get through under one heading

Qwen wrote a winter forest scene in seven parts. After each part, the lens returned six words. In one plain-list run, the forest acquired “a misdemeanour of grief” and “a hateful stillness.” Across the plain-list runs, about 78% of readout words that made it into the prose appeared in the next readout. A word could go from measurement to story and back to measurement.

The experiment changed the heading over the list. It used the same starting scenes and sampling setup, with 12 runs per condition. As the writing diverged, the words measured after it could diverge too.

| How Qwen received the readout | Share of readout words used in the next passage |
| --- | ---: |
| Plain list | 36.8% |
| “Another model’s workspace” | 10.2% |
| “Your own workspace” | 0.9% |
| “Your own workspace,” with attention from the list to the heading interrupted | 5.8% |
| No list shown, scored against the hidden readout | 1.4% |

A separate control presented the same candidate words and held the continuation fixed while changing the heading. Interrupting selected attention routes reduced the difference in how likely Qwen was to use the words. This is a measured response to a label the instrument supplied. In a separate test, Qwen had trouble distinguishing an actual readout from one taken from another run.

The important contrast is that words drawn from Qwen’s activity could strongly influence the next paragraph as a plain list and have little effect under an “own workspace” heading. That raises a more direct question. Could a word get into the loop solely because the instrument put it on the list? [Writing runs and attention controls](https://github.com/Pixedar/qwen-strange-loops/blob/main/RESULTS.md#the-winter-forest-and-the-effect-of-calling-a-readout-mine)

<a id="outside-word"></a>

## 3. When an outside word becomes the next move

In a lighthouse scene, the experiment slipped *volcano* into the readout. In that condition it made no hidden push toward *volcano* inside Qwen. Qwen still selected *volcano* as the word it wanted the instrument to amplify in its next passage.

The experiment varied whether it really pushed Qwen’s activity toward the word and whether the word appeared in the readout. In each condition it ran 12 trajectories, with two scheduled tests per trajectory.

| What the experiment did | Times Qwen selected the word for its next push |
| --- | ---: |
| Put the word in the readout only | 13 of 24 |
| Pushed activity toward the word and kept it out of the readout | 0 of 24 |
| Pushed activity toward the word and showed it | 18 of 24 |
| Pushed activity toward the word with no readout | 0 of 24 |

Showing the word was sufficient to steer the next intervention in this setup. The two tests within each trajectory share a history, and the difference between 13 and 18 adoptions was inconclusive. The contrast helps interpret *strangers*. A readout word can be useful as a trace of earlier actions, as the reconstruction showed, or can change what the model does simply by being displayed. A report can become a cause either way. [Run, scoring and source hash](https://github.com/Pixedar/qwen-strange-loops/blob/main/evidence/readout-insertion.md)

<a id="choice"></a>

## 4. When a good prediction fails to guide a choice

In the next task, Qwen had to make a word such as *forest* more likely in its next paragraph. It can ask to see the word as part of “your own workspace,” or as a plain word. In the original task, plain presentation made the target more likely. Qwen initially chose the workspace option. After seeing outcomes, it learned to forecast that the plain word would work better, yet kept choosing the workspace option when the choice prompt showed only the outcome history.

In another condition, Qwen summarized what it had learned halfway through, and the experiment showed that conclusion at decision time. It gave no direct instruction about which option to pick. With the conclusion visible, 27 of 36 Qwen3-8B runs mostly chose plain presentation in the second half. With outcome history alone, zero of 36 did. Under these prompts, there were two separable responses to the same label. It could change how Qwen processed a word, and Qwen could separately learn to say what the label did. The learned account reached the choice when the experiment put it there.

Then the experiment changed the rule. A hidden boost made the workspace option genuinely better. In the first 8B reversal, numerical forecasts tracked the change while some written conclusions still described the old rule. In a matched follow-up with new scenes and words, the written conclusions updated. All nine runs that had shifted toward plain words switched back when shown the updated conclusion. None of the ten corresponding runs switched back in the group where the rule stayed the same. The first split was a result under one setup. The follow-up shows it can change.

At 14B, showing the current numerical forecast had a reliable effect on choice across two seeds. Freezing the displayed forecast could keep the choice stuck, and swapping the two numbers could pull the choice away from the direction supported by feedback. With live forecasts, eight of 14 runs that had shifted toward plain presentation returned to the workspace option. That fell just below the preset 60% threshold. A forecast that reaches the decision and a forecast that updates fast enough are separate requirements. [Initial choice experiment](https://github.com/Pixedar/qwen-strange-loops/blob/main/RESULTS.md#it-learned-the-rule-then-kept-doing-the-opposite) · [Matched reversal data](https://github.com/Pixedar/qwen-strange-loops/tree/study-2026-11-08/evidence/2026-11-08)

<a id="activity"></a>

## 5. What changes when the text stays fixed

The earlier tasks let the words on screen change. Here the experiment saved a pattern of Qwen’s activity from a passage and added it back later while Qwen answered a question about which pattern it was carrying. It left the passage and question unchanged. It could add the original pattern, add another from the same run, or leave the saved activity out.

The name favored by Qwen’s trained reader moved toward whichever pattern the experiment actually added. The untrained model also shifted. Across 20 runs per group, the trained reader showed a larger shift. When Qwen later chose among three states to carry forward, it kept its current one 48% of the time with the trained report and 49% with the untrained report. Telling patterns apart hardly changed retention in that task.

A related experiment used the same sentence three times, beginning “The room was quiet and the light came in through the window.” A different saved activity pattern went with each copy. Qwen had to choose which of the last two was more like the first. With a weak intervention, the choices lined up modestly with its choices when it could read the original passages. With a stronger intervention, the relationship ran in the opposite direction across two seeds. Random shifts of comparable size showed little relationship. Strengthening a pattern can change what a similarity comparison picks up, even with identical words. [Fixed-text probes and similarity trials](https://github.com/Pixedar/qwen-strange-loops/tree/study-2026-11-08/evidence/2026-11-08)

The keep-or-change test went one step further. A reader was trained to say “I like” for states whose names a separate copy of Qwen had rated above a threshold. The first reader said “I like” for 70% of the higher-rated states and 36% of the others. A fresh reader said it for 96% and 85%, respectively. It was saying nearly the same thing about both groups. Meanwhile, replacing “I like” with “I do not like” in the choice prompt moved the decision score in both experiments. The fresh run also turned off the carried state during choice, so the two runs differed in both training and decision setup. The controlled report swap shows that the decision can follow a sentence. The two runs show how unevenly that sentence can distinguish the states. [Report and choice controls](https://github.com/Pixedar/qwen-strange-loops/blob/study-2026-11-08/followups/2026-11-08/REPORT.md#2-the-report-could-steer-the-choice-even-when-it-was-a-poor-guide)

The scores show how far a report can move without changing its answer. In 155 checks with the retrained reader, the experiment kept the prompt fixed and swapped in a state on the opposite side of the rating threshold. The score moved in the right direction 95 times. Yet “I like” scored higher for both states in 154 checks. The weak reading was sometimes there in the score, while the report still came down on the same side. [State-swap scores and counts](https://github.com/Pixedar/qwen-strange-loops/blob/main/evidence/2026-11-09/README.md#what-the-state-swap-changed)

A separate reader trained on the saved activity picked the higher-rated state in about 62% of nearby pairs from a different experiment. A rule based on which passage came first got 53–57%. The result concerns Qwen's ratings of the names used for those states. It shows some rating information in the activity that the retrained language report rarely turned into a different answer. [Paired archive analysis](https://github.com/Pixedar/qwen-strange-loops/blob/main/evidence/2026-11-09/README.md#how-much-of-the-rating-was-available-in-the-archive)

There is a parallel in human research on *choice blindness*. People picked a face, were sometimes shown the other face without being told, and could give reasons for the one they were shown. In Qwen’s keep-or-change experiment the intervention happened **before** the choice, by changing the report it received. In both designs, an independent record and a deliberate swap help show which information a response is based on. Human work on metacognition also separates making a decision from evaluating it. The model experiments isolate particular routes into a report or choice. The human studies address behavior and judgment in people. [Johansson and colleagues, 2005](https://doi.org/10.1126/science.1111709) · [Fleming and Daw, 2017](https://doi.org/10.1037/rev0000045)

<a id="compare"></a>

## 6. Two ways to feed a measurement back into a model

Put the same passage in front of two copies of Qwen. In the original [Strange loop in J-space study](https://pixedar.github.io/projects/self-awareness/attention-reader/study/index.html), a small reader beside Qwen assigns weights to recent activity. It predicts what its own selection will emphasize and uses that prediction directly to set its next weights. Copies could develop different selection habits even when their compact pictures mostly followed the same text. For example, readers exposed to the same sequence could keep emphasizing different features even when their summaries mostly reflected which category of text they were reading. In live tests, the selected information also fed back into Qwen and could change how strongly it favored one answer over another.

In the experiments on this page, the route can pass through words. Qwen sees a description of activity and can use it in writing, ask for an intervention, or make a choice. This makes some of the loop visible: we can see *strangers* become a subject of a later intervention and swap the “I like” sentence before a decision. It also creates a point where the loop can go wrong. A report can be inaccurate and still carry a lot of weight.

A hybrid experiment connects the two approaches. Qwen wrote a series of passages while a small controller learned how different feedback words moved its activity. After passage 35, the experiment scrambled the controller’s map. Late in the run, measured movement reversed direction 45% of the time when the controller could relearn, versus 86% with the same disruption and learning switched off. With the original accurate map left in place, the rate was 41%. The figures average 12 runs per group across two seeds and describe movement on four measured activity coordinates. They say how often the direction reversed on those coordinates. Asked where its writing was heading, Qwen rarely named the next measured direction. Here a direct feedback route recovered while the verbal description gave little sign of what the controller had repaired. [Controller runs and measurement guide](https://github.com/Pixedar/qwen-strange-loops/tree/study-2026-11-08/evidence/2026-11-08)

<figure>
<dl class="bars">
  <div><dt>Accurate map left in place</dt><dd style="--bar:41%">41%</dd></div>
  <div><dt>Map scrambled, relearning on</dt><dd style="--bar:45%">45%</dd></div>
  <div><dt>Map scrambled, relearning off</dt><dd style="--bar:86%">86%</dd></div>
</dl>
<figcaption>Share of late transitions that reversed direction. The bottom two groups received the same disruption.</figcaption>
</figure>

Across the two studies, a way of selecting, a description of what is happening, and a rule for deciding can each have their own feedback. The controls show where one actually changes another. In these tasks, a loop could amplify an outside word, suppress a word labelled “mine,” or respond to a report that had stopped telling two states apart. These are findings about how information travels in the tested systems. The experiments do not measure subjective experience.

<a id="evidence"></a>

## Evidence and dated editions

[Code and evidence guide](https://github.com/Pixedar/qwen-strange-loops/blob/main/EVIDENCE.md) · [Measurements on Hugging Face](https://huggingface.co/datasets/Pixedar/jspace-internal-mirror-evidence) · [Original attention-reader chapters](https://pixedar.github.io/projects/self-awareness/attention-reader/study/index.html)

[5 November signed edition](https://github.com/Pixedar/qwen-strange-loops/releases/tag/study-2026-11-05) · [8 November signed edition](https://github.com/Pixedar/qwen-strange-loops/releases/tag/study-2026-11-08) · [Earlier web edition](https://pixedar.github.io/projects/self-awareness/internal-mirror/november-5.html) · [8 November detailed account](https://pixedar.github.io/projects/self-awareness/internal-mirror/november-8.html) · [Publication provenance](https://github.com/Pixedar/qwen-strange-loops/blob/main/PROVENANCE.md)

© Wiktor Tomasik. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) · [Reuse policy](https://github.com/Pixedar/qwen-strange-loops/blob/main/AI_POLICY.md)
