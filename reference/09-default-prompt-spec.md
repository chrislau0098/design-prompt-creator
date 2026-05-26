# 09 · Default Prompt Spec

Internal spec for the **default** style — a parameterized base prompt that lets users / weak LLMs generate a new fixed style by choosing dial values, instead of inheriting one of the 6 fixed styles. This file is read by Cowork during Phase 2 prompt drafting and Phase 3 management registration. It is **not** the prompt itself; it is the rule source the prompt is compiled from.

Boundary: default ≠ replacement of fixed styles. Default = "style factory"; fixed = "completed recipes". Three-Way Sync invariant for default: `System ⊆ Prompt ⊆ Slot` becomes `Rendered DOM ⊆ Prompt rules ⊆ URL-query dial set`.

## Dial system

| Dial | Type | Default | Allowed values |
|------|------|---------|----------------|
| `mode` | enum | `light` | `light` / `dark` |
| `brand_color` | hex string | `#1E40AF` | any valid 6-digit hex; also accepts named presets via `?named=` |
| `lightness_shift` | int −100–+100 | `0` | negative = darker · positive = lighter; maps to ±0.15 L offset on primary |
| `font_family` | enum | `geometric` | `geometric` / `editorial` / `technical` / `warmth` / `impact` / `ceremonial` |
| `hero_shader` | enum | `mesh` | `mesh` / `grain` / `dithering` / `none` |
| `radius` | enum | `sharp` | `sharp` (0px) / `crisp` (2px) / `soft` (6px) / `friendly` (12px) / `playful` (16px) |
| `density` | enum | `balanced` | `sparse` / `balanced` / `dense` |

`neutral_temperature` removed — internal tokens always use branded chroma (C 0.008 light / 0.012 dark). No user-facing dial.
`accent_strategy` removed — always `mono` (bordered). `card_border` fixed to `bordered`.

Named color presets (`?named=<key>`): `red` `crimson` `orange` `amber` `green` `teal` `blue` `indigo` `purple` `pink` `slate` `black`. Priority: `?color=` > `?named=` > default.

## Color expansion rule (OKLCH)

Inputs: `brand_color` (hex) + `lightness_shift` (−100…+100) + `mode`. The user's hex is parsed to OKLCH (`pL`, `pC`, `pH`) and used as the **accent anchor** — `--primary` equals the user's hex with optional lightness offset. Neutrals share `pH` only (their L/C follow the standardized ramp).

### Algorithm

```
1. (pL, pC, pH) = hexToOKLCH(brand_color)
2. shift = lightness_shift / 100                  // −1.0 … +1.0
3. primaryL = clamp(pL + shift × 0.15, 0.30, 0.70)

Accent tokens (anchored to user color):
  --primary       = oklch(primaryL,                  pC,            pH)
  --primary-hl    = oklch(min(primaryL+0.10, 0.78),  pC,            pH)
  --primary-soft  = oklch(0.92,                      min(pC, 0.04), pH)
  --chart-1       = var(--primary)
  --chart-2       = oklch(primaryL + 0.07,           pC - 0.02,     pH)
  --chart-3       = oklch(primaryL - 0.03,           pC - 0.06,     pH)
  --chart-4       = oklch(primaryL - 0.13,           pC - 0.10,     pH)
  --chart-5       = oklch(primaryL - 0.23,           pC - 0.14,     pH)

Neutral tokens (L from spec ramp, hue from user color):
  --background    = oklch(0.985, neutralC, pH)
  --surface-l1    = oklch(0.985, neutralC, pH)
  --surface-l2    = oklch(0.965, neutralC, pH)
  --surface-l3    = oklch(0.935, neutralC, pH)
  --foreground    = oklch(0.14,  0.008,    pH)
  --foreground-2  = oklch(0.42,  0.008,    pH)
  --foreground-3  = oklch(0.62,  0.008,    pH)
  --border        = oklch(0.14,  0.008,    pH, 0.10)
  --border-strong = oklch(0.14,  0.008,    pH, 0.22)
  --chart-hover   = oklch(0.14,  0.008,    pH, 0.05)
```

