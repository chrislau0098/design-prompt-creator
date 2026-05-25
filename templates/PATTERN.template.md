---
type: pattern-block
project: "{{project}}"
scenario: "{{scenario}}"
phase: "{{phase}}"
created: "{{created}}"
status: draft
---

# PATTERN Block · {{scenario}}

> Internal planning document. Do not include in final Design Prompt as-is.
> Assemble into Design Prompt §11–§13 + §16. Section numbers follow the host file.

---

## 11. Section Archetype Library

A section is composed from three independent choices: an **archetype** (what the section says), a **composition treatment** (how it is laid out), and a **dominant move** (the one element that leads the eye). Archetype and treatment are decoupled — the same archetype can take different treatments across a page, and that is where layout variety comes from. Treatment selection is rule-driven: it follows the archetype's allowed list, the item count, and the adjacency rules in §12.

### 11.1 Composition Treatments

| Treatment | Composition logic | Density |
|-----------|-------------------|---------|
| **Full-bleed Monolith** | One element fills the frame, vertically centered; supporting elements stack around it. | spacious |
| **Asymmetric Split** | Two unequal columns (roughly 3:2 or 2:1). One column leads; the other carries supporting evidence or annotation. | medium |
| **Stacked Band** | Full-width horizontal bands stacked vertically; each band is one sub-claim. | medium–dense |
| **Matrix Grid** | Equal-size cells in an N×M grid. Narratively bound — every cell is evidence for this section's single claim, not a free-standing tile stack. | dense |
| **Proportion Rail** | One continuous rail, band, or scale carrying a parts-of-whole reading. | medium |
| **Offset Frame** | Content deliberately cropped, off-center, or breaking a frame edge. | medium |
| **Sequence Track** | A linear stepped progression; each step is index → title → note. | medium–dense |
| **Typographic Field** | Composition built from type alone — scale, weight, and spacing do the work, with no panels or cards. | spacious–medium |
| **Annotation Rail** | A main element paired with a narrow margin of notes or callouts. | medium |

Favored treatments for {{scenario}}: <!-- fill per scenario evidence -->

### 11.2 Dominant Move

Each section leads with exactly one dominant move — the element that takes the eye first. Moves are either **steady** or **disruptive**; the page-level budget for disruptive moves is set in §12.

| Dominant Move | Class |
|---------------|-------|
| Scale jump — focal element ≥ 2 scale tiers larger than surroundings | steady |
| Single stroke — one drawn line, accent stroke, or light cone leads the eye | steady |
| Path reveal — a curve draws in, or a proportion rail fills | steady |
| Crop / bleed — focal element cropped by an edge or overflowing the frame | disruptive |
| Offset placement — focal element sits deliberately off the regular grid position | disruptive |
| Column break — one element spans columns or goes full-width, interrupting the grid | disruptive |

### 11.3 Archetypes

Archetype names are internal planning labels. Visible eyebrows, captions, and labels come from the topic, period, data role, or business meaning — never from archetype names.

**Hero Monolith** — Trigger: opening anchor metric. Slots: eyebrow · metric-label · primary-value · unit-text · delta-indicator · subtitle. Treatments: Full-bleed Monolith (default) · Offset Frame · Typographic Field. Dominant Move: scale jump · crop/bleed · single stroke.

**Time Series** — Trigger: ordered values over a time dimension. Slots: title · time-axis · value-axis · series (1–3) · callout. Treatments: Stacked Band (default) · Asymmetric Split · Annotation Rail. Dominant Move: path reveal · scale jump on the peak point.

**Proportion Field** — Trigger: parts-of-whole as percentages. Slots: proportion-visual · focal-value · integrated labels (2–5) · note. Treatments: Proportion Rail (default) · Stacked Band · Typographic Field. Dominant Move: path reveal (rail fill) · scale jump. Donut/pie/ring not used.

**Comparison** — Trigger: two metrics contrasted. Slots: left-value · left-label · right-value · right-label · divider · delta. Treatments: Asymmetric Split (default, weighted toward leading value) · Stacked Band · Offset Frame. Dominant Move: scale jump · offset placement.

**Ranking / List** — Trigger: items ordered by magnitude. Slots: rank · label · value · delta · highlight (top 1–3). Treatments: Stacked Band (default, ≤ 5 items) · Matrix Grid (≥ 6 items) · Asymmetric Split (top-1 isolated). Dominant Move: scale jump on top-1 · offset placement · single stroke as a magnitude scale.

**Grouped Metric Cluster** — Trigger: parallel metrics that together evidence one claim. Slots: cluster-claim · metric cells (2–6, each: label · value · note). Treatments: Matrix Grid (default) · Stacked Band. Dominant Move: scale jump · single stroke. Narratively bound — one claim's evidence, not a free-standing tile stack.

