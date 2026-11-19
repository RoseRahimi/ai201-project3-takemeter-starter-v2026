# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts comments from r/nba, Reddit's main NBA discussion community,
by what kind of contribution they make. Every comment gets one of four labels:
`analysis` (a claim backed by checkable evidence), `hot_take` (an opinion
or prediction with no checkable evidence), `reaction` (the writer's own
feeling about something) or `meme_joke` (a post whose main purpose is to be
funny). r/nba is a good fit because every thread mixes all four: stat
breakdowns sit right next to one-line takes, injury-news grief and running
jokes.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** A comment that backs a basketball claim with at least one
concrete, checkable piece of evidence (a number or stat, a record, a date or
season, a named game, series or trade, a direct quote, or a specific described
play), or that states a checkable fact to correct or inform the discussion.
Not used when the stat is only the subject of a joke or an emotional outburst.

**Example 1:**
> I think if Harden wanted, he could have had a couple more big scoring
> seasons. He joined BKN, then Philly with Embiid averaging 30-35 and Maxey,
> then he goes to LA with Kawhi and PG, plus Russ and Powell for a sec. He was
> averaging 25/8 before he got traded to Cleveland last year age 36. I think if
> he stayed in HOU, he could have averaged his 30 a night for 3-4 more years.
> Obviously he had some injuries, I believe in BKN he played through a
> hamstring issue, maybe that slowed him down, gaining all that weight in
> Houston didn't help either.

**Example 2:**
> The Celtics had a better net rating with Brown off the court than on it in
> seven of his 10 seasons in Boston, including each of the last four.

### `hot_take`

**Definition:** Any opinion, judgement, prediction or speculation about
players, teams, owners or the league that offers no checkable evidence,
whether stated confidently or hedged with "I think", "imo" or "probably". This
includes general reasoning, definitions of terms, and examples given only as
player names with nothing checkable attached.

**Example 1:**
> He’s basically done, no one’s gonna take on a guy who can’t stay healthy

**Example 2:**
> Jaylen brown has never been a particularly impactful player. Years of
> advanced stats have said this

(Example 2 sounds like analysis, but "years of advanced stats" names no
number, so nothing in it can be checked.)

### `reaction`

**Definition:** A comment whose main point is the writer's own feeling
(shock, sadness, sympathy, excitement, anger, nostalgia, or frustration with
the thread or fans) rather than an argument, usually a short exclamation, even
if it mentions a stat or fact in passing. Not used when the comment is joking.

**Example 1:**
> I was rooting for him ngl. This sucks.

**Example 2:**
> brutal. this was likely his last shot

### `meme_joke`

**Definition:** A comment whose main purpose is to be funny rather than
literally true, such as a joke, pun, sarcasm, absurd exaggeration, wordplay, a
meme or a mock quote. A sarcastic or joking comment is `meme_joke` even when it
contains a stat, a fact or an opinion.

> These four definitions are word for word what `label_definitions.txt` holds.
> I tightened them after my first training run: `hot_take` originally meant
> only *confident* claims, which left hedged opinions ("I think he'll...") with
> no clear home, and `reaction` originally required a *recent* event.

**Example 1:**
> PG, Harden, Lavine, and myself. We're all trying to figure it out