`neutralC` always branded: 0.008 (light) / 0.012 (dark). `neutral_temperature` dial removed.

### Dark mode ramp

Same accent algorithm; neutral L flips symmetrically — background 0.10, surfaces 0.12 / 0.14 / 0.17, foregrounds 0.92 / 0.70 / 0.50. Primary lifts via the same algorithm to maintain ≥ 4.5:1 contrast against the dark background.

### Neutral hue handling (KEY)

All neutrals (surface / foreground / border / chart-hover) **share the same `pH` (brand hue) as the accent family**, but with fixed branded chroma. Rationale:

- OKLCH's L axis is perceptually uniform across hues — the same `L` value (e.g. 0.985 for background) gives the same perceived lightness whether `hue=30` (warm) or `hue=232` (cool). No hue-specific L adjustment needed.
- Letting neutrals inherit `pH` gives the gray a **subtle warmth/coolness that matches the brand** (a hue-232 cool surface vs hue-30 warm surface — both look "gray" but emotionally aligned with the brand). Pure C=0 grays look detached and clinical.
- Chroma is fixed at branded level (C 0.008 light / 0.012 dark) — no user-facing dial. This gives consistent brand cohesion across all default-style outputs while keeping neutrality readable.

### Chroma constraints (HARD)

- Neutral family (surface / foreground / border / chart-hover): C ≤ 0.008 (light mode) · C ≤ 0.012 (dark mode)
- Accent family (primary / primary-hl / primary-soft): C ∈ [0.04, 0.22]
- Chart ramp: C 0.08–0.22 (`--chart-1` highest, descending to `--chart-5`)
- Any token with C > 0.22 = violation. Regenerate.

## Font family dial

`--body-stack` separates Display from Body — each family now has an explicit body font var injected alongside `--display-stack` and `--sans-stack`.

| Family | Latin Display | 中文 Display | 中文 Body (`--body-stack`) | Scope |
|--------|---------------|--------------|----------------------------|-------|
| **geometric** *(default)* | Geist / Helvetica Neue | 思源黑体 700 (or MiSans / 鸿蒙) | 思源黑体 400 | 科技 / 通用 / 商务 / 极简 |
| **editorial** | Fraunces / Spectral | 思源宋体 700 | 思源宋体 400 (Noto Serif SC) | 文艺 / 阅读 / 杂志 |
| **technical** | JetBrains Mono / IBM Plex Mono | 思源黑体 700 + tnum | 思源黑体 400 | SaaS / fintech / 数据 |
| **warmth** | DM Sans / Outfit | 霞鹜文楷 | 思源黑体 400 | 温暖 / 教育 / 文化 |
| **impact** | Druk / Bebas Neue | 优设标题黑 or 得意黑 (Smiley Sans) | 思源黑体 400 | 运动 / 户外 / 硬核 |
| **ceremonial** | Playfair Display / Cinzel | 演示魁本楷 or 马善政毛笔 | 朱雀仿宋 / FZShuSong-Z01 / 方正书宋 | 庆典 / 国潮 / luxury |

Stack ordering rule: **中文 family first** when CJK glyph shape differs notably (warmth / editorial / ceremonial / impact). Otherwise Latin first acceptable.

Weight floor (Display): geometric 700 · editorial 700 · technical 700 · warmth 400-500 · impact 800 · ceremonial 700. Body always 400.

## Hero shader dial

