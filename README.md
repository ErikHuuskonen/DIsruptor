# JTBD Disruptor

Enter a product → get its Jobs To Be Done → choose a disruptive strategy → get 5 very different, scored business ideas that share the product's jobs and make it obsolete.

This README is also the **build instruction for Claude**. Any Claude session that changes the code reads this first and follows it.

---

## Workflow

### User flow

```
1. PRODUCT    user enters a product
2. JTBD       app outputs functional, emotional and social jobs + real competitors
3. STRATEGY   user chooses a disruptive strategy          ← new feature lives here
4. IDEAS      app outputs 5 business ideas + strategies that
              (a) do the same jobs to be done as the product
              (b) are built entirely on the chosen strategy
              (c) are scored for novelty and feasibility
```

### New feature: biological disruption strategies (step 3)

At step 3 the user can choose one of three biological strategies. The chosen strategy's full schema is sent to the AI as the disruptive strategy, and the AI turns it into 5 business ideas with the same JTBD as the given product.

| Strategy | Core logic | Status |
|---|---|---|
| **Parasite** | live off the incumbent's host (its customers/infrastructure) without killing it too early, then spread | ✅ schema done — `strategies/parasite.md` |
| **Predator** | find the weakest, most profitable target, capture it and take its full value at once; every hunt must pay for itself | ✅ schema done — `strategies/predator.md` |
| **Mushroom / Fungi** | grow an invisible network to where the value is, break down what others can't, trade with partners and become the infrastructure | ✅ schema done — `strategies/fungi.md` |

Rules for the feature:
- The user picks exactly one strategy.
- The whole strategy schema is the business logic of each idea, not a single feature added to it.
- Output format is the same as today: 5 ideas, as different from each other as possible, each with novelty and feasibility scores.
- Existing strategy chips and the free-text field stay available.

### Method: how a biological strategy schema is produced

Parasite was built with these steps. Predator and Fungi **must** be built the same way, one step at a time, so all three schemas have the same shape and can be swapped in the code.

```
1. UNIVERSAL RULE     explain the strategy that applies to ALL members of the group
                      (golden rule + analogy)
2. SHARED FUNCTIONS   list the concrete mechanisms all members share
                      (the core problem they solve + main functions)
3. ROLE WORDS         strip to letters + role words only (A, B, C, D / a, b, c)
4. SPECIFY            one main stage at a time: 4 sub-roles (a–d),
                      each with 4 mechanisms (i–iv)
5. GAP ANALYSIS       combine all stages, find missing stages, add them
6. SCHEMA             final flowchart: entities = letters only,
                      actions/functions = predicate words and process descriptions,
                      plus the master loop
```

### Schema format (shared by all three strategies)

```
X. STAGE NAME
   a. sub-role
      i.   mechanism
      ii.  mechanism
      iii. mechanism
      iv.  mechanism
   b. ...

Master loop:  X → Y → Z → ...  (repeats)
```

Reference: Parasite master loop

```
F. HOST SELECTION → A. ENTRY → B. EVASION → C. EXTRACTION → E. REPRODUCTION → D. TRANSMISSION
↑________________________________________________________________________________________↑
                                   repeats in new host
```

Predator master loop

```
E. TERRITORY → A. DETECTION → B. SELECTION → C. CAPTURE → D. CONSUMPTION → F. LEARNING
↑___________________________________________________________________________________↑
                          repeats when hungry, smarter each round
```

Fungi master loop

```
A. COLONIZATION → B. NETWORK → C. DIGESTION → D. EXCHANGE → F. DEFENSE → E. REPRODUCTION
↑_______________________________________________________________________________________↑
                                 repeats on new substrate
G. PERSISTENCE runs underneath all stages
```

### Development workflow

```
1. Develop one feature in the claude.ai session
2. Test it in the published JTBD Disruptor page
3. Claude gives the updated index.html
4. Download it and run:  ./sync.sh "what changed"
   → moves it into the local folder and pushes to GitHub
```

One feature = one sync. Every feature goes to GitHub.

The same `index.html` runs in both places: claude.ai's built-in AI on claude.ai, and `server.py` + Anthropic API key locally.

---

## Run locally

Requires Python 3 (built into macOS). No packages to install.

```bash
cp .env.example .env        # then put your API key in .env
python3 server.py
```

Open http://localhost:8000

## Where to edit

| What | Where |
|---|---|
| Look and colors | `<style>` in `index.html` |
| JTBD analysis prompt | `analyzeJTBD()` in `index.html` |
| Business idea prompt | `generateDisruptors()` in `index.html` |
| Strategy buttons | `.strategy-chips` in `index.html` |
| Strategy schemas | `strategies/` |
| Model / token limit | `.env` |
