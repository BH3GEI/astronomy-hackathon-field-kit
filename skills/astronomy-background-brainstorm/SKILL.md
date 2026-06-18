---
name: astronomy-background-brainstorm
description: Brainstorm astronomy hackathon ideas from a local field kit of Chinese astronomy association materials. Use when Codex needs to turn astronomy background knowledge, observation guides, astrophotography files, question banks, image samples, or historical club materials into grounded project concepts, agent prompts, data products, demo scopes, judging themes, or event formats.
---

# Astronomy Background Brainstorm

## Overview

Use this skill to convert astronomy background material into concrete hackathon directions. Treat the repository as a field kit: every idea should point back to evidence in the files, and every project seed should have a small demo path.

## Workflow

1. Read `README.md` and `00-素材地图与筛选说明.md` first to understand the material map.
2. If the user asks for broad ideation, read `references/background-lenses.md` before proposing ideas.
3. Inspect only the relevant source folders after choosing a direction:
   - `01-共同语境与背景课件` for shared astronomy concepts.
   - `02-观测活动与目标` for observing targets, activity formats, and site constraints.
   - `03-望远镜赤道仪与拍摄前期` for equipment, setup, tracking, exposure, and checklists.
   - `04-天文摄影后期与实验数据` for image processing, raw data, stacking, denoising, and visual demos.
   - `05-样例照片与素材` for visible examples and image assets.
   - `06-题库与科普问答` for QA, games, knowledge graphs, and public-facing interaction.
4. Generate ideas as project seeds, not sequential onboarding plans. Each seed should include:
   - `核心问题`: the interesting astronomy or event problem.
   - `可用素材`: specific local paths or folders.
   - `黑客松 demo`: a buildable prototype in one sentence.
   - `agent/AI 角度`: where an agent, model, parser, recommender, or UI assistant helps.
   - `验证方式`: how to prove it works with local files, a smoke test, or live data.
5. Rank ideas by fit for the current event only after the idea pool exists. Use "high signal / medium signal / risky but interesting" rather than generic priority labels.

## Grounding Rules

- Do not frame the repository as a participant curriculum or a start-to-finish path.
- Do not treat historical meteor shower calendars, comet tables, or old activity notes as current sky schedules. If a project depends on current dates, ephemerides, weather, object visibility, software versions, or laws, verify with live sources.
- Do not recommend old installers, cracks, keygens, or unsafe binaries as build dependencies.
- Preserve original filenames when citing evidence, even if a historical title contains words like `学习`.
- Prefer project language: `素材`, `语境`, `项目种子`, `demo`, `观测任务`, `数据产品`, `agent flow`.

## Output Shape

For broad brainstorming, produce:

1. A one-paragraph framing of the event opportunity.
2. A table of 8-12 project seeds using the fields above.
3. A short "best first demos" section with 3 strongest builds and why.
4. A "needs live verification" section for ideas that depend on current sky or current tools.

For a single project direction, produce a tighter plan: target user, core flow, source files, data extraction needs, demo scope, validation checklist, and one stretch path.