**Example 2:**
> Bro coulda just said LeBron lol

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`. On r/nba, many hot takes
quote a number ("he's 0-4 in Game 7s"), so the presence of a fact is not
enough to call something analysis.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

The deletion test: mentally delete the fact. If the claim still stands just
as strongly, the fact was decoration and the post is a `hot_take`. It is
`analysis` only if there is a real "because" linking the evidence to the
conclusion. For the other boundaries I checked in a fixed order and took the
first match: (1) is the main point a joke or not meant literally? →
`meme_joke`; (2) is it mainly a feeling about a specific recent event? →
`reaction`; (3) does checkable evidence carry the argument? → `analysis`;
(4) otherwise → `hot_take`.


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Top-level comments and replies from eight
public r/nba threads, copied by hand from reddit.com in November 2026: James
Harden on accepting a smaller role, Victor Wembanyama's 52/24/8 game, "What is
considered a winning player?", Kristaps Porzingis stepping away, the Sixers
starting lineup's net rating, the Las Vegas expansion bid, Ben Simmons's
Achilles injury, and the NBA.com Rookie Ladder. I tried Reddit's API first,
but new API access now needs approval, so I pasted each thread page and used
`clean_thread.py` to strip usernames, flair, vote counts, buttons and ads and
split it into one row per comment. I removed 57 comments that couldn't be
understood without their parent comment or were off-topic.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->
I labelled the first 23 comments myself, cold, before asking an AI anything
about them (`note` = `cold`). I then asked Claude to review those 23; it
disagreed with several under my own rules, and I changed 8 of them (`note` =
`cold, revised after AI review`). The remaining 499 rows were pre-labelled by
Claude following the pattern of my 23. See the pre-labelling disclosure below.

**Counts per label:**

| Label | First run (unit 5) | Share | Final `labels.csv` | Share |
|---|---|---|---|---|
| `hot_take` | 230 | 44.1% | 100 | 24.0% |
| `reaction` | 111 | 21.3% | 111 | 26.7% |
| `analysis` | 105 | 20.2% | 105 | 25.2% |
| `meme_joke` | 75 | 14.4% | 100 | 24.0% |
| **Total** | 521 | 100% | 416 | 100% |

The first training run used the 521-row version. For the improvement (see
The Improvement below) I cut `hot_take` from 230 to 100 and added 25
`meme_joke` comments from three more threads (a travel-dunk thread, a
Bulls/Wolves thread and an Elvin Hayes thread), giving the 416 rows now in
`labels.csv`.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Jordan went to play baseball when his father died because it
> was his father's dream that he pursue baseball. I wouldn't call that
> quitting. Considering his experience with baseball and it being a skill
> sport, he was actually pretty good at it as well."
>
> *Could have been:* `hot_take` or `analysis`
>
> *I chose, because:* `analysis`. I first called it a hot take because it
> reads like an opinion, but under the deletion test the argument ("it wasn't
> quitting") depends entirely on the fact about his father. Take that away and
> there is no claim left.

**2.**
> *The post:* "one of the actual most impressive things in nba history is how
> harden transitioned instantly from two of the best scoring seasons of all
> time to playing the traditional point guard role at a truly elite level. if
> he had focused on playing the way he did on the nets for his whole career,
> he would've been a top 5 point guard of all time."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. It sounds analytical, but nothing in it is
> checkable: "two of the best scoring seasons" and "truly elite" are
> assertions, not evidence. This is the reverse of case 1.

**3.**
> *The post:* "Hamstring injury certainly slowed him down. It was the first
> step down (lost explosiveness, etc.). Before that while on the Nets, he was
> playing quite possibly the best of anyone in the league. All around
> spectacular. Absolute shame. He has title without that. Highest TS ever in
> the playoffs for anyone averaging 25 ppg (along with a near triple double).
> Then reinjured again start of the next series. Pre injury Nets Harden was
> awesome."
>
> *Could have been:* `reaction` or `analysis`
>
> *I chose, because:* `analysis`. "Absolute shame" made me call it a reaction
> at first, but the main point isn't the writer's feeling, it's an argument
> ("he has a title without that injury"). The TS% record isn't a passing
> mention; it's the evidence the argument stands on, so emotional wording
> doesn't override it.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** <!-- epochs, learning rate, batch size, seed -->
3 epochs, learning rate 2e-5, batch size 16, seed 42, max length 128 tokens.
Trained on Apple Silicon (`mps`), torch 2.15.0.

**Anything I changed from the defaults, and why:** Nothing. I kept the
notebook defaults so this first run is a clean starting point. The one change
I made to the notebook was adding `meme_joke` to `LABELS`.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
70/15/15 stratified: train 364, val 78, test 79. Test split per label:
`hot_take` 35, `reaction` 17, `analysis` 16, `meme_joke` 11. Every label has
at least 8 in test, but `meme_joke` is the thinnest at 11.

On seed 42 the model reached 0.47 accuracy and 0.23 macro F1. It predicted
`hot_take` for 75 of the 79 test posts, so almost all of its correct answers
were the 35 real hot takes. It never predicted `meme_joke` at all. The
imbalance in my data (44% `hot_take`) is the first thing I would look at.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I told Claude I wanted six labels: `hot_take`,
  `analysis`, `reaction`, `substantive`, `low_effort` and `meme_joke`.
- *What came back:* It pointed out that `substantive` and `low_effort` aren't
  separate categories but umbrellas over the other four (every analysis post
  is also substantive, every hot take also low effort), so most posts would
  have two correct labels. It also noted that 200 posts over six labels leaves
  about 5 per label in the test split.
- *What I changed:* I dropped `substantive` and `low_effort` and kept four
  labels, then had it help me write edge rules for every pair, including the
  deletion test and the fixed checking order.

**Moment 2**

- *What I asked for:* After labelling my first 23 comments cold, I asked
  Claude whether my labels were right.
- *What came back:* It reviewed them against my own rules and flagged cases
  where I had broken them, such as calling a self-deprecating joke a
  `reaction`, and calling a stat-backed post a `reaction` because it sounded
  emotional. It also caught a typo (`hot-take`) and that my notes were empty.
- *What I changed:* I relabelled 8 of the 23 (marked `cold, revised after AI
  review`). Three of them became my hard cases above. I didn't accept every
  suggestion; my other 15 labels stayed as I first had them.

**Pre-labelling disclosure:**

Rows 1 to 23 of `labels.csv` were labelled by me before any AI input (8 of
them later revised after an AI review, as noted in the `note` column). The
other 499 rows were pre-labelled by Claude, which read each comment and
applied my four definitions and the patterns from my 23 cold labels.
[FILL IN: say honestly how many of the 499 you then read and checked, and
roughly how many labels you changed. If you have not checked them yet, say
that. Also say who labelled the 25 `meme_joke` comments added for the
improvement (their `note` says which thread they came from).]

For the improvement I removed 130 `hot_take` rows, so 374 Claude-pre-labelled
rows remain in the final `labels.csv`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

521 rows, `distilbert-base-uncased`, 3 epochs, lr 2e-5, batch 16. Test split
79 posts per seed. From `results_three_seeds_before.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.468 | 0.468 | 0.494 | MISSED |
| 2. Lowest per-label F1 | ≥ 0.45 | 0.00 (`meme_joke`) | 0.00 (`analysis`, `meme_joke`) | 0.00 (`analysis`, `meme_joke`) | MISSED |
| 3. Posts per label | 45 to 60 | 75 to 230 | same data | same data | MISSED |
| 4. Self-relabel match | ≥ 17 of 20 | not measured | not measured | not measured | NOT MEASURED |
| 5. Confidence gap (top third minus bottom third) | ≥ 0.20 | +0.54 | +0.27 | +0.31 | MET |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, before:

