---
type: pattern-block
scenario: campaign-report
status: shipped
based_on: examples/vibe-view-campaign-report/PATTERN-block-enriched-v1.md
covers: §11 archetype library · §12 composition rhythm · §13 section anatomy · §16 additions
---

# PATTERN · campaign-report

> Page-skeleton spec for the campaign-report scenario. Internal planning document — assembles into Design Prompt §11–§13 + §16 (host file numbering wins). Style layer owns colour, weight, radius, motion. This file owns layout logic only.

A campaign report is the periodic, data-supported retelling of one campaign, product launch, period, or fiscal slice. Its job is to anchor a single primary metric, then walk the reader through evidence chapters and exit on a quiet, attributed close. Sparse data shrinks the page. Dense data extends it. Never pad.

---

## 11. Section Archetype Library

A section is composed from three independent choices: an **archetype** (what the section says), a **composition treatment** (how it is laid out), and a **dominant move** (the one element that leads the eye). Archetype and treatment are decoupled — the same archetype can take different treatments across a page, and that is where layout variety comes from. Treatment selection follows the archetype's allowed list, the item count, and the adjacency rules in §12 — not designer whim.

### 11.1 Composition Treatments

| Treatment | Composition logic | Density |
|-----------|-------------------|---------|
| **Full-bleed Monolith** | One element fills the frame, vertically centered; supporting elements stack around it. | spacious |
| **Asymmetric Split** | Two unequal columns (~3:2 or 2:1). One column leads; the other carries supporting evidence or annotation. | medium |
| **Stacked Band** | Full-width horizontal bands stacked vertically; each band is one sub-claim. | medium–dense |
| **Matrix Grid** | Equal-size cells in an N×M grid. Narratively bound — every cell is evidence for one section claim, not a free-standing tile stack. | dense |
| **Proportion Rail** | One continuous rail, band, or scale carrying a parts-of-whole reading. | medium |
| **Offset Frame** | Content deliberately cropped, off-center, or breaking a frame edge. | medium |
| **Sequence Track** | A linear stepped progression; each step is index → title → note. | medium–dense |
| **Typographic Field** | Composition built from type alone — scale, weight, and spacing do the work, with no panels or cards. | spacious–medium |
| **Annotation Rail** | A main element paired with a narrow margin of notes or callouts. | medium |

### 11.2 Dominant Move

Each section leads with exactly one dominant move — the element that takes the eye first. Moves are either **steady** or **disruptive**; the page-level budget for disruptive moves is set in §12.

| Dominant Move | Class |
|---------------|-------|
| Scale jump — the focal element is ≥ 2 scale tiers larger than its surroundings | steady |
| Single stroke — one drawn line, accent stroke, or light cone leads the eye | steady |
| Path reveal — a curve draws in, or a proportion rail fills | steady |
| Crop / bleed — the focal element is cropped by an edge or overflows the frame | disruptive |
| Offset placement — the focal element sits deliberately off the regular grid position | disruptive |
| Column break — one element spans columns or goes full-width, interrupting the grid | disruptive |

### 11.3 Archetypes

Archetype names are internal planning labels — visible eyebrows, captions, and chapter titles always come from the topic, period, data role, or business meaning, never from archetype names.

**Hero Monolith** — Trigger: opening anchor metric. Slots: eyebrow · metric-label · primary-value · unit-text · delta-indicator · subtitle. Treatments: Full-bleed Monolith (default) · Offset Frame · Typographic Field. Dominant Move: scale jump · crop/bleed · single stroke.

**Time Series** — Trigger: ordered values over a time dimension. Slots: title · time-axis · value-axis · series (1–3) · callout. Treatments: Stacked Band (default) · Asymmetric Split · Annotation Rail. Dominant Move: path reveal · scale jump on the peak point.

**Proportion Field** — Trigger: parts-of-whole as percentages. Slots: proportion-visual · focal-value · integrated labels (2–5) · note. Treatments: Proportion Rail (default) · Stacked Band · Typographic Field. Dominant Move: path reveal (rail fill) · scale jump. Donut, pie, and ring charts are not used — proportion reads as a continuous rail or band.

**Comparison** — Trigger: two metrics contrasted. Slots: left-value · left-label · right-value · right-label · divider · delta. Treatments: Asymmetric Split (default, weighted toward the leading value) · Stacked Band · Offset Frame. Dominant Move: scale jump · offset placement.

