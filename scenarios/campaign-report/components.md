---
type: component-spec
scenario: campaign-report
status: shipped
---

# Component Spec · campaign-report

> The complete list of components the weak model may render for a campaign-report page. Update whenever a new component is added or an existing one is renamed.

**Three-library limit**: every component composes from **shadcn/ui** (chrome, structure), **motion** (entry, count-up, hover transitions), and **paper-shaders** (Hero or quote background fields only). No other UI library is introduced. Charts use **recharts** as a raw rendering primitive — recharts default styles are stripped and replaced by Slot tokens.

---

## Required Components (every campaign-report page)

### Hero

**Purpose**: Opening anchor. Carries the primary-value Display Number, eyebrow, and subtitle. Sets the page's emotional tone via the shader / background field.

**Props**:
- `eyebrow: string` — `{topic} · {period}`
- `displayValue: string` — formatted focal number from data source (pass through `parseDisplayValue()`)
- `unit?: string` — separate from `displayValue` so unit can render at unit-text scale
- `delta?: string` — delta indicator, optional
- `subtitle?: string`

**DOM structure**:
```
section[data-archetype="hero"]
  div.hero-inner
    p.eyebrow
    h1.page-title (optional, ALL CAPS, style-dependent)
    div.focal-block
      AnimateNumber (Display Number scale, count-up)
      span.unit
    p.delta-indicator (optional)
    p.subtitle (optional)
  [HeroShader | StaticBackground] (position absolute, z-index 0)
```

**Visual variants**: Full-bleed Monolith (default) · Offset Frame · Typographic Field. Controlled by `molecular.hero_geometry.default_treatment` in Slot.

**Adaptive states**: loading — render zeros in AnimateNumber, shader animates; empty (no primary value resolved) — omit Hero entirely; error — omit Hero entirely.

---

### ChapterOpener

**Purpose**: Opens each non-Hero chapter. Renders the chapter index, claim-line title, and a separator per the style layer's `decorative_pack`.

**Props**:
- `index: string` — zero-padded chapter number, e.g. `"01"`
- `title: string` — chapter claim-line, plain language

**DOM structure** varies by `style_meta.decorative_pack` in Slot (systematic / editorial / instrumental / theatrical / festive). One ChapterOpener per chapter; never inside the Hero.

**Adaptive states**: always rendered; title falls back to a generic label if the data context is missing.

---

### KPICell

**Purpose**: One metric cell inside a Grouped Metric Cluster (Matrix Grid).

**Props**:
- `label: string`
- `value: string` — formatted; pass through `parseDisplayValue()`
- `unit?: string`
- `note?: string`

**DOM structure**:
```
div.kpi-cell
  p.eyebrow (label, mono or sans per pack)
  div.focal-block
    AnimateNumber (Section Primary scale, count-up)
    span.unit
  p.note.mt-auto (optional)
```

**Visual variants**: default cell · leading cell (Display Number scale, one per cluster, highlights the strongest claim).

**Adaptive states**: loading — AnimateNumber at 0; empty value — render `—` in foreground-3, no AnimateNumber; error — render `—`.

---

### TimeSeriesChart

**Purpose**: Area or line chart for Time Series sections.

**Props**:
- `data: Array<{ period: string; value: number }>`
- `seriesKey: string`
- `callout?: string`

**DOM structure**:
```
section[data-archetype="time-series"]
  div.chart-region
    ResponsiveContainer
      AreaChart | LineChart (bare recharts, no recharts default styles)
  div.callout-band (optional, lower band in Stacked Band treatment)
```

**Visual variants**: Stacked Band (default) · Asymmetric Split (chart in wide column, reading column on side).

**Adaptive states**: loading — flat skeleton line; empty — empty-state message at Section Secondary scale; error — error-state message.

---

### TimelineNode

**Purpose**: One step inside a Sequence Track.

**Props**:
- `index: string`
- `title: string`
- `note?: string`
- `terminus?: boolean` — marks the final step

**DOM structure**:
```
li.timeline-step
  span.step-index (mono, ALL CAPS where pack allows)
  div.step-body
    h3.step-title
    p.step-note (optional)
```

**Visual variants**: in-track node · terminus node (slightly emphasized).

**Adaptive states**: empty title — skip the step entirely, do not render a placeholder.

---

### CompareGroup

**Purpose**: Two-metric Comparison archetype.

**Props**:
- `left: { label: string; value: string; unit?: string }`
- `right: { label: string; value: string; unit?: string }`
- `delta?: string`