| true \ predicted | analysis | hot_take | reaction | meme_joke |
|---|---|---|---|---|
| **analysis** | 1 | 15 | 0 | 0 |
| **hot_take** | 1 | 34 | 0 | 0 |
| **reaction** | 0 | 15 | 2 | 0 |
| **meme_joke** | 0 | 11 | 0 | 0 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

15 real `analysis` posts were called `hot_take`, and only 1 went the other
way; the same 15-to-0 pattern holds for `reaction`. This isn't one boundary
failing. The whole `hot_take` column is full: the model predicted `hot_take`
for 75 of 79 posts, so it never learned any boundary at all. It learned that
`hot_take` was 44% of my data and guessed it almost every time.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

Verdicts on the "before" run.

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60 | MISSED | Best seed was 0.494 |
| 2 | Every label F1 | ≥ 0.45 | MISSED | `meme_joke` was 0.00 on all three seeds |
| 3 | Posts per label | 45 to 60 | MISSED | `hot_take` had 230 posts |
| 4 | Self-relabel match | ≥ 17 of 20 | NOT MEASURED | I haven't done the relabel yet |
| 5 | Confidence gap | ≥ 0.20 | MET | Lowest gap was +0.27 (seed 7) |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 3 (balance) missed: too many `hot_take` posts.** 230 of 521 posts
were `hot_take`. This is a data-collection miss, not a model one: r/nba
threads are full of unsupported opinions, and I collected and labelled
everything rather than sampling for balance.

**Criteria 1 and 2 missed: imbalance plus undertraining.** Two pieces of
evidence. First, the confusion matrix: 75 of 79 test posts were predicted
`hot_take`, so the model fell back on the most common label, which is what
imbalance causes. Second, the training log: training loss was still falling
at epoch 3 (1.34 to 1.00) and validation macro F1 rose every epoch (0.15,
0.31, 0.33 on seed 42). The model stopped before it had learned anything
beyond "guess the majority label". 3 epochs on 364 posts is only 69 training
steps.

**Labelling or model problem?** [FILL IN after running the agreement check:
the course asks you to use your agreement report here. If you agreed with
the staff on most `analysis` vs `hot_take` posts, your labelling of that
boundary is probably consistent and the misses are a model/data-size problem.
If you disagreed mostly on that boundary, some of the confusion is your
labels.] A labelling problem is also possible here because 374 of the final
labels are AI pre-labels I haven't fully checked.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:** Three things, which I'm reporting together rather than
pretending it was one:

1. **Balanced the labels.** I cut `hot_take` from 230 to 100 and added 25
   `meme_joke` comments from three new threads (75 to 100). Final counts:
   111 / 105 / 100 / 100, 416 rows.
2. **Switched base model** from `distilbert-base-uncased` to
   `distilroberta-base`, which was pretrained on more web text and handles
   Reddit slang better.
3. **Trained for 8 epochs instead of 3**, chosen from the validation curve.

