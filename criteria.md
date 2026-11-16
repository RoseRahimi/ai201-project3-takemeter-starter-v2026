# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

Overall accuracy on the held-out test split is at least **0.60** on each of
the three seeds.

**Why this target:** With four labels a random guesser gets about 25%, so 0.60
is more than double chance. It means 18 of the 30 test posts right. I didn't go
higher because the `analysis` / `hot_take` boundary is subtle on r/nba (many
takes include a stat), and 200 posts is a small training set.

---

## 2. Per-label performance

Every label has an F1 of at least **0.45** on each of the three seeds.

**Why this target:** Each label has only about 7 or 8 posts in the test split,
so a single miss can move its F1 by about 0.1. A floor of 0.45 still catches a
label the model has basically failed to learn. I expect `analysis` to be
closest to the floor, because it's the rarest kind of post on r/nba and it
looks a lot like hot takes that quote a stat.

---

## 3. Balance

In my 200 labeled posts, every label has between **45 and 60** posts (22.5% to
30%).

**Why this target:** 45 posts puts about 7 in the test split, close to the
README's warning line of about 8. Below that, a label's F1 is mostly noise. The
ceiling of 60 is there because r/nba is flooded with hot takes and jokes, and
without a cap those two would crowd out `analysis`, which I'll have to search
for deliberately.

---

## 4. Consistency

At least a week after labeling, I relabel 20 randomly chosen posts from my 200
without looking at my original labels, and at least **17 of 20 (85%)** match.

**Why this target:** If I can't reproduce my own labels, the model is learning
my mood on the day, not my rules. I allowed 3 mismatches because some r/nba
posts sit on real boundaries (a take that quotes one stat, sarcasm that could
be a sincere take), but more than 3 would mean my decision rules for
`analysis` / `hot_take` and `hot_take` / `meme_joke` aren't specific enough.
20 posts is 10% of my dataset, enough to catch a drifting rule without
relabeling everything.

---

## 5. Confidence

On each of the three seeds, accuracy on the model's most confident third of
test posts is at least **0.20 higher** than on its least confident third.

**Why this target:** Each third is 10 posts, so 0.20 means at least 2 more
correct posts among the confident ones. If the gap is smaller, the model's
confidence tells you nothing, and you couldn't use it to decide which r/nba
posts to trust and which to check by hand.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