**DOM structure**:
```
section[data-archetype="comparison"]
  div.compare-left (wide column in Asymmetric Split)
    p.label
    AnimateNumber (Section Primary scale)
  div.divider (single stroke or hairline, per pack)
  div.compare-right (narrow column)
    p.label
    AnimateNumber (Section Secondary scale)
  p.delta (optional)
```

**Visual variants**: Asymmetric Split (default, weighted toward leading value) · Stacked Band · Offset Frame.

**Adaptive states**: missing one side — collapse to single-metric Hero-style focal block, do not render `—` opposite a real value.

---

### RankingList

**Purpose**: Ranking / List archetype.

**Props**:
- `items: Array<{ rank: number; label: string; value: string; delta?: string; highlight?: boolean }>`

**DOM structure**:
```
section[data-archetype="ranking"]
  ol.ranking-list
    li.ranking-row[data-highlight="true|false"]
      span.rank
      span.label
      AnimateNumber (Section Secondary scale)
      span.delta (optional)
```

**Visual variants**: Stacked Band (default, ≤ 5 items) · Matrix Grid (≥ 6 items) · Asymmetric Split (top-1 isolated).

**Adaptive states**: < 2 items — render as a single CompareGroup or Hero supplement instead; empty — omit section.

---

### ProportionRing

**Purpose**: Proportion Field archetype focal element. Despite the name, renders as a Proportion Rail or Stacked Band — **never** a donut, pie, or ring chart (those are banned, see below).

**Props**:
- `segments: Array<{ label: string; percent: number; highlight?: boolean }>`
- `focalValue: string` — the dominant segment's value, called out at scale

**DOM structure**:
```
section[data-archetype="proportion"]
  div.proportion-rail (horizontal continuous bar, segments inline)
    div.segment[data-highlight] (one per segment)
  div.focal-readout
    AnimateNumber (Section Primary scale)
    p.note
```

**Visual variants**: Proportion Rail (default) · Stacked Band · Typographic Field.

**Adaptive states**: 1 segment — degenerates to a focal-value block, no rail; empty — omit section.

---

### Annotation

**Purpose**: Margin notes paired with another archetype via the Annotation Rail treatment.

**Props**:
- `text: string`
- `target?: string` — optional pointer to the element the note describes

**DOM structure**:
```
aside.annotation
  span.marker (small index or tick, mono)
  p.note
```

**Adaptive states**: empty text — omit; rendered only when its target is visible.

---

### QuoteBlock

**Purpose**: Quote Interstitial archetype.

**Props**:
- `text: string` — one sentence, ≤ 28 words
- `attribution?: string`

**DOM structure**:
```
section[data-archetype="quote"]
  span.quote-mark (large, decorative)
  blockquote.quote-text (Typographic Field, scale jump)
  cite.attribution (small, mono)
  [QuoteShader] (optional, per pack)
```

**Adaptive states**: text > 28 words — refuse to render; > 1 sentence — refuse to render. Truncation is not allowed; the data must be re-edited upstream.

---

### Outro

**Purpose**: Outro Reverent — the closing section.

**Props**:
- `title: string` — closing claim, plain language
- `subtitle?: string`
- `caveats: Array<string>` — period, source, audit notes

**DOM structure**:
```
section[data-archetype="outro"]
  div.outro-inner
    h2.outro-title (centered, Section Primary scale)
    p.outro-subtitle (optional)
    ul.caveats (mono, foreground-3)
      li (one per caveat: period / source / audit)
    span.flourish (single stroke or stamp, per pack)
```

**Visual variants**: Full-bleed Monolith (default) · Typographic Field.

**Adaptive states**: always rendered; if no caveats, omit the `ul`.

---

### ContentDivider

**Purpose**: In-chapter rest divider; sparingly used. Inherits chrome from Slot `molecular.dividers.content_divider`.

**Adaptive states**: always rendered as-is.

---

## Banned Components

The following are **not used** in campaign-report:

- Donut / Pie / Ring charts — proportion reads as a continuous rail or band; ring charts read as decoration.
- Frosted-glass panels (`backdrop-blur`) — use surface token depth instead.
- Raster-image Hero backgrounds — shader or static layer only, unless the brief explicitly requests imagery.
- recharts default tooltip — use a custom `<ChartTooltipCard>` or override `contentStyle` with Slot tokens.
- `rounded-xl` / `rounded-2xl` / `rounded-3xl` card chrome — use `sharp_panel_max_px` from Slot.
- Dashboard-style free-standing KPI tiles outside a Grouped Metric Cluster — KPI cells are narratively bound to one claim.
- Decorative dividers between every section — let composition rhythm carry the breath.
