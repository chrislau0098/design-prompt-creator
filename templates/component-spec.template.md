---
type: component-spec
project: "{{project_name}}"
scenario: "{{scenario}}"
created: "{{YYYY-MM-DD}}"
status: draft
---

# Component Spec · {{scenario}}

> Internal reference for the renderer. Lists every component expected in {{scenario}}.
> Update whenever a new component is added or an existing one is renamed.

---

## Required Components (every {{scenario}} page)

### Hero

**Purpose**: Opening anchor; carries the primary-value Display Number + eyebrow + subtitle.

**Props**:
- `eyebrow: string` — `{topic} · {period}`
- `displayValue: string` — formatted focal number from Bitable (pass through `parseDisplayValue()`)
- `delta?: string` — delta indicator, optional
- `subtitle?: string`

**DOM structure**:
```
section[data-archetype="hero"]
  div.hero-inner
    p.eyebrow
    h1.page-title (optional)
    div.focal-block
      AnimateNumber (Display Number scale)
      span.unit (if unit exists)
    p.delta-indicator (optional)
    p.subtitle (optional)
  [HeroShader | StaticCSSBackground] (position absolute, z-index 0)
```

**Visual variants**: Full-bleed Monolith · Asymmetric Split · Typographic Field (controlled by `molecular.hero_geometry.default_treatment` in Slot)

**Adaptive states**:
- loading: render zeros in AnimateNumber; shader animates
- empty (no primary value): omit Hero section entirely
- error: omit Hero section entirely; do not render broken placeholder

---

### ChapterOpener

**Purpose**: Opens each non-Hero chapter with the style layer's declarative chapter-opener component (ChapterBanner / ChapterStamp / SealStamp / ChapterNumeralLarge).

**Props**:
- `index: string` — zero-padded chapter number, e.g. `"01"`
- `title: string` — chapter claim-line

**DOM structure** (varies by `decorative_pack` in Slot — fill per scenario):
```
<!-- systematic pack -->
div.chapter-opener
  Badge[variant="outline"].chapter-index (mono ALL-CAPS)
  h2.chapter-title (sans 700 ALL-CAPS)
  ShadSeparator (full-width)

<!-- editorial pack -->
div.chapter-opener
  span.chapter-kicker (mono accent, small)
  h2.chapter-title
  hr.hairline-banner
```

**Visual variants**: controlled by `style_meta.decorative_pack` in Slot

**Adaptive states**:
- all states: always rendered; title falls back to generic label if data empty

---

### KPICell

**Purpose**: One metric cell inside a Grouped Metric Cluster (Matrix Grid).

**Props**:
- `label: string`
- `value: string` — formatted; pass through `parseDisplayValue()`
- `note?: string`

**DOM structure**:
```
div.kpi-cell[bg-surface-l2, card-chrome-radius, p-6]
  p.eyebrow (label)
  div.focal-block
    AnimateNumber (Section Primary scale)
    span.unit (optional)
  p.note.mt-auto (optional)
```

**Visual variants**: default card · leading card (Display Number scale, prominent)

**Adaptive states**:
- loading: AnimateNumber at 0
- empty value: render "—" in foreground-3, no AnimateNumber
- error: render "—"

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
      AreaChart | LineChart (bare recharts, no recharts styles)
  div.callout-band (optional, lower band in Stacked Band treatment)
```

**Visual variants**: Stacked Band (default) · Asymmetric Split (chart + reading column)

**Adaptive states**:
- loading: chart renders with skeleton data (flat line)
- empty: render empty-state message at Section Secondary scale
- error: render error-state message

---

### ContentDivider

**Purpose**: In-chapter rest divider; sparingly used.

**Props**: none (inherits from Slot `molecular.dividers.content_divider`)

**DOM structure** (varies by pack):
```
<!-- alpha-hairline -->
hr[h-px, oklch-border-alpha]

<!-- hairline-dotdotdot -->
div.divider
  hr[1px border-t]
  span.dots (· · ·, mono, foreground-3, tracking-[0.8em])
```

**Adaptive states**: always rendered as-is

---

## Optional Components (scenario-dependent)

### {{OptionalComponent1}}

**Purpose**: {{description}}
**When to include**: {{condition}}
**Props**: {{prop list}}

---

## Banned Components

The following component patterns are **not used** in {{scenario}}:

- Donut / Pie / Ring charts — use Proportion Rail instead
- Frosted-glass panels (`backdrop-blur`) — use surface token depth
- Raster-image Hero backgrounds — shader or static CSS only
- `<tooltip>` from recharts library directly — use custom `<ChartTooltipCard>` or `contentStyle`
- `rounded-xl` / `rounded-2xl` / `rounded-3xl` card chrome — use `sharp_panel_max_px` from Slot

<!-- Scenario-specific bans for {{scenario}} — add below -->