**Ranking / List** — Trigger: items ordered by magnitude. Slots: rank · label · value · delta · highlight (top 1–3). Treatments: Stacked Band (default, ≤ 5 items) · Matrix Grid (≥ 6 items, truncated past a readable count) · Asymmetric Split (top-1 isolated). Dominant Move: scale jump on top-1 · offset placement · single stroke as a magnitude scale.

**Grouped Metric Cluster** — Trigger: parallel metrics that together evidence one claim — for example a scenario's sub-metrics. Slots: cluster-claim · metric cells (2–6, each: label · value · note). Treatments: Matrix Grid (default) · Stacked Band. Dominant Move: scale jump · single stroke. Narratively bound — one claim's evidence, not a free-standing dashboard tile stack.

**Sequence / Timeline** — Trigger: time-ordered events, milestones, or a process — distinct from Time Series, which carries values, not events. Slots: track · steps (each: index · title · note) · terminus. Treatments: Sequence Track (default) · Stacked Band. Dominant Move: path reveal · single stroke.

**Peer Set / Catalog** — Trigger: a set of same-kind peers shown together without a magnitude order — a product family, a set of brands. Slots: set-label · peer cells (each: name · attribute · optional value). Treatments: Matrix Grid (default) · Stacked Band · Asymmetric Split (one peer featured). Dominant Move: scale jump on a featured peer · crop/bleed.

**Quote Interstitial** — Trigger: a narrative pause between data sections. Slots: mark · text · attribution. Treatments: Typographic Field (default) · Offset Frame. Dominant Move: column break · offset placement. Quote text is one sentence, 28 words or fewer.

**Outro Reverent** — Trigger: end of report. Slots: title · subtitle · flourish · statistical caveats (period, source, audit note where relevant). Treatments: Full-bleed Monolith (default) · Typographic Field. Dominant Move: single stroke · scale jump.

---

## 12. Composition

Default sequence: **Hero Monolith → 3–7 data-supported evidence chapters → optional Quote Interstitial → Outro Reverent**.

Section count is governed by data, not by template. Sparse datasets may produce Hero plus 1–2 evidence chapters and an Outro. Dense datasets stretch to 8–10 sections. Stop before a section becomes filler; omit archetypes whose data is absent.

### 12.1 Chapter cadence

| Chapter slot | Required | Notes |
|---|---|---|
| 1 · Hero Monolith | required | Anchors the primary value. Omit only if no primary value resolves. |
| 2–N · Evidence chapters | 2–8, data-driven | Each chapter picks one archetype + one treatment + one dominant move. Order follows narrative arc (overview → breakdown → comparison → context), not archetype enum order. |
| Quote Interstitial | optional, ≤ 1 per page | Inserted between two data-dense chapters as a breath. Skip on sparse pages. |
| Last · Outro Reverent | required | Closes with topic, period, source, caveats. |

### 12.2 Rhythm discipline

Four rules, all countable for self-check after generation:

1. **Density rotation** — every section is classified `dense` (≥ 6 atomic elements), `medium` (3–5), or `spacious` (≤ 2). Adjacent sections differ in density; no two consecutive `dense` sections; a page uses all three tiers across its length.
2. **Treatment variety** — no two consecutive sections use the same composition treatment, and no two consecutive sections use the same archetype.
3. **Bold-move budget** — each section leads with exactly one dominant move. Disruptive moves (crop/bleed, offset placement, column break) stay near one in five sections; the rest lead with a steady move.
4. **Break cadence** — at least one section per page breaks the grid — a Full-bleed Monolith, an Offset Frame, or a Typographic Field. A page made only of regular grids and stacked bands reads as a template.

### 12.3 Other composition rules

Background rhythm: vary rhythm with composition, linework, and light placement rather than deep section colour bands.

Chapter markers: sequential 01, 02, 03 when useful. Markers are optional and vary by composition — side note, tick mark, rail label, divider number, or small stamp. **Don't** repeat the same circular stamp treatment across every chapter.

---

## 13. Section Anatomy

### 13.1 Hero Monolith

Focal: primary-value — the numeric value itself, rendered as the single largest element in the Hero at Display Number scale (per the style layer) and animated with the count-up roll. Secondary: delta-indicator, subtitle. Tertiary: eyebrow, metric-label, unit-text. The metric-label and the unit-text are supporting elements — never rendered at Display Number or Section scale, never larger than the primary-value.

