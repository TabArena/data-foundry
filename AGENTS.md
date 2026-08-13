# AGENTS.md

Guidance for autonomous coding agents (Claude Code, Cursor, Aider, …)
working inside the **Data Foundry** repository.

If you are an interactive contributor and just want to know the repo layout,
read [`README.md`](README.md) first. This document is the part of that
information an agent needs in order to act safely.

---

## What this repo is

Data Foundry is the data-layer toolkit behind
[BeyondArena](https://huggingface.co/datasets/TabArena/BeyondArena) and
[TabArena](https://tabarena.ai/), introduced in the paper
[*Beyond IID: How General Are Tabular Foundation Models, Really?*](https://arxiv.org/abs/2606.30410)
(arXiv:2606.30410). The Python package
(`src/data_foundry/`) defines:

* a pydantic-dataclass **schema** for tabular datasets, predictive ML tasks,
  and outer CV splits (`schema.py`);
* a **`CuratedContainer`** that bundles a DataFrame with that schema, persists
  it dtype-faithfully, and computes a Blake2b checksum over everything
  (`curation_container.py`);
* a **collections API** that pins immutable `(unique_name, uuid)` pointers
  and resolves them against a local warehouse or the BeyondArena Hugging
  Face mirror, with cache + force-download semantics (`collections/`);
* helpers used by curation notebooks — exploratory data checks
  (`dataset_checks.py`), post-hoc bundle integrity checks (`bundle_checks.py`)
  and recommended outer-CV split builders (`curation_recommendations.py`);
* a git-native **curation backlog** (`src/data_foundry/curation/`) that replaces
  the legacy curation Google Sheet. The source of truth is **one markdown record
  per candidate dataset** (YAML front-matter for the structured/dropdown fields +
  a free-text body for `## Comments` / `## Reference`) under `curation/records/`.
  Add or triage a dataset by creating/editing its `<unique_name>.md` file — by
  hand, with an agent, or via the dashboard. A local **Sheets-like dashboard**
  (`data-foundry-curation serve` → http://127.0.0.1:8765) edits those records in
  place and ships a built-in **Guidelines** tab (the curation criteria, from the
  paper). The per-record schema is `CurationRecord` (`curation/record.py`); the
  editable dropdown vocabularies live in `curation/vocabularies.yaml`. The CLI
  (`data-foundry-curation -h`) also covers `sync-notebooks` (refreshes each
  record's `notebook_path`, the stored pointer to its curation notebook),
  `import-sheet`, `validate`, `export`,
  and `build-site` (a read-only static site). That static site is published to
  GitHub Pages at https://tabarena.github.io/data-foundry/ — regenerated from
  `curation/records/` on every push to `main` by `.github/workflows/pages.yaml`,
  so editing a record and merging to `main` is what updates the public site.

The actual curation work happens in `datasets/`, which is mostly Jupyter
notebooks — see [`CONTRIBUTING_DATASETS.md`](CONTRIBUTING_DATASETS.md).

---

## High-leverage use cases for an agent

Roughly ordered by how often agents are useful here:

### 1. Processing a dataset — scaffolding its curation notebook from spreadsheet metadata

Highest-value: the curator has tab-separated metadata from a spreadsheet
and wants a populated notebook under `datasets/_dev/<topic>/<unique_name>/`.

The `/process-dataset` slash command at
[`.claude/commands/process-dataset.md`](.claude/commands/process-dataset.md) is the
canonical procedure — column mappings, snake-case conversion, target
subfolder picking, BibTeX templates, and which split helper to call for
which regime. **Always read that file before scaffolding.** It encodes
decisions you would otherwise have to guess at.

The skill writes a 21-cell notebook based on
`datasets/_template/_template.ipynb`. Read the template before writing so
the JSON structure is exact.

Its reference sections (§B–§E) are the **distilled conventions of the ~155 shipped
notebooks**: the ordered preprocessing recipe, the per-regime split recipes (including
the temporal loop, which the template only stubs), the recurring traps worth flagging,
and a table mapping every `bundle_checks` slug to the scaffold action that pre-empts it.
Keep them in sync when the collection's practice changes — the check-side evidence comes
from `scripts/beyond_arena/check_collection_bundles.py`, the practice-side evidence from
re-reading the notebooks' preprocessing / task-curation cells and `curation_comments`.
The governing rule for scaffolding is **pre-fill structure, never facts**: anything that
needs a look at the data becomes a `# TODO(verify): …` marker, which the notebook's
Bundle Checks cell then refuses to export (`meta_placeholder_left`).

### 2. Verifying a filled-in notebook before it ships

Once the curator has filled in and run the notebook, the `/verify-dataset` slash
command ([`.claude/commands/verify-dataset.md`](.claude/commands/verify-dataset.md))
is the second pass: it runs `bundle_checks` for the mechanical invariants and then
works a 13-item **judgment rubric** for what code cannot settle — is the link really
the original source, does the split regime match the real application, would every
feature have been known at prediction time, do the `curation_comments` describe what
the code actually does, does the BibTeX cite the right work. Verdicts are advisory;
`cannot-verify` is a valid outcome and must never be reported as `pass`.

### 3. Triaging candidate datasets (curation dashboard + guidelines)

The backlog is **one markdown record per candidate dataset** in `curation/records/`
(`<unique_name>.md`: YAML front-matter for structured/dropdown fields + a body with
`## Comments` / `## Reference`).

To assist, run the **`/triage-candidates`** slash command
([`.claude/commands/triage-candidates.md`](.claude/commands/triage-candidates.md)).
It starts the local dashboard
(`data-foundry-curation serve` → http://127.0.0.1:8765) and, importantly,
**loads the curation guidelines** — the IID/non-IID background, the dataset
*selection criteria*, and the *processing* conventions. **Read those guidelines
before advising** whether a dataset belongs in the benchmark or how to process it;
they encode decisions (IID vs temporal vs grouped, the selection criteria, the
processing conventions) you would otherwise guess at. The guidelines are summarized
in the skill and rendered in full in the dashboard's **Guidelines** tab
(`src/data_foundry/curation/static/guidelines.html`).

Add or triage a dataset by creating/editing its `<unique_name>.md` record (by hand,
with an agent, or in the dashboard); the dashboard and the `build-site` export both
read these files. The per-record schema is `CurationRecord` (`curation/record.py`);
dropdown options live in `curation/vocabularies.yaml`. `curation/_template.md` is a
copy-me, field-by-field guide.

**`data_foundry_status` is a merged multi-tag field** holding both work state
(`DF: Yes` / `WIP (DF)` / `WIP (Triage)` / `DF: Much work` / `DF: Suspended`) and shipped-collection
membership (`TabArena (v0.1)`, `BeyondArena`). Only datasets under `datasets/beyond_iid/`
(and the v0.1 set) carry a collection tag. **`DF: …` with no collection tag is a valid,
intentional state** — the dataset is in Data Foundry but not in a shipped collection
(it lives under `datasets/_maintenance/` — deprecated / suspended / out-of-scope — or
`datasets/_dev/`); do not "fix" it by adding a collection tag. See
`datasets/_maintenance/_deprecated/README.md`. (The separate `collections` field is only
for *external* benchmarks the dataset also appears in: TabSTAR, TabRed, CARTE/TARTE, ….)

### 4. Extending the package (schema, container, collections, examples)

When changing core code:

* **Tests live in `tests/`.** Run `pytest -q` after any change. The suite
  is fast (~2s); there is no excuse for not running it.
* **Linting:** `ruff check .` and `ruff format .`. Settings are in
  `pyproject.toml` (`[tool.ruff]`). `from __future__ import annotations`
  is mandatory in every file; 120-char lines; Google-style docstrings.
* **Examples in `examples/` are part of the docs surface.** When you add a
  feature, add or update the matching example, and (only if it's a major
  use case) link it from `README.md`.
* **`describe()` methods** on `DatasetMetadata`, `PredictiveMLTaskMetadata`,
  `PredictiveMLSplitsMetadata`, and `CuratedContainer` are the human-facing
  surface — keep them in sync if you add or rename schema fields.

### 5. Curation tooling work (checks, recommended splits, helpers)

**There are three check layers; put a new check in the right one.**

| Layer | Where | Scope |
|---|---|---|
| creation-time | `schema.py` `__post_init__` | coherence of *one* metadata object, no DataFrame needed (e.g. `group_labels` requires `group_on`, `time_horizon` requires its unit). Runs on every `CuratedContainer.load`, so a new rule here **must hold for every already-shipped container** — verify against the BeyondArena collection before making one hard. |
| exploratory | `dataset_checks.run_all_checks(...)` | statistics a human reads while curating. Returns five DataFrames whose rendered output is committed in the notebooks — don't change its output shape lightly. |
| post-hoc / bundle | `bundle_checks.py` | *cross-referential* checks over the assembled bundle (DataFrame + task + splits + dataset metadata) and, after export, the save/load round-trip. This is the default home for anything new. |

* `bundle_checks.run_bundle_checks(container)` returns a `BundleCheckReport`
  (errors / warnings / infos, each with a stable `slug`); the notebook calls
  `report.raise_if_errors()` before `save()`, and
  `verify_saved_container(save_path, container=...)` after it. A check that
  fires on a legitimately unusual dataset is accepted via `ignore=[slug]` in
  the notebook, with a reason.
* When adding a check, calibrate it against the shipped collection before
  choosing its severity (`error` only for "no consumer can use this"), and
  keep O(rows x cols) work behind the `heavy_cell_budget` guard.
* `dataset_checks.run_all_checks(...)` returns five DataFrames — see
  `simple_metadata_exploration_v2.py` (in `scripts/beyond_arena/`) for how
  the warehouse-wide stats are computed; that file's dtype categorization
  is the reference for `CuratedContainer._feature_dtype_counts`.
* `curation_recommendations.py` has three flavors — IID, grouped, temporal.
  IID and grouped have automated helpers; temporal splits are still
  manual.

### 6. Repo plumbing (CI, packaging, release)

`pyproject.toml` carries PyPI metadata. The release flow is documented in
`README.md` under "Releasing to PyPI" — `uv build` + `uv publish`. Don't
bump versions or publish without explicit human authorization.

---

## Conventions you must follow

* **Always read before writing.** The schema fields and `describe()` output
  are user-facing; pattern-match the existing style rather than inventing
  a new one.
* **`from __future__ import annotations`** at the top of every `.py` file.
* **Don't commit changes unless the user explicitly asks.** Same for
  pushes, PRs, and PyPI publishes.
* **Don't write README files, planning docs, or analysis files** unless
  asked. The repo intentionally has very few `.md` files.
* **Don't add comments that describe what the code does** — only *why*,
  when the why is non-obvious.
* **Curation notebooks must be valid JSON.** When editing them, use
  `nbformat` if available, or treat them as opaque structured data; do not
  hand-edit the cell `source` array without verifying the result parses.
* **Prose you write is held to the style rules in
  [AI Writing Tropes to Avoid](#ai-writing-tropes-to-avoid)** at the bottom of
  this file — docstrings, markdown, commit messages, and chat replies alike.

---

## Things that look like blockers but aren't

* **`local-data-warehouse/` is gitignored** and may be empty on a fresh
  clone. That's fine — only the toy container (in
  `src/data_foundry/examples/toy_container/`) ships in-tree; everything
  else is downloaded on demand via the collections API.
* **Huggingface_hub is an optional runtime requirement** for `prefetch` /
  `get_dataset` cache *misses* — if every container is already cached,
  the package does not import it. So a fresh dev env without HF set up
  can still run all of `pytest tests/`.
* **The toy container is regenerated by `scripts/build_toy_container.py`,**
  not edited by hand. If a test fails on a UUID/checksum mismatch, the
  fix is to regenerate, not to update the test expectation.

---

## Pointers

| Topic | Read |
|---|---|
| Repo overview, install, quickstart | [`README.md`](README.md) |
| Curation contribution flow | [`CONTRIBUTING_DATASETS.md`](CONTRIBUTING_DATASETS.md) |
| Schema definitions | [`src/data_foundry/schema.py`](src/data_foundry/schema.py) |
| Curation backlog (records, dashboard, import/export) | [`src/data_foundry/curation/`](src/data_foundry/curation/) |
| Curation records + dropdown vocab (data) | [`curation/`](curation) |
| Public read-only backlog (GitHub Pages) | [tabarena.github.io/data-foundry](https://tabarena.github.io/data-foundry/) · [`.github/workflows/pages.yaml`](.github/workflows/pages.yaml) |
| Triage candidates — dashboard + curation guidelines | [`.claude/commands/triage-candidates.md`](.claude/commands/triage-candidates.md) |
| Curation guidelines (selection criteria + processing) | [`src/data_foundry/curation/static/guidelines.html`](src/data_foundry/curation/static/guidelines.html) |
| Container save/load + describe | [`src/data_foundry/curation_container.py`](src/data_foundry/curation_container.py) |
| Bundle integrity checks (post-hoc + post-export) | [`src/data_foundry/bundle_checks.py`](src/data_foundry/bundle_checks.py) |
| Collections + cache helpers | [`src/data_foundry/collections/`](src/data_foundry/collections/) |
| Process a dataset — scaffold its curation notebook | [`.claude/commands/process-dataset.md`](.claude/commands/process-dataset.md) |
| Verify a filled-in notebook / bundle (checks + judgment rubric) | [`.claude/commands/verify-dataset.md`](.claude/commands/verify-dataset.md) |
| Browse / prefetch a collection | [`.claude/commands/browse-collection.md`](.claude/commands/browse-collection.md) |
| Load a single dataset | [`.claude/commands/get-dataset.md`](.claude/commands/get-dataset.md) |
| Fit + score a model on a dataset | [`.claude/commands/benchmark-dataset.md`](.claude/commands/benchmark-dataset.md) |
| Notebook template | [`datasets/_template/_template.ipynb`](datasets/_template/_template.ipynb) |
| Examples (use-case anchors) | [`examples/`](examples) |

---

# AI Writing Tropes to Avoid

Applies to everything you write in this repo that a human reads: docstrings,
comments, markdown docs, commit messages, PR descriptions, user-facing copy,
and your replies in the chat.

Source: [tropes.fyi](https://tropes.fyi) by [ossama.is](https://ossama.is)

---

## Word Choice

### "Quietly" and Other Magic Adverbs

Overuse of "quietly" and similar adverbs to convey subtle importance or understated power. AI reaches for these adverbs to make mundane descriptions feel significant. Also includes: "deeply", "fundamentally", "remarkably", "arguably".

**Avoid patterns like:**
- "quietly orchestrating workflows, decisions, and interactions"
- "the one that quietly suffocates everything else"
- "a quiet intelligence behind it"

### "Delve" and Friends

Used to be the most infamous AI tell. "Delve" went from an uncommon English word to appearing in a staggering percentage of AI-generated text. Part of a family of overused AI vocabulary including "certainly", "utilize", "leverage" (as a verb), "robust", "streamline", and "harness".

**Avoid patterns like:**
- "Let's delve into the details..."
- "Delving deeper into this topic..."
- "We certainly need to leverage these robust frameworks..."

### "Tapestry" and "Landscape"

Overuse of ornate or grandiose nouns where simpler words would do. "Tapestry" is used to describe anything interconnected. "Landscape" is used to describe any field or domain. Other offenders: "paradigm", "synergy", "ecosystem", "framework".

**Avoid patterns like:**
- "The rich tapestry of human experience..."
- "Navigating the complex landscape of modern AI..."
- "The ever-evolving landscape of technology..."

### The "Serves As" Dodge

Replacing simple "is" or "are" with pompous alternatives like "serves as", "stands as", "marks", or "represents". AI avoids basic copulas because its repetition penalty pushes it toward fancier constructions (I've studied this!).

**Avoid patterns like:**
- "The building serves as a reminder of the city's heritage."
- "Gallery 825 serves as LAAA's exhibition space for contemporary art."
- "The station marks a pivotal moment in the evolution of regional transit."

---

## Sentence Structure

### Negative Parallelism

The "It's not X -- it's Y" pattern, often with an em dash. The single most commonly identified AI writing tell. Man I f*cking hate it. AI uses this to create false profundity by framing everything as a surprising reframe. One in a piece can be effective; ten in a blog post is a genuine insult to the reader. Before LLMs, people simply did not write like this at scale. Includes the causal variant "not because X, but because Y" where every explanation is framed as a surprise reveal, the em-dash dismissal "X -- not Y", and the cross-sentence reframe where the same noun is negated then repositioned: "The question isn't X. The question is Y."

**Avoid patterns like:**
- "It's not bold. It's backwards."
- "Feeding isn't nutrition. It's dialysis."
- "Half the bugs you chase aren't in your code. They're in your head."

### "Not X. Not Y. Just Z."

The dramatic countdown pattern. AI builds tension by negating two or more things before revealing the actual point. Creates a false sense of narrowing down to the truth.

**Avoid patterns like:**
- "Not a bug. Not a feature. A fundamental design flaw."
- "Not ten. Not fifty. Five hundred and twenty-three lint violations across 67 files."
- "not recklessly, not completely, but enough"

### "The X? A Y."

Self-posed rhetorical questions answered immediately in the next sentence or clause. The model asks a question nobody was asking, then answers it for dramatic effect. Thinks this is the epitome of great writing.

**Avoid patterns like:**
- "The result? Devastating."
- "The worst part? Nobody saw it coming."
- "The scary part? This attack vector is perfect for developers."

### Anaphora Abuse

Repeating the same sentence opening multiple times in quick succession.

**Avoid patterns like:**
- "They assume that users will pay... They assume that developers will build... They assume that ecosystems will emerge... They assume that..."
- "They could expose... They could offer... They could provide... They could create... They could let... They could unlock..."
- "They have built engines, but not vehicles. They have built power, but not leverage. They have built walls, but not doors."

### Tricolon Abuse

Overuse of the rule-of-three pattern, often extended to four or five. A single tricolon is elegant; three back-to-back tricolons are a pattern recognition failure.

**Avoid patterns like:**
- "Products impress people; platforms empower them. Products solve problems; platforms create worlds. Products scale linearly; platforms scale exponentially."
- "identity, payments, compute, distribution"
- "workflows, decisions, and interactions"

### "It's Worth Noting"

Filler transitions that signal nothing. AI uses these phrases to introduce new points without actually connecting them to the previous argument. Also includes: "It bears mentioning", "Importantly", "Interestingly", "Notably".

**Avoid patterns like:**
- "It's worth noting that this approach has limitations."
- "Importantly, we must consider the broader implications."
- "Interestingly, this pattern repeats across industries."

### Superficial Analyses

Tacking a present participle ("-ing") phrase onto the end of a sentence to inject shallow analysis that says nothing. The model attaches significance, legacy, or broader meaning to mundane facts using phrases like "highlighting its importance", "reflecting broader trends", or "contributing to the development of...".

**Avoid patterns like:**
- "contributing to the region's rich cultural heritage"
- "This etymology highlights the enduring legacy of the community's resistance and the transformative power of unity in shaping its identity."
- "underscoring its role as a dynamic hub of activity and culture"

### False Ranges

Using "from X to Y" constructions where X and Y aren't on any real scale. In legitimate use, "from X to Y" implies a spectrum with a meaningful middle. AI uses it as a fancy way to list two loosely related things. "From innovation to cultural transformation" -- what's in between???? Nothing!

**Avoid patterns like:**
- "From innovation to implementation to cultural transformation."
- "From the singularity of the Big Bang to the grand cosmic web."
- "From problem-solving and tool-making to scientific discovery, artistic expression, and technological innovation."

---

## Paragraph Structure

### Short Punchy Fragments

Excessive use of very short sentences or sentence fragments as standalone paragraphs for manufactured emphasis. RLHF training has pushed models toward "writing for readability" aimed at the lowest common denominator: one thought per sentence, no mental state-keeping required. It's an inhuman style. No real person writes first drafts this way because it doesn't match how humans think or speak.

**Avoid patterns like:**
- "He published this. Openly. In a book. As a priest."
- "These weren't just products. And the software side matched. Then it professionalised. But I adapted."
- "Platforms do."

### Listicle in a Trench Coat

Numbered or labeled points dressed up as continuous prose. The model writes what is essentially a listicle but wraps each point in a paragraph that starts with "The first... The second... The third..." to disguise the format. Perhaps you told it to stop generating lists and it decided to do this instead... still very common.

**Avoid patterns like:**
- "The first wall is the absence of a free, scoped API... The second wall is the lack of delegated access... The third wall is the absence of scoped permissions..."
- "The second takeaway is that... The third takeaway is that... The fourth takeaway is that..."

---

## Tone

### "Here's the Kicker"

False suspense transitions that promise a revelation but deliver a point that did NOT need the buildup. The model uses these phrases to manufacture drama before an otherwise unremarkable observation LOL. Also includes: "Here's the thing", "Here's where it gets interesting", "Here's what most people miss", "Here's the starting point", "Here's the deal".

**Avoid patterns like:**
- "Here's the kicker."
- "Here's the thing about AI adoption."
- "Here's where it gets interesting."

### "Think of It As..."

The patronizing analogy. AI constantly reaches for "Think of it as..." or "It's like a..." to simplify concepts. The model defaults to teacher mode and assumes the reader needs a metaphor to understand anything. Often produces analogies that are less clear than the original concept.

**Avoid patterns like:**
- "Think of it like a highway system for data."
- "Think of it as a Swiss Army knife for your workflow."
- "It's like asking someone to buy a car they're only allowed to sit in while it's parked."

### "Imagine a World Where..."

The classic AI invitation to futurism. To sell the argument usually begins with "Imagine" followed by a list of wonderful things that will happen if the reader agrees with the premise.

**Avoid patterns like:**
- "Imagine a world where every tool you use -- your calendar, your inbox, your documents, your CRM, your code editor -- has a quiet intelligence behind it..."
- "In that world, workflows stop being collections of manual steps and start becoming orchestrations."

### False Vulnerability

Simulated self-awareness or honesty that reads as performative. The model pretends to break the fourth wall or admit a bias, creating a false sense of authenticity. Real vulnerability is specific and uncomfortable; AI vulnerability is polished and risk-free!!!!

**Avoid patterns like:**
- "And yes, I'm openly in love with the platform model"
- "And yes, since we're being honest: I'm looking at you, OpenAI, Google, Anthropic, Meta"
- "This is not a rant; it's a diagnosis"

### "The Truth Is Simple"

Asserting that something is obvious, clear or simple instead of actually proving it. If you have to tell the reader your point is clear, it very likely isn't. Also includes the dramatic reveal variant: "but none of them is the real story. The real story is..." -- claiming privileged insight while waving away everything before it.

**Avoid patterns like:**
- "The reality is simpler and less flattering"
- "History is unambiguous on this point"
- "History is clear, the metrics are clear, the examples are clear"

### Grandiose Stakes Inflation

Everything is the most important thing ever. AI inflates the stakes of every argument to world-historical significance. A blog post about API pricing becomes a meditation on the fate of civilization.

**Avoid patterns like:**
- "This will fundamentally reshape how we think about everything."
- "will define the next era of computing"
- "something entirely new"

### "Let's Break This Down"

The pedagogical voice that assumes the reader needs hand-holding. AI defaults to a teacher-student dynamic even when writing for expert audiences. Also includes: "Let's unpack this", "Let's explore", "Let's dive in".

**Avoid patterns like:**
- "Let's break this down step by step."
- "Let's unpack what this really means."
- "Let's explore this idea further."

### Vague Attributions

Attributing claims to unnamed authorities instead of being specific. AI loves to invoke "experts", "observers", "industry reports", and "several publications" without naming anyone. It also inflates the quantity of sources -- presenting what one person said as a widely held view, or writing "several publications have cited" when it means two. If you can't name the expert, you don't have a source.

**Avoid patterns like:**
- "Experts argue that this approach has significant drawbacks."
- "Industry reports suggest that adoption is accelerating."
- "Observers have cited the initiative as a turning point."

### Invented Concept Labels

AI clusters invented compound labels that sound analytical without being grounded. It appends abstract problem-nouns (paradox, trap, creep, divide, vacuum, inversion) to domain words -- "supervision paradox", "acceleration trap", "workload creep" -- and uses them as if they're established, rigorously defined terms. They function as rhetorical shorthand: name a thing, skip the argument. Multiple such labels in the same piece is a strong signal of AI slop.

**Avoid patterns like:**
- "the supervision paradox"
- "the acceleration trap"
- "workload creep"

---

## Formatting

### Em-Dash Addiction

Compulsive overuse of em dashes for dramatic pauses, parenthetical asides and pivot points. A human writer might use 2-3 per piece (and naturally); AI will use 20+.

**Avoid patterns like:**
- "The problem -- and this is the part nobody talks about -- is systemic."
- "The tinkerer spirit didn't die of natural causes -- it was bought out."
- "Not recklessly, not completely -- but enough -- enough to matter."

### Double-Hyphen Dash

The em dash wearing a false moustache. Once "em dash means AI" became common knowledge, the character started getting swapped for a double hyphen: sometimes because the text passed through a markdown conversion, sometimes because someone ran a find-and-replace to look more human, sometimes because the model was steered off the character while keeping the habit. Either way the compulsive mid-sentence pivot survives the substitution, which is what actually gives it away. Writers who reach for double hyphens honestly do so once or twice out of typographic laziness, rarely fifteen times in one post. Flagged at five or more per thousand words.

**Avoid patterns like:**
- "The problem -- and this is the part nobody talks about -- is systemic."
- "It's not a rewrite -- it's a reckoning."
- "We shipped it fast -- maybe too fast -- and paid for it later."

### Bold-First Bullets

Every bullet point or list item starts with a bolded phrase or sentence. Extremely common in Claude and ChatGPT markdown output. Almost nobody formats lists this way when writing by hand. It's a telltale sign of AI-generated documentation and blog posts AND README files (especially with emojis).

**Avoid patterns like:**
- "Every single bullet point begins with a bold keyword."
- "**Security**: Environment-based configuration with..."
- "**Performance**: Lazy loading of expensive resources..."

### Unicode Decoration

Use of unicode arrows (->), smart/curly quotes, and other special characters that can't be easily typed on a standard keyboard. Real writers typing in a text editor produce straight quotes and -> or =>. Claude in particular loves the -> arrow.

**Avoid patterns like:**
- "Input → Processing → Output"
- "This leads to better outcomes → which means higher engagement"
- "“Smart quotes” instead of straight "quotes" that you’d actually type"

---

## Composition

### Fractal Summaries

"What I'm going to tell you; what I'm telling you; what I just told you" -- applied at every level of the document. Every subsection gets a summary. Every section gets a summary. The document itself gets a summary.

**Avoid patterns like:**
- "In this section, we'll explore... [3000 words later] ...as we've seen in this section."
- "A conclusion that restates every point already made in the previous 3000 words"
- "And so we return to where we began."

### The Dead Metaphor

Latching onto a single metaphor and beating it into the ground across the entire thing. A human writer would introduce a metaphor, use it then move on. AI will repeat the same metaphor 5-10 times.

**Avoid patterns like:**
- "The ecosystem needs ecosystems to build ecosystem value."
- "Walls and doors used 30+ times in the same article"
- "Every paragraph finds a way to say "primitives" again"

### Historical Analogy Stacking

ESPECIALLY COMMON IN TECHNICAL WRITING: Rapid-fire listing of historical companies or tech revolutions to build false authority.

**Avoid patterns like:**
- "Apple didn't build Uber. Facebook didn't build Spotify. Stripe didn't build Shopify. AWS didn't build Airbnb."
- "Every major technological shift -- the web, mobile, social, cloud -- followed the same pattern."
- "Take Spotify... Or consider Uber... Airbnb followed a similar path... Shopify is another example... Even Discord..."

### One-Point Dilution

Making a single argument and restating it in 10 different ways across thousands of words. The model pads a simple thesis to feel "comprehensive" by rephrasing the same idea with different metaphors, examples, and framings. An 800-word argument becomes 4000 words of circular repetition.

**Avoid patterns like:**
- "The same point, restated eight ways across 4000 words."
- "Each section rephrases the thesis with a different metaphor but adds nothing new"

### Content Duplication

Repeating entire sections or paragraphs verbatim within the same piece. This happens when the model loses track of what it has already written, especially in longer pieces. A dead giveaway of unedited AI output. Less common nowadays.

**Avoid patterns like:**
- "The same section appeared twice, word-for-word identical."
- "Paragraph 3 and paragraph 17 are the same sentence reworded"

### The Signposted Conclusion

Explicitly announcing the conclusion with "In conclusion", "To sum up", or "In summary". Competent writing doesn't need to tell you it's concluding. The reader can feel it. AI signals its structural moves because it's following a template, not writing organically.

**Avoid patterns like:**
- "In conclusion, the future of AI depends on..."
- "To sum up, we've explored three key themes..."
- "In summary, the evidence suggests..."

### "Despite Its Challenges..."

The rigid formula where AI acknowledges problems only to immediately dismiss them. Always follows the same beat: "Despite its [positive words], [subject] faces challenges..." then ends with "Despite these challenges, [optimistic conclusion].".

**Avoid patterns like:**
- "Despite these challenges, the initiative continues to thrive."
- "Despite its industrial and residential prosperity, Korattur faces challenges typical of urban areas."
- "Despite their promising applications, pyroelectric materials face several challenges that must be addressed for broader adoption."

---

Remember: any of these patterns used once might be fine. The problem is when
multiple tropes appear together or when a single trope is used repeatedly.
Write like a human: varied, imperfect, specific.