**Which diagnosis pointed at it:** The imbalance diagnosis pointed at (1):
the model guessed `hot_take` for 75 of 79 posts. The undertraining diagnosis
pointed at (3): loss was still falling at epoch 3. I picked 8 epochs from
**validation** numbers, not test numbers. On a 50-epoch run, validation loss
was lowest around epoch 5 to 8 and rose after that (0.88 at epoch 5, 1.56 at
epoch 50) while validation F1 stayed flat, so going past 8 was only
overfitting. A 15-epoch run confirmed it: validation loss was lowest at
epoch 8 (0.82) and test F1 dropped. For (2), I compared models at 8 epochs on
validation macro F1: `distilroberta-base` reached 0.74, against 0.68 for
`distilbert-base-uncased`.

What I tried along the way (seed 42 only, test split of 59 to 63 posts):

| Run | Data | Model | Epochs | Test acc | Test macro F1 | Lowest label F1 |
|---|---|---|---|---|---|---|
| Before | 521 | distilbert | 3 | 0.47 | 0.23 | 0.00 |
| Balanced | 391 | distilbert | 3 | 0.49 | 0.32 | 0.00 (`hot_take`, `meme_joke`) |
| Longer | 391 | distilbert | 50 | 0.56 | 0.52 | 0.27 (`meme_joke`) |
| 8 epochs | 391 | distilbert | 8 | 0.59 | 0.53 | 0.13 (`meme_joke`) |
| More memes | 416 | distilbert | 8 | 0.65 | 0.64 | 0.48 (`hot_take`) |
| **Final** | 416 | **distilroberta** | 8 | 0.635 | 0.63 | 0.44 (`hot_take`) |

### Run Log — After

416 rows, `distilroberta-base`, 8 epochs, lr 2e-5, batch 16. Test split 63
posts.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.635 | [run section 6] | [run section 6] | [pending] |
| 2. Lowest per-label F1 | ≥ 0.45 | 0.44 (`hot_take`) | [run section 6] | [run section 6] | MISSED (seed 42 is already below) |
| 3. Posts per label | 45 to 60 | 100 to 111 | same data | same data | MISSED |
| 4. Self-relabel match | ≥ 17 of 20 | not measured | not measured | not measured | NOT MEASURED |
| 5. Confidence gap | ≥ 0.20 | +0.48 | [run section 6] | [run section 6] | [pending] |

Seed 42, after:

| true \ predicted | analysis | hot_take | reaction | meme_joke |
|---|---|---|---|---|
| **analysis** | 11 | 5 | 0 | 0 |
| **hot_take** | 3 | 7 | 1 | 4 |
| **reaction** | 1 | 2 | 14 | 0 |
| **meme_joke** | 0 | 3 | 4 | 8 |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

Yes, a lot, on seed 42. Accuracy went from 0.47 to 0.635 and macro F1 from
0.23 to 0.63. More importantly, the model now uses all four labels: before,
`analysis` and `meme_joke` were almost never predicted, and now
`analysis` gets 11 of 16 right and `meme_joke` 8 of 15. The confidence gap is
also wider (0.86 accuracy on the most-sure third, 0.38 on the least-sure).
Adding 25 jokes did the most for `meme_joke` (F1 0.13 to 0.64 with
distilbert), so data helped more than any setting. I can't call criteria 1
and 5 met until seeds 7 and 2024 are in, since a target has to hold on all
three.


---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**Criterion 2 (every label F1 ≥ 0.45):** `hot_take` is at 0.44, one post
short. Its errors go in every direction (3 to `analysis`, 1 to `reaction`, 4
to `meme_joke`), because my revised definition makes `hot_take` the
"everything without evidence" label that borders all three others. Next I
would check the AI pre-labels on `hot_take` and `meme_joke` posts, since
sarcastic opinions are easy to put on either side. I stopped because changing
settings again on the same test split would be tuning to the test set.

**Criterion 3 (45 to 60 per label):** I balanced the labels to 100 to 111
each, which fixes the problem the criterion was protecting against but
doesn't meet the number. Cutting to 60 per label would throw away almost 200
labelled posts, and the improvement showed more data helps more than
anything else. Looking back, the target was the wrong way round: the real
requirement is labels at *similar* sizes with at least 45 each, not a
ceiling of 60.

**Criterion 4 (self-relabel):** not done yet. [FILL IN once you relabel 20
random posts without looking.]

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant `hot_take` and `analysis` to be split by whether the evidence does
real work in the argument, but the model mostly learned surface signals:
numbers mean `analysis`, emotional words mean `reaction`, which is why 5
real `analysis` posts with soft evidence still land in `hot_take`. It also
can't fully separate "funny" from "opinion", since 4 hot takes were called
jokes, which makes sense because sarcasm only shows in meaning, not in
wording.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