Hero background field: a full-bleed shader or static layer per the style layer. The Hero background is the shader only — do not place raster images or photographs in the Hero unless the brief explicitly requests imagery.

Hero composition: the primary number interacts with at least one structural element from its treatment — a cropped edge, a spotlight cone, a stage horizon, an offset frame, or a data path. Avoid the plain centered big-number Hero made only from eyebrow, number, badge, and paragraph.

Primary-value selection — pick exactly one numeric value to headline the report. Resolve by field-name pattern, stopping at the first match:

1. **Rate / percentage field** — a field whose display name contains a percent or rate indicator. Show the average across all records.
2. **Explicit aggregate field** — a field whose display name is an aggregate keyword (total, aggregate, 总计, 合计). Show its sum.
3. **Primary metric field (max)** — otherwise, identify the primary metric field by name semantics (revenue, GMV, score). Show its maximum.
4. **Primary metric field (avg)** — same field as rule 3, show the average instead.

Display the selected value directly. Preserve units and percent signs already in the source. If the selected value is missing or null, omit the Hero Monolith section entirely.

Eyebrow slot format: `{topic} · {period}`. Emit the actual period from data context; if period is unavailable, omit the period segment — do not emit placeholder strings.

### 13.2 Non-Hero archetypes — slot mapping per treatment

For every section, the first slot is focal, the second is supporting evidence, labels and notes are tertiary. The table gives focal and secondary placement for the principal archetype × treatment combinations; combinations not listed follow the same logic from the treatment's structure in §11.1.

| Archetype × Treatment | Focal placement | Secondary placement | Favored move |
|-----------------------|-----------------|---------------------|--------------|
| Time Series · Stacked Band | chart fills the upper band | callout in the lower band | path reveal |
| Time Series · Asymmetric Split | chart in the wide column | reading + callout in the narrow column | path reveal |
| Proportion Field · Proportion Rail | the rail spans the section width | focal-value at the rail's dominant segment | path reveal |
| Proportion Field · Stacked Band | each band one proportion segment | integrated labels inline per band | scale jump |
| Comparison · Asymmetric Split | leading value in the wide column | trailing value + delta in the narrow column | scale jump |
| Comparison · Stacked Band | upper band the leading value | lower band the trailing value, divider between | offset placement |
| Ranking · Stacked Band | top-1 row, emphasized | rows 2–5 descending | scale jump on top-1 |
| Ranking · Matrix Grid | top-1 cell, emphasized | remaining cells in reading order | offset placement |
| Ranking · Asymmetric Split | top-1 isolated in the wide column | rest compressed in the narrow column | scale jump |
| Grouped Metric Cluster · Matrix Grid | the cluster-claim above the grid | metric cells equal-weight, one cell may lead | scale jump |
| Grouped Metric Cluster · Stacked Band | cluster-claim leads | metric bands stacked below | single stroke |
| Sequence / Timeline · Sequence Track | the track line | steps along it, index → title → note | path reveal |
| Peer Set / Catalog · Matrix Grid | set-label above the grid | peer cells equal-weight | scale jump on a featured peer |
| Peer Set / Catalog · Asymmetric Split | featured peer in the wide column | remaining peers in the narrow column | crop/bleed |
| Quote Interstitial · Typographic Field | the quote text, set large | mark and attribution flank it | column break |
| Outro Reverent · Full-bleed Monolith | the closing title, centered | subtitle and caveats below | single stroke |

---

## 16. Do's and Don'ts — additions

These join the existing §16 list in the host Design Prompt.

- **Don't** use the same composition treatment in two consecutive sections — vary the treatment, not only the archetype.
- **Don't** keep a whole page at `medium` density — without a compression-and-breath rhythm the page reads flat.
- **Don't** build a page with zero break sections — at least one section breaks the grid (Full-bleed, Offset Frame, or Typographic Field).
- **Don't** give every section a heading — space and rhythm can carry a content shift without a label.
- **Don't** ship a perfectly symmetric layout with no visual tension — alternating density reads as intentional.
- **Don't** lead a section with more than one dominant move — the protagonist is singular.
- **Don't** render a Matrix Grid or Grouped Metric Cluster that is not narratively bound — a grid of cells is valid only as one claim's evidence, never as a page-wide parallel tile stack.
- **Don't** pad to hit a section target — sparse data deserves a sparse page; a 4-section campaign report is honest.