**Sequence / Timeline** — Trigger: time-ordered events, milestones, or a process. Slots: track · steps (each: index · title · note) · terminus. Treatments: Sequence Track (default) · Stacked Band. Dominant Move: path reveal · single stroke.

**Peer Set / Catalog** — Trigger: same-kind peers shown together without magnitude order. Slots: set-label · peer cells (each: name · attribute · optional value). Treatments: Matrix Grid (default) · Stacked Band · Asymmetric Split (one peer featured). Dominant Move: scale jump on a featured peer · crop/bleed.

**Quote Interstitial** — Trigger: a narrative pause between data sections. Slots: mark · text · attribution. Treatments: Typographic Field (default) · Offset Frame. Dominant Move: column break · offset placement. One sentence, 28 words or fewer.

**Outro Reverent** — Trigger: end of report. Slots: title · subtitle · flourish · statistical caveats. Treatments: Full-bleed Monolith (default) · Typographic Field. Dominant Move: single stroke · scale jump.

<!-- Scenario-specific archetypes for {{scenario}} — add below if needed -->

---

## 12. Composition

Default sequence: Hero Monolith → data-supported evidence chapters → optional Outro Reverent.

Section count: use as many sections as the data and business story support. Stop before a section becomes filler. Omit archetypes whose data is absent.

### 12.1 Rhythm discipline

Four rules, all countable for self-check after generation:

1. **Density rotation** — adjacent sections differ in density; no two consecutive `dense` sections; the page uses all three tiers (dense / medium / spacious) across its length.
2. **Treatment variety** — no two consecutive sections use the same composition treatment, and no two consecutive sections use the same archetype.
3. **Bold-move budget** — each section leads with exactly one dominant move. Disruptive moves stay near one in five sections; the rest lead with a steady move.
4. **Break cadence** — at least one section per page breaks the grid (Full-bleed Monolith, Offset Frame, or Typographic Field).

### 12.2 Other composition rules

Background rhythm: vary rhythm with composition, linework, and accent placement — not deep section color bands.

Chapter markers: sequential 01, 02, 03 when useful. Markers are optional and vary by composition — side note, tick mark, rail label, or divider number. Do not repeat the same marker treatment across every chapter.

---

## 13. Section Anatomy

### 13.1 Hero Monolith

Focal: primary-value — the numeric value itself, rendered as the single largest element in the Hero at Display Number scale, animated with count-up roll. Secondary: delta-indicator, subtitle. Tertiary: eyebrow, metric-label, unit-text.

Hero background field: a full-bleed shader or static CSS layer, per the style layer. Do not place raster images or photographs in the Hero unless the user explicitly requests imagery.

Primary-value selection — pick exactly one numeric value, resolving in priority order:
1. Rate / percentage field — show average.
2. Explicit aggregate field (total, aggregate) — show sum.
3. Primary metric field — show maximum.
4. Primary metric field — show average as fallback.

Eyebrow format: `{topic} · {period}`. Omit period segment if unavailable — do not emit placeholder strings.

### 13.2 Non-Hero archetypes — slot mapping per treatment

| Archetype × Treatment | Focal placement | Secondary placement | Favored move |
|-----------------------|-----------------|---------------------|--------------|
| Time Series · Stacked Band | chart fills the upper band | callout in the lower band | path reveal |
| Time Series · Asymmetric Split | chart in the wide column | reading + callout in the narrow column | path reveal |
| Proportion Field · Proportion Rail | rail spans the section width | focal-value at the dominant segment | path reveal |
| Comparison · Asymmetric Split | leading value in the wide column | trailing value + delta in the narrow column | scale jump |
| Ranking · Stacked Band | top-1 row, emphasized | rows 2–5 descending | scale jump on top-1 |
| Grouped Metric Cluster · Matrix Grid | cluster-claim above the grid | metric cells equal-weight | scale jump |
| Sequence / Timeline · Sequence Track | the track line | steps along it, index → title → note | path reveal |
| Quote Interstitial · Typographic Field | quote text, set large | mark and attribution flank it | column break |
| Outro Reverent · Full-bleed Monolith | closing title, centered | subtitle and caveats below | single stroke |

<!-- Scenario-specific rows for {{scenario}} — add below -->

---

## 16. Do's and Don'ts additions

- **Don't** use the same composition treatment in two consecutive sections.
- **Don't** keep a whole page at `medium` density — without compression-and-breath rhythm the page reads flat.
- **Don't** build a page with zero break sections — at least one section breaks the grid.
- **Don't** give every section a heading — space and rhythm can carry a content shift without a label.
- **Don't** ship a perfectly symmetric layout with no visual tension.
- **Don't** lead a section with more than one dominant move — the protagonist is singular.
- **Don't** render a Matrix Grid or Grouped Metric Cluster that is not narratively bound.

<!-- Scenario-specific don'ts for {{scenario}} — add below -->
