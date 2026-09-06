# 02805 — Social Graphs and Interactions · course reference

**Read this before doing anything else in this repo.** It is the shared context file for
human group members and for coding agents. Everything in it has been checked against the
live course site or against the files on disk — if you change a fact here, verify it first.

---

## 1. What this repo is

The workspace and public website for a 3-person group taking **02805 Social Graphs and
Interactions** at DTU, autumn 2026. Each week we work through the course page, do the
exercises, and publish one post about what we found.

| | |
| --- | --- |
| Repository | <https://github.com/martinmoll/SocialGraphsAndInteractions> |
| Live site (GitHub Pages) | <https://martinmoll.github.io/SocialGraphsAndInteractions/> |
| Default branch | `main` |

---

## 2. Course site map

Base URL: **<https://sunelehmann.com/socialgraphs2026-web/>**

| Page | URL | Notes |
| --- | --- | --- |
| Home | `index.html` | Schedule, tests, project, groups — all as anchors on this one page: `#overview`, `#weeks`, `#tests`, `#project`, `#groups`. There is **no** separate project page. |
| The new way of working | `the-new-way.html` | The rules on AI use in this course. Required reading. |
| Week 1 · Networks | `weeks/week1.html` | Published |
| Week 2 · Models & null models | `weeks/week2.html` | Published |
| Weeks 3–8 | `weeks/week{N}.html` | **Not yet published — these URLs 404.** Each week's page goes up one session ahead. |
| Course data | `data/` | Dataset releases and download links. See §5. |
| Textbook | <https://www.networkatlas.eu/> | Michele Coscia, *The Atlas for the Aspiring Network Scientist*, 2nd ed. Free. Week 1 reading: ch. 6 (Basic Graphs), ch. 9 (Degree). |

Two things that trip up link-guessing:

- `weeks/` on its own is a **404**. Link the individual week files.
- Week pages appear one session ahead. If `week{N}.html` 404s, the material simply is not
  released yet — do not substitute a different source.

**Agents: fetch the week page rather than working from this summary.** This file is a map,
not a replacement for the material. The week pages carry interactive explorables and the
exact exercise wording, and both matter.

---

## 3. Schedule and assessment

Wednesdays from 09:00, building 303A (Auditorium 43, 44; classroom 46).
Instructor: Sune Lehmann, <sljo@dtu.dk>.

| Week | Topic | Date |
| --- | --- | --- |
| 1 | Networks | Wed 2 Sep |
| 2 | Models & null models | Wed 9 Sep |
| 3 | Who matters, and why | Wed 16 Sep |
| 4 | Communities & backbones | Wed 23 Sep |
| 5 | NLP I | Wed 30 Sep |
| 6 | NLP II | Wed 7 Oct |
| 7 | NLP III | Wed 21 Oct |
| 8 | Networks × language | Wed 28 Oct |
| 9–13 | Project period | — |

| Component | Weight | When |
| --- | --- | --- |
| Test 1 (weeks 1–4) | 25% | Wed 30 Sep, first hour |
| Test 2 (weeks 5–8) | 25% | Wed 4 Nov, first hour |
| Final project | 50% | Weeks 9–13; demo fair Wed 2 Dec |

Both tests are **pen-and-paper, closed-book, in class** — roughly 60 minutes, roughly 25
multiple-choice questions, testing application rather than recall. There are no take-home
assignments. There are no lectures: after a short framing talk each Wednesday, groups work
through the week's page at their own pace.

---

## 4. How the course works

> **"We use paper to ensure understanding. We use agents to explore the world."**

The course is designed around the assumption that students have capable AI tools. That
assumption comes with a split, and the split is the whole point. Every exercise carries one
of three labels:

### 🧠 Learn — AI hands-off

Concepts and hand calculations. Doing these with a machine is pointless: **this is the test
material**, and the tests are individual and on paper. Draw the graph, write the adjacency
matrix, count the triangles yourself.

### 🚀 Builder — full agentic mode

Ambitious goals, all tools allowed. Judged on the outcome *and* on the ability to **defend
every choice in it** during a live demo. An agent writing code you cannot explain is a
failure mode here, not a shortcut.

### 🔬 Tool — the LLM as measurement instrument

Using a model to label, extract, or classify data. The skill being taught is knowing when to
trust the machine, so the deliverable must include **validation against a ground-truth
sample and an error analysis**.

### Documenting AI use

The final project must include an **`AI_METHODS.md`** recording every place a model touched
the results and how that was checked. "The model said so" is explicitly not a method.

### The weekly rhythm

Every week ends the same way (exercise `N.8`):

1. Use the week's tools on the shared playground dataset — freely, creatively.
2. Write one post for the group site: what you asked, what you did, at least one figure or
   table, and what surprised you.
3. Post the link in the Teams channel **by Monday evening**.
4. Read the other groups' posts and leave constructive criticism on at least one.

### Group rules

Groups of three, kept all semester (smaller is fine, larger is not). The binding constraint:
**everyone must be able to solve everything.** The tests are individual and do not care who
in the group understood it.

---

### ⚠️ Instructions for agents