| Engine | When to use | colors[] rule | Numeric param ranges |
|--------|-------------|----------------|----------------------|
| **mesh** *(MeshGradient)* | brand / luxury / editorial / calm | 4–6 colors, L 0.85–0.97, max C 0.06, ΔL ≤ 0.10 across set | distortion 0.3–1.1 · swirl 0.2–0.8 · grainMixer 0.01–0.10 · speed 0.10–0.45 |
| **grain** *(GrainGradient)* | warmth / lifestyle / texture | 2–4 base colors L 0.80–0.95 + optional 1 accent point | softness 0.4–0.8 · intensity 0.06–0.15 · speed 0.10–0.30 |
| **dithering** *(Dithering)* | systematic / technical / severe | colorFront L 0.55–0.75 neutral · colorBack L 0.92–0.97 | type `8x8`/`4x4` · shape `simplex`/`wave` · size 2–6 · scale 0.8–1.4 · speed 0.3–0.5 |
| **none** | dashboard / docs / admin / form | static CSS dot-grid or line-grid fallback | n/a |

`hero_shader` independent of `font_family`. All shaders confined to Hero section, viewport-paused (`speed: 0` off-viewport).

## Radius dial

| Token | Value | Mapped vibe |
|-------|-------|-------------|
| **sharp** *(default)* | 0px | systematic / editorial / minimal / 高级感 |
| **crisp** | 2px | instrumental / fintech / 半严肃 |
| **soft** | 6px | saas / dashboard / 中性 |
| **friendly** | 12px | consumer / lifestyle / 温暖 |
| **playful** | 16px | 节庆轻盈 / 教育 (战报场景慎用) |

ONE radius per page (existing HARD rule, no mixing).

## Density dial

| Density | Section py (lg) | Grid gap | Cols |
|---------|------------------|----------|------|
| **sparse** | 160–200px | 8–12px | 2–3 |
| **balanced** *(default)* | 96–128px | 24–32px | 3–4 |
| **dense** | 48–72px | 16–24px | 4–6 |

## Accent strategy dial

| Strategy | Rule | When |
|----------|------|------|
| **silent** | No accent. Foreground = accent. Tags filled-bg only. | luxury / editorial / minimal |
| **mono** *(default)* | One accent token (`--primary`). CTA, focal numerals, chart-1, chapter index. | most cases |
| **semantic** | Primary + success / warning / error. | dashboard / fintech only |

## Combination matrix

Recommended dial combinations (any deviation requires Chris confirmation):

| Vibe | mode | font | hero | radius | density | accent |
|------|------|------|------|--------|---------|--------|
| Generic luxury *(default of default)* | light | geometric | mesh | sharp | balanced | silent |
| Editorial calm | light | editorial | mesh | sharp | sparse | silent |
| Technical fintech | light | technical | dithering | crisp | dense | semantic |
| Warm wellness | light | warmth | grain | friendly | balanced | mono |
| Sport energy | light | impact | grain | crisp | balanced | mono |
| Ceremonial fest | light | ceremonial | mesh | sharp | sparse | mono |
| Dark dashboard | dark | technical | none | soft | dense | semantic |

Forbidden combinations (HARD):
- `impact` + `playful` radius — visual whiplash
- `editorial` + `dense` — undermines reading rhythm
- `ceremonial` + `semantic` — color budget collapse
- `technical` + `mesh` shader — readability conflict on data sections

## URL query schema

Default style is configured via URL query (no slot.json):

```
?style=default
&mode=light
&hue=232
&font=geometric
&hero=mesh
&radius=sharp
&density=balanced
```

Missing params fall back to defaults from Dial table. Invalid values rejected client-side.

## Three-Way Sync (default revision)

Standard fixed-style invariant: `System ⊆ Prompt ⊆ Slot SoT`.

Default invariant: `Rendered DOM ⊆ Prompt rules ⊆ URL-query dial set`.

- **URL query** is the SoT (replaces slot.json)
- **Prompt md** declares what each dial does
- **System view** renders one dial-set materialization at a time, regenerates on query change
- **Design Example iframe** loads `?style=default&...` and reflects current dial values

Phase 2 (prompt md) and Phase 4 (Example route) must both consume this schema.
