# CLAUDE.MD -- Distributed Systems Research with Claude Code

**Project:** Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes: Arquitectura, Manejo de Fallos e Implicaciones en la Consistencia (título de trabajo, v1-5)
**Institution:** Universidad de Carabobo, Valencia, Estado Carabobo, Venezuela
**Author:** Angel A. Parejo R. — Valencia, Estado Carabobo, Venezuela — angelparejo@gmail.com
**Field:** Distributed Systems / Cloud-Native Infrastructure (Databases, Container Orchestration, Storage)
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile and confirm output at the end of every task
- **Single source of truth** -- Paper `main.tex` is authoritative; talks and supplements derive from it
- **Quality gates** -- weighted aggregate score; nothing ships below 80/100; see `quality.md`
- **Worker-critic pairs** -- every creator has a paired critic; critics never edit files
- **Auto-memory** -- corrections and preferences are saved automatically via Claude Code's built-in memory system
- **Air-gapped scripting** -- `scripts/` uses bash + Python standard library only. No `pip install`, no external packages, no R.
- **Language** -- the paper is drafted in **Spanish** (`/write`, humanizer). English translation + language editing is a dedicated final phase, run only before targeting the secondary (English) journal tier — see `domain-profile.md` → Target Journals. Scaffold config files (this file, `domain-profile.md`) stay in English as the scaffold's own technical instructions.

---

## Getting Started

1. Fill in the `[BRACKETED PLACEHOLDERS]` in this file
2. Run `/discover interview [topic]` to build your research specification
3. Or run `/new-project [topic]` for the full orchestrated pipeline

---

## Folder Structure

```
pg-k8s-paper/
├── CLAUDE.MD                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── Bibliography_base.bib        # Centralized bibliography
├── paper/                       # Main LaTeX manuscript (source of truth)
│   ├── main.tex                 # Primary paper file
│   ├── sections/                # Section-level .tex files
│   ├── figures/                 # Generated figures (.pdf, .png)
│   ├── tables/                  # Generated tables (.tex)
│   ├── talks/                   # Beamer presentations
│   ├── quarto/                  # Quarto RevealJS presentations
│   ├── preambles/               # LaTeX headers / shared preamble
│   ├── supplementary/           # Online appendix and supplements
│   └── replication/             # Replication package for deposit
├── data/                        # Benchmark traces and fault-injection logs
│   ├── raw/                     # Raw Chaos Mesh / Prometheus / operator logs (testbed output, gitignored)
│   └── cleaned/                 # Parsed RTO/RPO/latency series ready for analysis
├── scripts/                     # bash + Python stdlib only (air-gapped testbed, no external deps)
│   ├── run-experiment.sh        # e.g., orchestrates fault injection + workload runs
│   ├── parse-verifier.py        # e.g., parses operator/CSI logs into structured records
│   └── analyze.py               # e.g., non-parametric analysis (Mann-Whitney, Kruskal-Wallis, Spearman)
├── quality_reports/             # Plans, session logs, reviews, scores
├── explorations/                # Research sandbox (see rules)
├── templates/                   # Session log, quality report templates
└── master_supporting_docs/      # Reference papers and data docs
```

---

## Commands

```bash
# Paper compilation (latexmk handles multi-pass + biber automatically)
cd paper && latexmk main.tex

# Talk compilation
cd paper/talks && latexmk talk.tex

# Clean auxiliary files
cd paper && latexmk -c
```

> **Note:** `paper/latexmkrc` configures XeLaTeX, TEXINPUTS, and BIBINPUTS.
> On Overleaf, set compiler to XeLaTeX via Menu > Compiler — Overleaf reads `latexmkrc` automatically.

---

## Quality Thresholds

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate (blocking) |
| 90 | PR | Weighted aggregate (blocking) |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks (reported, non-blocking) |

See `quality.md` for weighted aggregation formula.

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| `/discover [mode] [topic]` | Discovery: interview, literature, data, ideation |
| `/strategize [mode] [question]` | Identification strategy, pre-analysis plan, or formal theory section (`theory` mode) |
| `/analyze [dataset]` | End-to-end data analysis |
| `/write [section]` | Draft paper sections + humanizer pass (`style-guide` mode extracts voice from prior papers) |
| `/review [file/--flag]` | Quality reviews (routes by target: paper, code, peer) |
| `/revise [report]` | R&R cycle: classify + route referee comments |
| `/talk [mode] [format]` | Create, audit, or compile Beamer presentations |
| `/submit [mode]` | Journal targeting → package → audit → final gate |
| `/tools [subcommand]` | Utilities: commit, compile, validate-bib, journal, etc. |
| `/checkpoint [--flag]` | Session handoff: memory + SESSION_REPORT + research journal (+ Obsidian if configured) |

> `/write` and the humanizer pass draft in **Spanish** for this project. English translation runs as a separate final pass before targeting the secondary (English) journal tier — see `domain-profile.md` → Target Journals.

---

## Beamer Custom Environments (Talks)

| Environment       | Effect        | Use Case       |
|-------------------|---------------|----------------|
| `[your-env]`      | [Description] | [When to use]  |

---

## Output Organization

<!-- Options: by-script (default) or by-purpose -->
Output organization: by-script

<!-- by-script:  paper/figures/rto_comparison/figure1.pdf, paper/tables/rto_comparison/table1.tex -->
<!-- by-purpose: paper/figures/recovery/rto_boxplot.pdf, paper/tables/robustness/spearman_corr.tex -->

---

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Paper | `paper/main.tex` | draft | Título de trabajo v1-5 (en español): "Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes..." |
| Experiments | `scripts/` | in-progress | bash+Python harnesses: Chaos Mesh fault injection, RTO/RPO measurement, CloudNativePG vs. Zalando/Patroni |
| Replication | `paper/replication/` | not started | Deposit status TBD |
| Talk | `paper/talks/` | -- | Not started |