- **Do not solve 🧠 Learn exercises.** They are individual test preparation, and answering
  them removes their only purpose. If asked about one, explain the underlying concept, or
  check work that has already been done by hand — but do not produce the answer.
- **Do not silently make modelling choices** on 🚀 Builder work. Every threshold, filter,
  projection and layout has to be defensible out loud by a human. Surface the choice and say
  what the alternative would have changed.
- **Never present model output as measurement** on 🔬 Tool work without validation against a
  labelled sample.
- Prefer fetching the live week page over relying on any summary, including this one.

---

## 5. The shared dataset

One dataset all semester: the **303 characters in Wikipedia's `Category:Marvel Comics
superheroes`** — first the network of links between their pages, later the pages themselves.
Frozen snapshots, so every group computes on identical data while Wikipedia moves on.

### Releases

| Files | Arrives | What |
| --- | --- | --- |
| `week1_edges.tsv`, `week1_nodes.tsv` | Week 1 — **out now** | Unweighted directed network: an edge A → B wherever A's article links to B's. 303 nodes, 1,784 edges. |
| weighted edition | ~week 3 | The same edges, plus how often each link is repeated. |
| bipartite edition | ~week 4 | Pages × people. |
| raw text | week 5 | Full wiki-source per page, for the language half. Too big for the course site — served from DTU storage, link appears at release. |

### Week 1 files

Downloaded to `Data/Week1/`. Upstream:
`https://sunelehmann.com/socialgraphs2026-web/data/week1_edges.tsv` and
`.../week1_nodes.tsv`.

**`week1_edges.tsv`** — 1,789 lines total: 5 `#` comment lines + 1,784 directed edges.
Two columns, source and target, both Wikipedia page titles with underscores for spaces.

**`week1_nodes.tsv`** — 307 lines total: 3 `#` comment lines + a real header row + 303 rows.
Columns: `node_id`, `name`, `wikidata_id`, `url`, `description`. `node_id` matches the ids
used in the edge file. The node file carries no degrees and no statistics — computing those
is our job.

### Facts you need before loading it

- **The edge file's header line is itself commented out** (`# source⇥target`), so a reader
  that strips `#` lines gets no header and the column names have to be supplied.
- The node file's one-line blurbs **contain unescaped `"` characters**. A reader with default
  quote handling will mangle rows; quoting has to be disabled.
- **17 of the 303 characters have no edge in either direction.** Building the graph from the
  edge list alone gives you **286 nodes** and silently drops them. The node set has to come
  from the node file. *(Verified against the files in `Data/Week1/`: edges-only → 286 nodes;
  roster-first → 303 nodes and 17 isolates; 1,784 edges either way; every edge endpoint
  appears in the roster.)*
- The isolates are part of the story, not noise to be cleaned away.

### Where it came from

Built 26 August 2026 from the live English Wikipedia. Two pipeline decisions are worth
citing whenever we report on this network, because they are exactly the kind of choice week
1 is about:

1. **Edges come from the article text, not Wikipedia's link index.** The index counts links
   contributed by shared navigation templates — every Avenger carries the same team navbox,
   which would make whole rosters mutually adjacent as a templating artefact rather than
   because anyone's article mentions anyone. Here an edge means the running text of A's
   article actually links B.
2. **Redirects are resolved on both ends**, so `[[Spidey]]` and `[[Spider-Man]]` are one
   node, and a link to any alias still lands on the character.

Both could have been decided differently, and the network would have come out different.
When our own project crawls a domain, those choices become ours.

---

## 6. Repo conventions

| Path | Holds |
| --- | --- |
| `Data/Week{N}/` | Frozen course datasets, exactly as downloaded. **Never edited.** |
| `Notebooks/Week{N}/` | Jupyter notebooks for that week's 🚀 Builder exercises. |
| `Figures/Week{N}/` | Exported plots referenced by that week's post. |
| `posts/week{N}/` | That week's write-up for the site. |
| `index.html` | Site homepage, served at the Pages root. |
| `docs/` | Documentation for us, not for the site. This file lives here; `AI_METHODS.md` will join it during the project. |
| `CLAUDE.md`, `AGENTS.md` | Root-level pointers to this file. **They have to stay at the root** — that is the only place agent tools load them from automatically. |

**Datasets are committed to git.** They total ~125 KB, and a frozen release only does its
job if all three of us compute on identical bytes — gitignoring `Data/` would quietly break
that. *Revisit at week 5*: the raw wiki-source release comes from DTU storage and will likely
be too large to commit, at which point we need a download script instead.

Site structure (settled week 1): plain static HTML, no build step. index.html and style.css at the repo root; one post per week at posts/week{N}/index.html; figures at Figures/Week{N}/. All paths inside posts are relative (../../style.css), because a project Pages site serves from /SocialGraphsAndInteractions/ and absolute paths 404.

---

## 7. Maintaining this file

Each week, in this file:

- Add the new week page to the site map in §2 and flip its status to published.
- Add a release row in §5 when a new dataset stage drops, with the local path and the file's
  actual schema.
- **Re-verify counts rather than remembering them.** Every number in §5 came from running
  `wc -l` and a load-and-count against the files in `Data/`. If a number here disagrees with
  the data on disk, the data on disk is right.
