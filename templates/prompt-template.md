---
style_name: "{{style_meta.style_name}}"
description: "{{style_meta.proposition}}"
template_version: v0.5.2(R-94 Stage 6 three-way sync · delete TasselDivider/OutlinedPill/SpotlightGradient(theatre), Swiss ChapterStamp→ChapterBanner+ShadSeparator, drawn-horizon Hero-only note, Warm editorial banner clarify)
---

## 1. Brand & Style

Mood: **{{style_meta.mood_adjectives.0}} · {{style_meta.mood_adjectives.1}} · {{style_meta.mood_adjectives.2}} · {{style_meta.mood_adjectives.3}}**

Proposition: {{style_meta.proposition}}

## 2. Colors

Mode: {{style_meta.mode}}. Color space: OKLCH.

```css
:root {
  --brand-hue: {{style_meta.brand_hue}};
  --background:    oklch({{atomic.color.background.0}} {{atomic.color.background.1}} {{atomic.color.background.2}});
  --surface-l1:    oklch({{atomic.color.surface_l1.0}} {{atomic.color.surface_l1.1}} {{atomic.color.surface_l1.2}});
  --surface-l2:    oklch({{atomic.color.surface_l2.0}} {{atomic.color.surface_l2.1}} {{atomic.color.surface_l2.2}});
  --surface-l3:    oklch({{atomic.color.surface_l3.0}} {{atomic.color.surface_l3.1}} {{atomic.color.surface_l3.2}});
  --foreground:    oklch({{atomic.color.foreground.0}} {{atomic.color.foreground.1}} {{atomic.color.foreground.2}});
  --foreground-2:  oklch({{atomic.color.foreground_2.0}} {{atomic.color.foreground_2.1}} {{atomic.color.foreground_2.2}});
  --foreground-3:  oklch({{atomic.color.foreground_3.0}} {{atomic.color.foreground_3.1}} {{atomic.color.foreground_3.2}});
  --border:        oklch({{atomic.color.border.0}} {{atomic.color.border.1}} {{atomic.color.border.2}} / {{atomic.color.border.3}});
  --border-strong: oklch({{atomic.color.border_strong.0}} {{atomic.color.border_strong.1}} {{atomic.color.border_strong.2}} / {{atomic.color.border_strong.3}});
  --primary:       oklch({{atomic.color.primary.L}} {{atomic.color.primary.C}} var(--brand-hue));
  --primary-hl:    oklch({{atomic.color.primary_hl.L}} {{atomic.color.primary_hl.C}} var(--brand-hue));
  {{#if atomic.color.primary_soft}}--primary-soft:  oklch({{atomic.color.primary_soft.L}} {{atomic.color.primary_soft.C}} var(--brand-hue));{{/if}}
  --primary-glow:  oklch({{atomic.color.primary.L}} {{atomic.color.primary.C}} var(--brand-hue) / {{atomic.color.primary_glow_alpha}});
  --chart-1:       var(--primary);
  --chart-2:       oklch({{atomic.color.chart_ramp.0.L}} {{atomic.color.chart_ramp.0.C}} var(--brand-hue));
  --chart-3:       oklch({{atomic.color.chart_ramp.1.L}} {{atomic.color.chart_ramp.1.C}} var(--brand-hue));
  --chart-4:       oklch({{atomic.color.chart_ramp.2.L}} {{atomic.color.chart_ramp.2.C}} var(--brand-hue));
  --chart-5:       oklch({{atomic.color.chart_ramp.3.L}} {{atomic.color.chart_ramp.3.C}} var(--brand-hue));
  --chart-hover:   oklch({{atomic.color.chart_hover.0}} {{atomic.color.chart_hover.1}} {{atomic.color.chart_hover.2}} / {{atomic.color.chart_hover.3}});
  --quote-bg:      oklch({{atomic.color.surface_l2.0}} {{atomic.color.surface_l2.1}} {{atomic.color.surface_l2.2}});
  --outro-bg:      oklch({{atomic.color.background.0}} {{atomic.color.background.1}} {{atomic.color.background.2}});
  {{#if atomic.color.primary_wash}}--ember-wash:    oklch({{atomic.color.primary_wash.0}} {{atomic.color.primary_wash.1}} {{atomic.color.primary_wash.2}} / {{atomic.color.primary_wash.3}});{{/if}}
  {{#if atomic.color.ambient_ink}}--glow-ink:      oklch({{atomic.color.ambient_ink.0}} {{atomic.color.ambient_ink.1}} {{atomic.color.ambient_ink.2}} / {{atomic.color.ambient_ink.3}});{{/if}}
}
```

Color rules:
- Focal numbers use `--primary` (L {{atomic.color.primary.L}} C {{atomic.color.primary.C}}). Units, unit suffixes, percent signs, delta arrows, and delta values use `--primary-hl` (same hue, lighter L {{atomic.color.primary_hl.L}} C {{atomic.color.primary_hl.C}}).
- Charts: ordered single-hue ramp chart-1 through chart-5. Latest period carries chart-1 brand accent; prior periods step to chart-3 through chart-5. No green, blue, library-default, or Tailwind palette unless brand hue itself sits in that range. Hover/active-bar/tooltip use `--chart-hover`.
- Depth from Hero shader, chapter rhythm, typographic scale, and brand accent — not shadow-heavy cards. Borders whisper-thin; surfaces stack by ≤ one L step. **Filled cards never carry visible borders** — when a panel uses `bg-surface-l2` / `bg-surface-l3` / any non-transparent background, drop the border. Fill alone separates the panel; adding a border on top is redundant noise. Choose one: fill OR border, never both. **Heavy / dark-saturated borders only as dividers** — thick or dark borders (e.g. `1px solid var(--foreground)` on a card) overwhelm the panel and read as cheap (Chris Round-82). Reserve heavy lines for `<hr>` dividers, chapter hairlines, or section breaks — never card edges. Non-filled card borders stay at `var(--border)` whisper-thin (≤ 12% alpha). **Hero is not a chapter** — do not render `ChapterStamp` / chapter number marker / chapter kicker label inside Hero region (Chris Round-83). Hero ornament is reserved for eyebrow + Display Number + delta + lead. **Shader-induced readability issues solve at the shader source** — if Hero shader (Dithering / MeshGradient / GodRays / GrainGradient) `colorFront` is too dark / saturated and obstructs Hero text, lower the shader `colorFront` lightness or chroma directly (e.g. Swiss Dithering uses `#C8CACE` neutral light gray, not `#1E3FB0` cobalt full strength). **Never add backdrop-filter / mask / opacity overlay to cover up shader contrast** — that violates the source-fix principle (Chris Round-83).
- Brand accent 8–15% of every viewport. Reserved for: focal numerals, chart-1 latest period, Hero shader breath, chapter index numeral, one structural accent per section.
- No `#000000`. No `#FFFFFF`. Tokens only.

Brand hue: `--brand-hue` is the only accent knob. Accent tokens take hue from it; neutral tokens (backgrounds, surfaces, foregrounds, borders) fixed at hue {{atomic.color.neutral_hue}}{{#if atomic.color.foreground_hue}}; foreground prose shifts to hue {{atomic.color.foreground_hue}} for measured offset against the neutral ground{{/if}}.

{{#if style_meta.mode == "chromatic"}}**Chromatic mode**: background uses the declared `chromatic_background` OKLCH token directly as `var(--background)`; surface tokens (`surface-l1/l2/l3`) step within the chromatic hue family with ≤ 0.08 L difference (e.g. crimson `[0.42, 0.18, 25]` → `[0.38, 0.17, 25]` → `[0.34, 0.15, 25]`). Foreground uses the declared `foreground_hue` for ceremonial contrast (e.g. gold ivory `hue 80` against crimson `hue 25`). No black, no white tokens.{{/if}}

## 3. Typography

### Font loading

```css
/* {{atomic.typography.font_loading}} loading — primary {{atomic.typography.sans_stack.0}} · display {{atomic.typography.display_stack.0}} · mono {{atomic.typography.mono_stack.0}} */
```

Font stacks: Primary Sans `{{atomic.typography.sans_stack}}`; Display Number `{{atomic.typography.display_stack}}`; Mono Meta `{{atomic.typography.mono_stack}}`. {{#if style_meta.display_typeface_class == "sans"}}All sans — no serif, no italic.{{/if}}{{#if style_meta.display_typeface_class == "serif"}}All serif — Display + Hero Title + Section + Eyebrow + Body + Caption use the declared serif stack consistently. No italic posture; emphasis from scale and color only.{{/if}}

Weight: `font-normal` (400) prose · `font-medium` (500) titles, Display Number, delta value, chapter marker, unit suffix. {{#if style_meta.decorative_pack == "editorial"}}No `font-semibold`/`font-bold`/≥600 — restraint is the signature.{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}`font-semibold` (600) reserved for delta value and chapter marker numeral only. No `font-bold`/≥700.{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}`font-semibold` (600) reserved for delta indicator value and chapter marker numeral only. No `font-bold`/≥700.{{/if}}{{#if style_meta.decorative_pack == "systematic"}}`font-bold` (700) is the **Swiss / IBM signature** — Hero Display Number, Page Title, Chapter Stamp numerals all use 700. Display stack ALL-CAPS at 700 is the typographic statement. Body / Lead remains 400-500.{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}`font-bold` (700) is the **Royal serif signature** — Hero Display Number, Hero Title, Section Primary, SealStamp numerals all use 700. Body / Lead / Caption remains 400-500. No `font-extrabold`, `font-black`.{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}`font-extrabold` (800) is the **Editorial brutalist signature** — Hero Display Number, Hero Title, Section Primary, ChapterNumeralLarge all use 800 in ALL CAPS where applicable. Body / Lead / Caption remains 400-500. No `font-black`.{{/if}}

| Level | lg | mobile | Weight |
|-------|----|--------|--------|
{{#if atomic.typography.hero_title_lg}}| Hero Title | `text-[{{atomic.typography.hero_title_lg}}px]` | `text-[{{atomic.typography.hero_title_mobile}}px]` | `font-medium` |
{{/if}}{{#if atomic.typography.page_title_lg}}| Page Title | `text-[{{atomic.typography.page_title_lg}}px]` | `text-[{{atomic.typography.page_title_mobile}}px]` | `font-medium` |
{{/if}}| Display Number | `text-[{{atomic.typography.display_number_lg}}px]` | `text-[{{atomic.typography.display_number_mobile}}px]` | `font-medium` |
| Section Primary | `text-[{{atomic.typography.section_primary_lg}}px]` | — | `font-medium` |
| Section Secondary | `text-[{{atomic.typography.section_secondary_lg}}px]` | — | `font-medium` |
| Section Tertiary | `text-[{{atomic.typography.section_tertiary_lg}}px]` | — | `font-normal` |
| Quote | `text-[{{atomic.typography.quote_lg}}px]` | — | `font-normal` |
{{#if atomic.typography.lead_paragraph_lg}}| Lead Paragraph | `text-[{{atomic.typography.lead_paragraph_lg}}px]` | — | `font-normal` |
{{/if}}| Body | `text-[{{atomic.typography.body}}px]` | — | `font-normal` |
| Caption | `text-[{{atomic.typography.caption}}px]` | — | `font-normal` |
{{#if atomic.typography.unit_suffix_lg}}| Unit Suffix | `text-[{{atomic.typography.unit_suffix_lg}}px]` | — | `font-medium` |
{{/if}}| Meta/Label | `text-[{{atomic.typography.eyebrow_px}}px]` | — | `font-medium` `tracking-[{{atomic.typography.meta_tracking_em}}em]` |
| Eyebrow | `text-[{{atomic.typography.eyebrow_px}}px]` | — | `font-medium` `tracking-[{{atomic.typography.eyebrow_tracking_em}}em]` |

Display Number `leading-[{{atomic.typography.display_lh}}]` `tracking-[{{atomic.typography.display_ls_em}}em]`. Focal numbers use exact breakpoint classes (no `clamp()` — sub-pixel jitter degrades spring count-up). Floor `text-[10px]`; required reading `text-[14px]+` per §8.

Display Number anatomy: focal figure Display Number scale `--primary`; {{#if atomic.typography.unit_suffix_lg}}unit suffix inline Unit Suffix scale{{/if}}{{#if style_meta.focal_numeral_strategy == "primary_on_neutral"}} `--primary-hl`{{/if}}{{#if style_meta.focal_numeral_strategy == "primary_on_primary"}} `--primary` / `--primary-hl` mixed{{/if}}{{#if style_meta.focal_numeral_strategy == "foreground_with_primary_signal"}} `--primary` as directional signal accent{{/if}}, baseline-aligned `gap-2`. Unit ~28–30% figure height; never same scale, never above baseline, never wrapped.

OpenType: `font-feature-settings: {{atomic.typography.font_feature_settings}}` on all data numbers.

CJK: primary sans for Hero Title, Chapter Title, Body, Caption when Chinese; display stack for Display Number (Latin only); `textWrap: "balance"`; `max-w-[{{atomic.typography.cjk_body_max_ch}}ch]` body / `max-w-[{{atomic.typography.cjk_hero_max_ch}}ch]` hero; 0.1em space flanking digits in mixed lines.

{{#if atomic.typography.lead_paragraph_lg}}Lead paragraph: first paragraph each chapter at Lead Paragraph scale, `font-normal`, `--foreground-2`, max `max-w-[{{atomic.typography.cjk_body_max_ch}}ch]` CJK / `max-w-[60ch]` EN.{{/if}} Body: `text-[{{atomic.typography.body}}px]`/`text-[{{atomic.typography.caption}}px]` caption, `font-normal`, `--foreground-2` prose, `--foreground-3` only decorative.

Chapter title: claim-line (5–14 CJK / 4–9 EN words), Section Primary, `font-medium`, `--foreground`. Names the outcome; never slogan, never ALL-CAPS, never question.

Hierarchy: one Primary number per section (largest, `--primary`, `--primary-hl` on unit/delta). Tiers differ ≥ 2 steps. Emphasis from scale and color — never italic, never bold above {{atomic.typography.weight_ceiling}}.

## 4. Spacing & Layout

Base unit: {{atomic.spacing.base_px}}px. Scale: `1` `2` `3` `4` `6` `8` `12` `16` `24`{{#if atomic.spacing.scale_extra.0}} `{{atomic.spacing.scale_extra.0}}`{{/if}}. Section: `py-{{atomic.spacing.section_py_mobile}} px-6` mobile → `py-{{atomic.spacing.section_py_lg}} px-{{atomic.spacing.section_px_lg}}` desktop. Container: `{{atomic.spacing.container_max_w}}` paragraph-driven; `max-w-5xl` KPI/chart. Grid: `gap-2`, `items-baseline`, `min-w-0`.

Long-scroll cadence: chapters stack vertically, separated by hairline + accent ornament. Content determines height, `min-h-[80vh]` floor. Overflow: truncate, wrap, or scale to longest plausible value.

Density: one observation per viewport. Gaps: `gap-1` tight · `gap-3` label+number · `gap-8` paragraph→KPI · `gap-12` KPI→chart.

Radius: pill/tag: {{atomic.radius.pill}}. Sharp panel (table/chart): `rounded-[0px]`–`rounded-[{{atomic.radius.sharp_panel_max_px}}px]`. {{#if atomic.radius.card_chrome == "double-bezel"}}Card chrome: Double-Bezel (outer `{{atomic.material.double_bezel_spec.outer}}` → inner `{{atomic.material.double_bezel_spec.inner}}`).{{/if}}{{#if atomic.radius.card_chrome != "double-bezel"}}Card chrome (cluster/commitments): `rounded-[{{atomic.radius.card_chrome}}px]`.{{/if}}

KPI row: 4–6 cells, vertical hairline column rule, Display Number + unit + caption each. `px-6 py-4`; first `pl-0`. Stack below `md:` with horizontal hairline.

## 5. Material

Surface: flat ground from `var(--background)` token (no page-level shader). {{#if molecular.hero_shader}}Hero shader is the page's only WebGL layer, scoped to Hero section.{{/if}}{{#if !molecular.hero_shader}}Hero uses a static CSS background layer (dot-grid / line-grid), scoped to Hero section — no WebGL anywhere on page.{{/if}} Panels lift through hairline + one-step L difference{{#if atomic.material.shadow == "none"}}, never shadow stacks or backdrop-blur{{/if}}{{#if atomic.material.shadow == "inset-glow"}}, with inset-glow shadow on Double-Bezel cards only{{/if}}{{#if atomic.material.shadow == "inset-light"}}, with inset-light shadow on thin-border-inset cards only{{/if}}.

Borders: Whisper `1px solid var(--border)` · Strong `var(--border-strong)`. Shadow: {{atomic.material.shadow}} on cards.

{{#if molecular.hero_shader}}Shader policy: 1 WebGL instance per page (Hero only). Pauses to `speed: 0` off-viewport, returns `speed: {{molecular.hero_shader.props.speed}}` on re-enter.{{/if}}{{#if !molecular.hero_shader}}Shader policy: page has **no WebGL layer**. Hero background relies on static CSS layer (dot-grid / line-grid) plus typographic scale alone — no shader breath, no opacity drift.{{/if}}

{{#if atomic.color.primary_wash}}Brand wash: `--ember-wash` ~12–18% alpha radial gradient marks Hero focal value{{#if style_meta.decorative_pack == "editorial"}} and Outro signature only{{/if}}. Above shader, below text.{{/if}}{{#if atomic.color.ambient_ink}}Ambient ink: `--glow-ink` ~18% alpha tint overlay applied to Hero shader stack for stage-light coherence.{{/if}}

{{#if atomic.material.noise_overlay == "svg-feturbulence"}}Page-level noise: SVG `feTurbulence baseFrequency=0.65 numOctaves=3` opacity ≤ 0.12 overlay-blend, applied page-wide for fintech instrument grain.{{/if}}

{{#if style_meta.decorative_pack == "editorial"}}Chapter opener: `ChapterBanner` — `--border-strong` hairline + mono accent kicker + chapter title `--foreground` sans medium. Left-aligned, no gradient band.{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}Chapter opener: `ChapterStamp` SVG circular badge — 1.5px `--primary` border ring (40×40), mono numeral centered `font-semibold` `--primary`, optional bilingual label below.{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}Chapter opener: `ChapterStamp` SVG circular badge — 1.25px `--primary` border ring (40×40), mono numeral centered `font-semibold` `--primary`, drawn-horizon hairline 1px `--primary` below at focal y-coordinate.{{/if}}{{#if style_meta.decorative_pack == "systematic"}}Chapter opener: `ChapterBanner` — ShadBadge `variant="outline"` mono ALL-CAPS chapter index (`01`) + ALL-CAPS chapter title sans 700 + `ShadSeparator` (Radix-based, per-pack styled) full-width below. No SVG, no solid-fill stamp, no dot, no gradient.{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}Chapter opener: `SealStamp` SVG (28-40px) solid-fill `fill="var(--primary)"` square or circle with **centered serif chapter numeral 700 weight in `var(--background)` reverse**, optional bilingual ceremonial label below (e.g. `第一章 · CHAPTER ONE`) `--foreground` serif `font-medium`, no ring, no banner kicker. Above: full-width `GoldenHairline` 1px `var(--primary)` 0.4 alpha rule.{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}Chapter opener: `ChapterNumeralLarge` — chapter index numeral `01` / `02` / `03` rendered at Section Primary scale (`font-extrabold` 800, `var(--primary)` crimson, no SVG, no ring, no badge) inline with chapter title sans 800 to the right (or baseline-aligned). Full-width `HairlineRule` 1px `var(--border-strong)` immediately above the row. No banner kicker, no dot, no gradient.{{/if}}

Chapter divider: {{#if molecular.dividers.content_divider == "hairline-dotdotdot"}}1px `--border` + `· · ·` `--foreground-3` Mono `text-[13px]` `tracking-[0.8em]`{{/if}}{{#if molecular.dividers.content_divider == "alpha-hairline"}}`oklch(1 0 0 / 0.08) h-px`{{/if}}{{#if molecular.dividers.content_divider == "gradient-hairline"}}gradient hairline fading at both ends{{/if}}. In-chapter rest only.

Panel discipline: `rounded-[2px]`–`rounded-[{{atomic.radius.sharp_panel_max_px}}px]` chart frames, {{#if atomic.radius.card_chrome == "double-bezel"}}Double-Bezel{{/if}}{{#if atomic.radius.card_chrome != "double-bezel"}}`rounded-[{{atomic.radius.card_chrome}}px]`{{/if}} card chrome. Each archetype one material logic.

## 6. Motion

Engines: `motion/react` · `motion-plus/react` (AnimateNumber){{#if molecular.hero_shader}} · `@paper-design/shaders-react` ({{molecular.hero_shader.component}}){{/if}}{{#if !molecular.hero_shader}}. No `@paper-design/shaders-react` — Hero uses static CSS layer{{/if}}.

```ts
const EASE = {
  out: [{{atomic.motion_timing.ease_out.0}}, {{atomic.motion_timing.ease_out.1}}, {{atomic.motion_timing.ease_out.2}}, {{atomic.motion_timing.ease_out.3}}],
  inOut: [{{atomic.motion_timing.ease_inout.0}}, {{atomic.motion_timing.ease_inout.1}}, {{atomic.motion_timing.ease_inout.2}}, {{atomic.motion_timing.ease_inout.3}}],
  snap: [{{atomic.motion_timing.ease_snap.0}}, {{atomic.motion_timing.ease_snap.1}}, {{atomic.motion_timing.ease_snap.2}}, {{atomic.motion_timing.ease_snap.3}}],
  spring: [{{atomic.motion_timing.ease_spring.0}}, {{atomic.motion_timing.ease_spring.1}}, {{atomic.motion_timing.ease_spring.2}}, {{atomic.motion_timing.ease_spring.3}}],
};
```

| Category | Duration | Easing |
|----------|----------|--------|
| Hover | {{atomic.motion_timing.hover_ms}}ms | out |
| Button press | {{atomic.motion_timing.button_press_ms}}ms | snap |
| Element entrance | {{atomic.motion_timing.entrance_ms_range.0}}-{{atomic.motion_timing.entrance_ms_range.1}}ms, y: 32-36px | out |
| Number rolling | {{atomic.motion_timing.number_rolling_s_range.0}}-{{atomic.motion_timing.number_rolling_s_range.1}}s | spring, no bounce |
| Curve pathLength | {{atomic.motion_timing.curve_path_s_range.0}}-{{atomic.motion_timing.curve_path_s_range.1}}s | out |
{{#if atomic.motion_timing.signature_stroke_s}}| Signature stroke | {{atomic.motion_timing.signature_stroke_s}}s | out, one-shot |
{{/if}}{{#if atomic.motion_timing.spotlight_drift_s}}| Spotlight drift | {{atomic.motion_timing.spotlight_drift_s}}s/cycle | inOut, infinite |
{{/if}}{{#if molecular.hero_shader}}| WebGL Hero | animated, viewport-paused | speed: {{molecular.hero_shader.props.speed}} |
{{/if}}{{#if !molecular.hero_shader}}| Hero background | static CSS dot-grid / line-grid layer | no motion |
{{/if}}

Entrance: Hero uses `animate=` with delays. Others use `whileInView` with viewport configured as `{{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}` — `once: true` is required to prevent reset to initial hidden state on scroll-out. Section shells, body paragraphs, chart wrappers, and prose render visible on first paint without animation wrappers.

**Every `whileInView` in the entire page must pair with `viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}`** — no exceptions. Without `once: true`, elements reset to initial (opacity 0 / scaleX 0) on scroll-out and disappear.

```tsx
<motion.div initial={{ opacity: 0, y: 34 }} whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }} transition={{ duration: 0.8, ease: EASE.out }} />
```

Stagger: `staggerChildren: {{atomic.motion_timing.stagger_children_s}}` from `"first"`. Reduce by 0.02 on mobile.

Motion per viewport: one focal motion only. Hero staged reveal → Time Series area draw → Proportion rail fill → Ranking cascade → Quote crossfade → Outro signature. Vary by archetype.

### Chapter-reveal trigger

```tsx
function useChapterReveal(margin = "-20%") {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin });
  const [revealed, setRevealed] = useState(false);
  useEffect(() => { if (inView) setRevealed(true); }, [inView]);
  return { ref, revealed };
}
```

Pass `revealed ? data : zeros` into AnimateNumber. Hero uses `margin: "0%"`.

### AnimateNumber scope

Wrap **every key number**: Hero primary, section focal claim, Comparison left/right, Ranking top-1, Cluster cell headlines. Do **not** wrap labels, ordinals, dates, axis values. Cap ≤ 3 per section. `AnimateNumber` accepts pure numeric strings only — always use `parseDisplayValue()` (§17) to extract the number from Bitable formatted values.

SVG: `pathLength: 0→1` draw-in. No `d` morph.

`prefers-reduced-motion`: `animation-duration: 0.01ms !important`; opacity crossfade only; WebGL `speed: 0`; AnimateNumber plain text.

Data-driven invariant: null/undefined → render empty state (§15), not broken animation.

{{#if molecular.hero_shader}}Continuous motion: Hero `{{molecular.hero_shader.component}}` speed {{molecular.hero_shader.props.speed}} in viewport, 0 out. SVG strokes one-shot. No infinite breathing, no scroll-linked transforms.{{/if}}{{#if !molecular.hero_shader}}Continuous motion: none in Hero — background is static CSS. SVG strokes one-shot. No infinite breathing, no scroll-linked transforms.{{/if}}

## 7. Iconography

`lucide-react`, {{atomic.iconography.stroke_width_px}}px stroke, outline-only, `currentColor`, rem sizing, `gap-2` to text. Icons ≤ cap-height. Decorative: `aria-hidden`. Semantic: `role="img"` + `aria-label`. Custom SVG only for {{atomic.iconography.custom_svg_scope}} use cases. Unicode {{#each atomic.iconography.allowed_unicode}}{{this}} {{/each}}allowed inline.

## 8. Accessibility & Mobile

WCAG 2.2 AA: ≥4.5:1 text contrast · ≥3:1 UI contrast · `size-6` (24×24px) targets, `size-11` (44×44px) mobile · `ring-2` focus ring · `prefers-reduced-motion` dual-layer · content reflows at 320px · logical heading hierarchy.

Small text contrast: required labels, captions, axes, and metadata below `text-[14px]` use `--foreground-2` or an equivalent 4.5:1 token. `--foreground-3` is for decorative marks, disabled states, and non-essential metadata only.

Breakpoints (mobile-first):

| Name | Width | Behavior |
|------|-------|----------|
| Base | < 768px | Single-column; full-width CTAs |
| md | ≥ 768px | Two-column layouts; padding increase |
| lg | ≥ 1024px | Full grids; sidebar visible |
| xl | ≥ 1440px | Content caps max-w-5xl; gutters absorb |

`min-h-dvh` for full-height. `env(safe-area-inset-bottom)` for sticky elements. Stair-step type scaling (Section 3 table).

## 9. Do's and Don'ts

Do:
- Neutral ground 60% of viewport; brand accent 8–15%; prose the rest. Open every chapter with the chosen chapter opener.
- {{#if style_meta.focal_numeral_strategy == "primary_on_neutral"}}Focal numerals in `--primary`; units/percent/delta in `--primary-hl` inline at baseline.{{/if}}{{#if style_meta.focal_numeral_strategy == "primary_on_primary"}}Focal numerals in `--primary`; units and delta mix `--primary` / `--primary-hl` at baseline.{{/if}}{{#if style_meta.focal_numeral_strategy == "foreground_with_primary_signal"}}Focal numerals in `--foreground` (white); `--primary` carries unit, direction arrows, and signal accent only — never the headline figure body.{{/if}} Hero leads with confident sans medium title + paragraph subtitle.
- Single-hue chart ramp chart-1–5. Latest period brand accent; older step to chart-3–5.
- One structural visual decision per viewport beyond color.

- **Don't** render focal numerals in {{#if style_meta.focal_numeral_strategy == "foreground_with_primary_signal"}}`--primary` — that token is signal-only; the headline figure is `--foreground`{{/if}}{{#if style_meta.focal_numeral_strategy != "foreground_with_primary_signal"}}`--foreground` — digits use `--primary`; prose holds the foreground{{/if}}.
- **Don't** use unauthorized accent palettes outside the brand hue. No heavy shadows, frosted glass, `backdrop-blur`, rim lighting, card-edge glow, or text glow{{#if atomic.material.shadow == "inset-glow"}} except the documented Double-Bezel inset-glow{{/if}}{{#if atomic.material.shadow == "inset-light"}} except the documented thin-border inset-light{{/if}}.
- **Don't** use `rounded-xl`/`rounded-2xl`/`rounded-3xl`/blob cards. Sharp panels `rounded-[0px]`–`rounded-[{{atomic.radius.sharp_panel_max_px}}px]`; card chrome {{#if atomic.radius.card_chrome == "double-bezel"}}Double-Bezel only{{/if}}{{#if atomic.radius.card_chrome != "double-bezel"}}`rounded-[{{atomic.radius.card_chrome}}px]`{{/if}}.
- **Don't** nest panels beyond one level or wrap sections in page-level containers.
- **Don't** use Inter, Roboto, Space Grotesk, Plus Jakarta, or overused faces outside the declared font stacks above.
- {{#if style_meta.display_typeface_class == "sans"}}**Don't** use serif typefaces or italic posture. Emphasis from scale and color only.{{/if}}{{#if style_meta.display_typeface_class == "serif"}}**Don't** use italic posture — emphasis from scale and color only. Use the declared serif stack consistently across all type levels.{{/if}}
- **Don't** apply weight above {{atomic.typography.weight_ceiling}}. {{#if atomic.typography.weight_ceiling == "500"}}No `font-semibold`, `font-bold`, `font-extrabold`, `font-black`.{{/if}}{{#if atomic.typography.weight_ceiling == "600"}}`font-semibold` reserved for delta value and chapter marker numeral. No `font-bold`, `font-extrabold`, `font-black`.{{/if}}{{#if atomic.typography.weight_ceiling == "700"}}{{#if style_meta.decorative_pack == "festive-royal"}}`font-bold` (700) reserved for Hero Display Number, Hero Title, Section Primary, SealStamp numerals — serif Royal signature. No `font-extrabold`, `font-black`. Body / Lead remains 400-500.{{/if}}{{#if style_meta.decorative_pack == "systematic"}}`font-bold` (700) reserved for Hero Display Number, Page Title, Chapter Stamp numerals. No `font-extrabold`, `font-black`. Body / Lead remains 400-500.{{/if}}{{#if style_meta.decorative_pack == "editorial"}}`font-bold` (700) reserved for Hero Display Number, Page Title, Chapter Stamp numerals. No `font-extrabold`, `font-black`. Body / Lead remains 400-500.{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}`font-bold` (700) reserved for Hero Display Number, Page Title, Chapter Stamp numerals. No `font-extrabold`, `font-black`. Body / Lead remains 400-500.{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}`font-bold` (700) reserved for Hero Display Number, Page Title, Chapter Stamp numerals. No `font-extrabold`, `font-black`. Body / Lead remains 400-500.{{/if}}{{/if}}{{#if atomic.typography.weight_ceiling == "800"}}{{#if style_meta.decorative_pack == "festive-editorial"}}`font-extrabold` (800) reserved for Hero Display Number, Hero Title, Section Primary, ChapterNumeralLarge — editorial brutalist signature. No `font-black`. Body / Lead remains 400-500.{{/if}}{{#if style_meta.decorative_pack != "festive-editorial"}}`font-extrabold` (800) reserved for Hero focal title in ALL CAPS. No `font-black`. Body / Lead remains 400-500.{{/if}}{{/if}}
- **Don't** repeat same panel material every chapter. Vary by archetype.
- **Don't** fade whole sections opacity-only, repeat identical `y + opacity` reveals, or animate CSS layout properties. Animate `transform` and `opacity`.
- **Don't** tween numbers as single value or duplicate unit/percent; per-digit spring only.
- **Don't** use ease strings; cubic-bezier arrays only. Use `min-h-dvh` not `h-screen`.
- **Don't** render text below `text-[10px]`; required reading `text-[14px]+`.
- **Don't** wrap every number in AnimateNumber — reserve for key claim numbers. Labels, ordinals, dates, axis values render plain.
- **Don't** use `whileInView` without `viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}`.
- **Don't** use `useInView` + conditional `animate` for entrance; use `whileInView` + `viewport`. `useInView` reserved for Hero shader pause and chapter-reveal trigger (§6).
- **Don't** use `useScroll`/`useTransform`/`scrollYProgress` for Hero exit or scroll-linked parallax.
- **Don't** use ScrambleText, Typewriter, Ticker, or character-level reveal.
- **Don't** introduce a second hot accent for delta-down or error. Neutral foreground carries those.
- **Don't** animate bar chart bars rising from zero — bars render static; highlighted bar uses `clip-path` reveal once.
- **Don't** animate paragraph reveal as reader scrolls. Prose visible on first paint.
- **Don't** wrap chapter `<section>` containers, chart wrappers, KPI grids, body paragraphs, or whole-page content blocks in `motion.div` with `initial={{ opacity: 0 }}` + `whileInView`. These containers must render visible on first paint.

## 10. Pattern Overview

### Scenario Mindset

This page is a story told in data, not a dashboard — every section is a chapter, every chart is evidence for a claim.
The narrative arc runs across the whole page: opening hook → supporting evidence → closing impact. Each section advances exactly one beat of the arc.
Each section carries one focal claim and exactly one supporting visual (chart, ranking, or quote). Parallel KPI tiles, side-by-side metric grids, and three competing focal numbers belong to a dashboard, not a campaign report.
A successful page lets the reader leave with three things: the headline number, the why behind it, the so-what of it.
Archetype names are internal planning labels only. Visible eyebrows, captions, and labels come from the topic, period, data role, or business meaning, not from section archetype names.

### Scope

Scope: scrollable single-page data narrative where numbers are the protagonist.

Atmosphere: Information density Low → High (rhythm-controlled) · Visual rhythm Strong alternation (different archetype per section) · Narrative arc Beginning → Middle → End.

Supported data shapes: time-series · proportions · paired metrics · ranking · grouped metrics · event sequence · peer catalog · comparison.

### Voice & Copy

The page's copy reads like a curator's wall text — terse, third-person, observational.

- Voice: third-person observational. Use `we` only in attribution; never address the reader as `you`.
- Statements, not calls to action: `Bookings closed at 142,300`, not `We booked 142,300!` — a campaign report is a read-only artifact.
- Eyebrows: uppercase, mono, `tracking-[{{atomic.typography.eyebrow_tracking_em}}em]`. Titles: sentence case, no terminal period. Body: sentence case, full sentences, terminal punctuation.
- Numbers in copy: tabular figures, thousands separators, no decimal padding.
- Period strings use a `·` middle dot (U+00B7) with single spaces around it.

### Voice — Style Annotations

Copy register: {{style_meta.ground_truth_signature}}. Chapter titles 5–14 CJK / 4–9 EN words, `font-medium` sans. Eyebrow tracking `{{atomic.typography.eyebrow_tracking_em}}em`. Resist slogans, questions, ALL-CAPS.

## 11. Section Archetype Library

A section = **archetype** (what) + **composition treatment** (layout) + **dominant move** (eye-lead).

### 11.1 Composition Treatments

| Treatment | Logic | Density |
|-----------|-------|---------|
| **Full-bleed Monolith** | One element fills frame, centered | spacious |
| **Asymmetric Split** | Two unequal columns (3:2 / 2:1) | medium |
| **Stacked Band** | Full-width bands stacked | medium–dense |
| **Matrix Grid** | Equal cells N×M, narratively bound | dense |
| **Proportion Rail** | Continuous parts-of-whole rail | medium |
| **Offset Frame** | Disrupts grid: crop/off-center/overflow | medium |
| **Sequence Track** | Stepped: index → title → note | medium–dense |
| **Typographic Field** | Type alone, no panels or chrome | spacious–medium |
| **Annotation Rail** | Main (3/4) + narrow rail (1/4) | medium |

Favored: {{molecular.hero_geometry.default_treatment}} (Hero), Matrix Grid (KPI Cluster), Stacked Band, Asymmetric Split.

### 11.2 Dominant Move

| Move | Class |
|------|-------|
| Scale jump (focal ≥ 2 tiers larger) | steady |
| Single stroke (one line/accent) | steady |
| Path reveal (curve draws / rail fills) | steady |
| Crop / bleed | disruptive |
| Offset placement | disruptive |
| Column break | disruptive |

Leads with scale jump and single stroke. Disruptive ≤ 1 chapter per page.

### 11.3 Archetypes

**Hero Monolith** — Opening anchor. Default treatment: {{molecular.hero_geometry.default_treatment}}. Alts: the other two treatments below.

**Time Series** — Values over time. Treatments: Stacked Band **(default)** · Asymmetric Split. Build with bare recharts `AreaChart`/`LineChart` in `<ResponsiveContainer>`, custom `<ChartTooltipCard>` or `contentStyle` per §17.

**Proportion Field** — Parts-of-whole. Treatments: Proportion Rail **(default)** · Stacked Band. Donut/pie/ring not used. Bare recharts horizontal `BarChart` + `<LabelList>`, or shadcn `Progress`.

**Comparison** — Two metrics contrasted. Treatments: Asymmetric Split **(default)** · Stacked Band. Left/right same font-size; hierarchy from color — leading `--primary`, trailing `--foreground-3`. Grid `items-start`.

**Ranking / List** — Items by magnitude. Stacked Band (≤ 5) · Matrix Grid (≥ 6). Scale jump on top-1. List typography — never recharts `BarChart`.

**Grouped Metric Cluster** — Parallel metrics, one claim. **Matrix Grid 2×2/2×3**: CSS `grid gap-1`, `bg-surface-l2 {{#if atomic.radius.card_chrome == "double-bezel"}}Double-Bezel{{/if}}{{#if atomic.radius.card_chrome != "double-bezel"}}rounded-[{{atomic.radius.card_chrome}}px]{{/if}} p-6 md:p-8`, no extra border/shadow{{#if atomic.material.shadow != "none"}} beyond declared depth treatment{{/if}}; cell `h-full`, note `mt-auto`; hover `whileHover={{ y: -2 }}` 0.28s.

**Sequence / Timeline** — Time-ordered events (not values). Sequence Track default. **Horizontal Timeline** alt (desktop ≥ md): 3–5 col grid, primary-bordered circle dots (10×10, 1.5px `--primary` border, `--background` fill), 1px `--border-strong` hairline connecting. Below each: mono accent kicker · title · body. **Mobile fallback (< md): Vertical Timeline, left-aligned** — collapses to single column; rotate the hairline 90° to a 1px `--border-strong` vertical rail at the left edge (offset ~7px from container left); primary dots (14×14, 1.5px `--primary` border, `--background` fill) centered on the rail at each milestone; each milestone's content (mono accent kicker · title sans medium · body) sits to the right of the rail, **left-aligned start-aligned at the dot baseline — never center-aligned**. Use shadcn `Item` + `ItemGroup` for the vertical mobile layout.

**Peer Set / Catalog** — Same-kind peers. Matrix Grid default. Shadcn `Card` (border-0 shadow-none p-0).

**Quote Interstitial** — Narrative pause. Typographic Field. {{#if style_meta.decorative_pack == "editorial"}}SVG L-shape brackets (40×40, 1px primary 0.6 opacity).{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}lucide `<Quote />` icon `--primary` 0.6 opacity, ≤ cap-height.{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}lucide `<Quote />` icon `--primary` 0.6 opacity, ≤ cap-height.{{/if}}{{#if style_meta.decorative_pack == "systematic"}}No icon, no brackets — quote sits unadorned in Typographic Field, opening en-dash `—` `--primary` as lead-in.{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}No icon, no brackets — quote sits in Typographic Field with opening character `「` (CJK left corner bracket) `var(--primary)` `font-medium` as lead-in and closing `」` symmetric. Serif Quote scale, `--foreground`.{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}No icon, no brackets — opening em-dash `—` `var(--primary)` `font-extrabold` as lead-in and trailing em-dash `—` symmetric. Quote scale `font-normal` `--foreground`, ALL CAPS optional for short pull quotes.{{/if}} One sentence ≤ 28 words, Quote scale `font-normal` — no italic, no left border.

**Outro Reverent** — End of report. Typographic Field. {{#if style_meta.decorative_pack == "editorial"}}`OutroSignature` component (§17) — twin hairlines + diamond rotate 0→45°.{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}Closing claim Section Primary + optional final `ChapterStamp` numeral.{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}Closing claim Section Primary + terminal drawn-horizon hairline + optional final `ChapterStamp` numeral.{{/if}}{{#if style_meta.decorative_pack == "systematic"}}Closing claim Section Primary ALL-CAPS sans 700 + terminal full-width `ShadSeparator`. No diamond, no stamp, no ornament beyond the separator.{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}Closing claim Section Primary serif `font-bold` (700) + terminal full-width `GoldenHairline` 1px `var(--primary)` 0.4 alpha + optional final `SealStamp` (square variant). No diamond, no ornament beyond the gold hairline.{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}Closing claim Section Primary sans `font-extrabold` (800) ALL CAPS + terminal full-width `HairlineRule` 1px `var(--border-strong)` + optional closing `ChapterNumeralLarge "END"` `var(--primary)`. No diamond, no SealStamp, no ornament beyond hairline.{{/if}} Optional — emit only with closing claim.

## 12. Composition

Default: Hero → evidence chapters → optional Outro. Section count follows data; stop before filler. {{#if patterned.density_lead == "spacious"}}This style favors 7–9 chapters, paragraph-driven.{{/if}}{{#if patterned.density_lead == "medium"}}This style favors 5–8 chapters, balanced cadence.{{/if}}{{#if patterned.density_lead == "dense"}}This style supports as many chapters as data evidence demands, dense rhythm.{{/if}}

### 12.1 Rhythm

1. **Density rotation** — adjacent differ (dense/medium/spacious); no two consecutive dense.
2. **Treatment variety** — no two consecutive same treatment or archetype.
3. **Bold-move budget** — disruptive ≤ ceil(N × 0.25). This style runs {{patterned.density_lead}}.
4. **Break cadence** — ≥ 1 section uses Full-bleed, Offset, or Typographic Field. Hero + Outro satisfy.

### 12.2 Rules

Ground consistent across chapters; vary rhythm through density, hairlines, accent position. Chapter markers: `01` `02` `03`. {{#if style_meta.decorative_pack == "editorial"}}Editorial pack uses `ChapterBanner` (ShadBadge filled + hairline-banner divider) — no `ChapterStamp` SVG.{{/if}}{{#if style_meta.decorative_pack != "editorial"}}ChapterStamp at most 3× when {{molecular.hero_geometry.stamp_constraint}}.{{/if}} Chapter opener: {{#if style_meta.decorative_pack == "editorial"}}`ChapterBanner` every non-Hero chapter{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}`ChapterStamp` SVG circular badge (border ring) optional per chapter{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}`ChapterStamp` SVG circular badge + drawn-horizon hairline optional per chapter{{/if}}{{#if style_meta.decorative_pack == "systematic"}}`ChapterBanner` (ShadBadge outline + ALL-CAPS title) + `ShadSeparator` every non-Hero chapter (one per chapter, no exceptions){{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}`SealStamp` SVG square/circle `fill="var(--primary)"` + `GoldenHairline` rule every non-Hero chapter (one per chapter, no exceptions; Hero ≠ chapter, no SealStamp){{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}`ChapterNumeralLarge` index numeral + chapter title sans 800 + `HairlineRule` rule every non-Hero chapter (one per chapter, no exceptions; Hero ≠ chapter, no ChapterNumeralLarge in Hero){{/if}}. Chapter divider for in-chapter rests, sparingly.

## 13. Section Anatomy

### 13.1 Hero Monolith

Focal: primary-value Display Number, display stack `font-medium` `--primary`, {{#if atomic.typography.unit_suffix_lg}}unit suffix `--primary-hl`{{/if}}{{#if !atomic.typography.unit_suffix_lg}}inline unit `--primary-hl`{{/if}}, animated count-up. Background: page-level `var(--background)` ground{{#if molecular.hero_shader}} + {{molecular.hero_shader.component}} Hero anchor (Hero section internal, see §17, viewport-paused){{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "dot-grid"}} + static CSS dot-grid layer (see §17, no WebGL){{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "line-grid"}} + static CSS line-grid layer (see §17, no WebGL){{/if}}. {{#if atomic.color.primary_wash}}Above the Hero shader, `--ember-wash` CSS radial ~18% alpha.{{/if}}{{#if atomic.color.ambient_ink}}Above the Hero shader, `--glow-ink` ambient tint.{{/if}}

Composition — {{molecular.hero_geometry.default_treatment}}: {{#if molecular.hero_geometry.default_treatment == "asymmetric-split"}}`grid-cols-1 lg:grid-cols-[1fr_auto] lg:gap-x-16 items-start`. Left: eyebrow → hero title → subtitle → focal block. Right: metadata masthead `hidden lg:flex flex-col items-end gap-10` — ISSUE/PAGES/AUDIT/AUTHOR mono uppercase{{/if}}{{#if molecular.hero_geometry.default_treatment == "full-bleed-monolith"}}Centered single-column. Stack: eyebrow → page title → focal Display Number → subtitle → delta indicator{{/if}}{{#if molecular.hero_geometry.default_treatment == "typographic-field"}}Centered type-only field. No chart, no figure — claim-line title carries the section{{/if}}.

Hero brand marks: focal numeral, delta indicator{{#if molecular.hero_shader}}, shader breath{{/if}}{{#if !molecular.hero_shader}}, static CSS background layer{{/if}}{{#if style_meta.decorative_pack == "editorial"}}. No signature line at bottom{{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "drawn-horizon"}}, drawn-horizon SVG line `pathLength: 0→1`{{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "dot-grid"}}. ALL-CAPS Hero title carries the section over the static dot-grid{{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "line-grid"}}. ALL-CAPS Hero title carries the section over the static line-grid{{/if}}.

Alts: the other two treatments not chosen as default.

Anti-refs: **Don't** set Hero on saturated brand-hue ground. **Don't** use product photos. **Don't** stack banners or KPI grids in Hero. **Don't** pair brand accent with a second hot accent.

Primary-value selection: (1) rate/percentage → avg, (2) aggregate keyword → sum, (3) primary metric → max, (4) same → avg. If missing, omit Hero.

```tsx
const heroVariants = { hidden: {}, visible: { transition: { staggerChildren: {{atomic.motion_timing.stagger_children_s}} } } };
const fadeUp = { hidden: { opacity: 0, y: 36 }, visible: { opacity: 1, y: 0, transition: { duration: 0.9, ease: EASE.out } } };
const { prefix, number, suffix } = parseDisplayValue(displayValue)

<motion.div initial="hidden" animate="visible" variants={heroVariants} className="relative z-20">
  <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] lg:gap-x-16 items-start">
    <div className="flex flex-col items-start text-left">
      <motion.p variants={fadeUp}><Eyebrow>{topic} · {period}</Eyebrow></motion.p>
      <motion.h1 variants={fadeUp} className="max-w-[{{atomic.typography.cjk_hero_max_ch}}ch] text-[{{atomic.typography.display_number_mobile}}px] md:text-[{{atomic.typography.display_number_lg}}px] font-medium leading-[{{atomic.typography.display_lh}}] tracking-[{{atomic.typography.display_ls_em}}em] text-[var(--foreground)]">{heroTitle}</motion.h1>
      <motion.p variants={fadeUp} className="max-w-[{{atomic.typography.cjk_body_max_ch}}ch] text-[{{atomic.typography.body}}px] font-normal leading-[1.6] text-[var(--foreground-3)]">{subtitle}</motion.p>
      <motion.div variants={fadeUp} className="inline-flex items-baseline gap-1 whitespace-nowrap">
        {/* Use parseDisplayValue() to safely split formatted Bitable value */}
        {prefix && <span style={{ color: "var(--primary-hl)" }}>{prefix}</span>}
        <AnimateNumber style={{ color: "var(--primary)" }} transition={{ type: "spring", duration: {{atomic.motion_timing.number_rolling_s_range.1}}, bounce: 0 }}>{number || 0}</AnimateNumber>
        {suffix && <span style={{ color: "var(--primary-hl)" }}>{suffix}</span>}
      </motion.div>
    </div>
    <motion.aside variants={fadeUp} className="hidden lg:flex flex-col items-end gap-10" />
  </div>
</motion.div>
```

Budget: 5-step stagger (entrance), AnimateNumber roll (data-load), shader breath (ambient).

### 13.2 Non-Hero slot mapping

| Archetype × Treatment | Focal | Secondary | Move |
|-----------------------|-------|-----------|------|
| Time Series · Stacked Band | chart upper band | prose lower | path reveal |
| Comparison · Asymmetric Split | leading `--primary` wide col | trailing `--foreground-3` same font-size | scale jump |
| Ranking · Stacked Band | top-1 row | rows 2–5 descending | scale jump |
| Cluster · Matrix Grid | banner + Display Number `--primary` cells | `h-full` + `mt-auto` alignment | scale jump |
| Quote · Typographic Field | Quote text `font-normal` foreground | {{#if style_meta.decorative_pack == "editorial"}}SVG L-shape{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}lucide Quote{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}lucide Quote{{/if}}{{#if style_meta.decorative_pack == "systematic"}}leading en-dash `—`{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}CJK bracket `「 」` lead-in / lead-out{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}em-dash `—` lead-in / lead-out{{/if}} + attribution | column break |
| Outro · Typographic Field | closing title Section Primary | {{#if style_meta.decorative_pack == "editorial"}}`OutroSignature`{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}closing `ChapterStamp` (ring){{/if}}{{#if style_meta.decorative_pack == "instrumental"}}closing `ChapterStamp` + terminal hairline{{/if}}{{#if style_meta.decorative_pack == "systematic"}}terminal `ShadSeparator`{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}closing solid-fill `SealStamp` (square) + `GoldenHairline`{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}closing `ChapterNumeralLarge "END"` + `HairlineRule`{{/if}} + caveats | single stroke |
| Hero · {{molecular.hero_geometry.default_treatment}} | focal Display Number `--primary` | metadata mono uppercase | scale jump |

## 14. Data → Section Mapping

| Data Shape | Archetype |
|------------|-----------|
| Report-level anchor | Hero Monolith |
| Time-ordered series | Time Series |
| Parts-of-whole | Proportion Field |
| Two contrasting values | Comparison |
| Ordered by magnitude | Ranking / List |
| Parallel metrics, one claim | Grouped Metric Cluster |
| Time-ordered events | Sequence / Timeline |
| Same-kind peer set | Peer Set / Catalog |
| Narrative beat | Quote Interstitial |
| End reflection | Outro Reverent |

Priority: data shape → adjacency → treatment per §11.3 → §12 rhythm. Favored order: Hero → Cluster → Time Series → Comparison → Cluster → Ranking → Sequence → Outro.

## 15. Functional States

- **Loading**: skeleton replaces only data-dependent slots. Static section structure, Hero shader, and chapter markers remain visible.
- **Empty**: section frame + centered "No data available" in `--foreground-3`.
- **Error**: frame + retry icon + "Failed to load" + retry button in `--foreground-2`.

## 16. Do's and Don'ts

Do: alternate archetypes. Consistent ground; vary rhythm through density/hairlines/accent position. One focal per section. Skip data-absent sections. Visible labels from topic/period/metric/business meaning.

- **Don't** show archetype names in visible UI.
- **Don't** use equal 3-col grids, sidecar KPI stacks, or Matrix not evidencing one claim.
- **Don't** fix section heights; content determines, min-height.
- **Don't** show multiple primary numbers per section. Separate legends from charts.
- **Don't** use donut/pie/ring charts — proportion is rail or band.
- **Don't** repeat identical circular markers. Apply identical reveals everywhere.
- **Don't** show >5 ranking items untruncated. Allow horizontal scroll.
- **Don't** use emoji. Add CTA/action buttons, "view more", dashboard/marketing verbs, second-person imperatives.
- **Don't** force outro without closing claim.

{{#if style_meta.mode == "light"}}Light-mode: overlays/skeletons use `--surface-l2`{{#if atomic.color.primary_wash}} or `--ember-wash`{{/if}}. No vignettes.{{/if}}{{#if style_meta.mode == "dark"}}Dark-mode: overlays/skeletons use `--surface-l2`{{#if atomic.color.ambient_ink}} or `--glow-ink`{{/if}}. No vignettes, no white-flash transitions.{{/if}}

## 17. Components Inventory

### Pre-imported

**Page ground** — Page background uses `var(--background)` token directly. Set via `style={{ background: "var(--background)" }}` on the App root `<div>`. {{#if molecular.hero_shader}}The page has no page-level WebGL shader; the only WebGL layer is Hero `<{{molecular.hero_shader.component}}>` (see below).{{/if}}{{#if !molecular.hero_shader}}The page has **no WebGL layer at all**. Hero background uses a static CSS layer (dot-grid / line-grid) — see Hero static background block below.{{/if}}

{{#if molecular.hero_shader}}
> Pass hex / rgb / hsl strings to paper-shaders `colors` and `colorBack` props. The shader engine does not parse CSS `oklch()` color functions — use the hex equivalent. CSS tokens with oklch() still apply on regular DOM elements.

**{{molecular.hero_shader.component}}** (@paper-design/shaders-react) — Hero anchor shader.
{{/if}}

{{#if molecular.hero_shader}}
{{#if molecular.hero_shader.component == "GrainGradient"}}
```tsx
import { GrainGradient } from "@paper-design/shaders-react";

function HeroShader() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { margin: '-10% 0px' });
  const reducedMotion = useReducedMotion();

  return (
    <>
      <div ref={ref} className="pointer-events-none"
        style={{ position: 'absolute', width: 1, height: 1, opacity: 0 }} aria-hidden />
      <div className="fixed inset-0 pointer-events-none"
        style={{ zIndex: 10, opacity: inView ? 1 : 0, transition: 'opacity 500ms ease' }} aria-hidden>
        <GrainGradient
          shape="{{molecular.hero_shader.props.shape}}"
          colors={[{{#each molecular.hero_shader.props.colors}}'{{this}}'{{#unless @last}}, {{/unless}}{{/each}}]}
          colorBack="{{molecular.hero_shader.props.colorBack}}"
          softness={ {{molecular.hero_shader.props.softness}} }
          intensity={ {{molecular.hero_shader.props.intensity}} }
          noise={ {{molecular.hero_shader.props.noise}} }
          speed={!reducedMotion && inView ? {{molecular.hero_shader.props.speed}} : 0}
          scale={ {{molecular.hero_shader.props.scale}} }
          rotation={ {{molecular.hero_shader.props.rotation}} }
          offsetX={ {{molecular.hero_shader.props.offsetX}} }
          offsetY={ {{molecular.hero_shader.props.offsetY}} }
          fit="{{molecular.hero_shader.props.fit}}"
          style={{ position: 'absolute', inset: 0 }}
        />
      </div>
    </>
  );
}
```
{{/if}}

{{#if molecular.hero_shader.component == "MeshGradient"}}
```tsx
import { MeshGradient } from "@paper-design/shaders-react";

function HeroShader() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { margin: '-10% 0px' });
  const reducedMotion = useReducedMotion();

  return (
    <>
      <div ref={ref} className="pointer-events-none"
        style={{ position: 'absolute', width: 1, height: 1, opacity: 0 }} aria-hidden />
      <div className="fixed inset-0 pointer-events-none"
        style={{ zIndex: 10, opacity: inView ? 1 : 0, transition: 'opacity 500ms ease' }} aria-hidden>
        <MeshGradient
          colors={[{{#each molecular.hero_shader.props.colors}}'{{this}}'{{#unless @last}}, {{/unless}}{{/each}}]}
          distortion={ {{molecular.hero_shader.props.distortion}} }
          swirl={ {{molecular.hero_shader.props.swirl}} }
          grainOverlay={ {{molecular.hero_shader.props.grainOverlay}} }
          opacity={ {{molecular.hero_shader.props.opacity}} }
          speed={!reducedMotion && inView ? {{molecular.hero_shader.props.speed}} : 0}
          style={{ position: 'absolute', inset: 0 }}
        />
      </div>
    </>
  );
}
```
{{/if}}

{{#if molecular.hero_shader.component == "GodRays"}}
```tsx
import { GodRays } from "@paper-design/shaders-react";

function HeroShader() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { margin: '-10% 0px' });
  const reducedMotion = useReducedMotion();

  return (
    <>
      <div ref={ref} className="pointer-events-none"
        style={{ position: 'absolute', width: 1, height: 1, opacity: 0 }} aria-hidden />
      <div className="fixed inset-0 pointer-events-none"
        style={{ zIndex: 10, opacity: inView ? 1 : 0, transition: 'opacity 500ms ease' }} aria-hidden>
        <GodRays
          colors={[{{#each molecular.hero_shader.props.colors}}'{{this}}'{{#unless @last}}, {{/unless}}{{/each}}]}
          colorBack="{{molecular.hero_shader.props.colorBack}}"
          colorBloom="{{molecular.hero_shader.props.colorBloom}}"
          density={ {{molecular.hero_shader.props.density}} }
          spotty={ {{molecular.hero_shader.props.spotty}} }
          midIntensity={ {{molecular.hero_shader.props.midIntensity}} }
          midSize={ {{molecular.hero_shader.props.midSize}} }
          intensity={ {{molecular.hero_shader.props.intensity}} }
          bloom={ {{molecular.hero_shader.props.bloom}} }
          offsetX={ {{molecular.hero_shader.props.offsetX}} }
          fit="{{molecular.hero_shader.props.fit}}"
          speed={!reducedMotion && inView ? {{molecular.hero_shader.props.speed}} : 0}
          style={{ position: 'absolute', inset: 0 }}
        />
      </div>
    </>
  );
}
```
{{/if}}

{{#if molecular.hero_shader.component == "Dithering"}}
```tsx
import { Dithering } from "@paper-design/shaders-react";

function HeroShader() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { margin: '-10% 0px' });
  const reducedMotion = useReducedMotion();

  return (
    <>
      <div ref={ref} className="pointer-events-none"
        style={{ position: 'absolute', width: 1, height: 1, opacity: 0 }} aria-hidden />
      <div className="fixed inset-0 pointer-events-none"
        style={{ zIndex: 10, opacity: inView ? 1 : 0, transition: 'opacity 500ms ease' }} aria-hidden>
        <Dithering
          type="{{molecular.hero_shader.props.type}}"
          shape="{{molecular.hero_shader.props.shape}}"
          size={ {{molecular.hero_shader.props.size}} }
          colorFront="{{molecular.hero_shader.props.colorFront}}"
          colorBack="{{molecular.hero_shader.props.colorBack}}"
          scale={ {{molecular.hero_shader.props.scale}} }
          speed={!reducedMotion && inView ? {{molecular.hero_shader.props.speed}} : 0}
          style={{ position: 'absolute', inset: 0 }}
        />
      </div>
    </>
  );
}
```
{{/if}}
{{/if}}

{{#if molecular.hero_geometry.extra_svg_layer == "dot-grid"}}
**Hero static background — CSS dot-grid** (no WebGL, no `@paper-design/shaders-react`). Replaces shader for Swiss / systematic minimalism. Pure CSS, zero runtime cost, respects `prefers-reduced-motion` by virtue of being static.

```css
.hero-static-bg {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, var(--border-strong) 1px, transparent 1px);
  background-size: 32px 32px;
  background-position: 0 0;
  pointer-events: none;
  z-index: 10;
}
```

Render inside Hero `<section className="relative">` as a single `<div className="hero-static-bg" aria-hidden />` before text wrapper. No animation, no opacity fade, no breath.
{{/if}}

{{#if molecular.hero_geometry.extra_svg_layer == "line-grid"}}
**Hero static background — CSS line-grid** (no WebGL). Static rectilinear grid for systematic register.

```css
.hero-static-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(to right, var(--border) 1px, transparent 1px),
    linear-gradient(to bottom, var(--border) 1px, transparent 1px);
  background-size: 80px 80px;
  pointer-events: none;
  z-index: 10;
}
```

Render inside Hero `<section className="relative">` as a single `<div className="hero-static-bg" aria-hidden />` before text wrapper. No animation, no fade.
{{/if}}

**App root structure** — Page background uses `var(--background)` flat token directly on the App root `<div>`. Do not wrap chapter sections in any semantic container (`<main>` / `<article>` / `<section>` wrapping all sections) — semantic wrappers create extra stacking contexts that conflict with absolute-positioned shaders inside Hero. {{#if molecular.hero_shader}}The Hero shader lives inside Hero `<section className="relative">`; all other chapter sections are direct children of the App root `<div>` and inherit the flat `var(--background)` ground.{{/if}}{{#if !molecular.hero_shader}}The Hero static background layer lives inside Hero `<section className="relative">`; all other chapter sections are direct children of the App root `<div>` and inherit the flat `var(--background)` ground.{{/if}}

{{#if atomic.color.primary_wash}}{{#if molecular.hero_geometry.radial_wash_css}}Hero ember-wash CSS: `{{molecular.hero_geometry.radial_wash_css}}`. Layer stack within Hero section (bottom→top): {{molecular.hero_shader.component}} (z:10) · ember-wash (z:15) · **Hero text wrapper must be `relative z-20` or higher**. Outro mirrors at page-bottom-center, smaller.{{/if}}{{/if}}{{#if atomic.color.ambient_ink}}Hero glow-ink overlay: ambient inked tint above shader, below text. Layer stack within Hero section (bottom→top): {{molecular.hero_shader.component}} (z:10) · glow-ink (z:15) · **Hero text wrapper must be `relative z-20` or higher**.{{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "drawn-horizon"}} Drawn-horizon SVG layer (z:17) — `<motion.line>` `var(--primary)` 1px stroke + `pathLength: 0→1`, `delay 0.4s, duration {{atomic.motion_timing.curve_path_s_range.1}}s`.{{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "dot-grid"}} Hero static CSS dot-grid layer (z:10) — single `<div className="hero-static-bg" aria-hidden />` per Hero. No motion. Text wrapper `relative z-20`.{{/if}}{{#if molecular.hero_geometry.extra_svg_layer == "line-grid"}} Hero static CSS line-grid layer (z:10) — single `<div className="hero-static-bg" aria-hidden />` per Hero. No motion. Text wrapper `relative z-20`.{{/if}}{{#if atomic.material.noise_overlay == "svg-feturbulence"}} Page-level SVG `feTurbulence baseFrequency=0.65 numOctaves=3` opacity 0.1 overlay-blend (z:1, below all content).{{/if}}

**AnimateNumber** (motion-plus/react) — Per-digit scroll. `{number || 0}` triggers roll. Children must be a **pure numeric string** (no commas, no symbols). Bitable formatted values like `"¥1,234,567.00"` or `"85%"` will NaN — use `parseDisplayValue()` to split first.

```tsx
import { AnimateNumber } from "motion-plus/react";

// Split Bitable formatted value → prefix / pure number / suffix
function parseDisplayValue(value: string | number | undefined) {
  if (value === undefined || value === null) return { prefix: "", number: "0", suffix: "" };
  const str = String(value);
  const match = str.match(/^([^\d\-]*?)(-?[\d,]+\.?\d*)(.*)$/);
  if (!match) return { prefix: "", number: "0", suffix: "" };
  return {
    prefix: (match[1] ?? "").trim(),
    number: match[2].replace(/,/g, ""),
    suffix: (match[3] ?? "").trim(),
  };
}

// Usage: "¥1,234,567.00" → prefix="¥", number="1234567.00", suffix=""
//        "85%" → prefix="", number="85", suffix="%"
const { prefix, number, suffix } = parseDisplayValue(row["sum(fldRevenue)"]?.value);
<span className="inline-flex items-baseline gap-1 whitespace-nowrap">
  {prefix && <span style={{ color: "var(--primary-hl)" }}>{prefix}</span>}
  <AnimateNumber
    style={{ color: "var(--primary)" }}
    transition={{ type: "spring", duration: {{atomic.motion_timing.number_rolling_s_range.1}}, bounce: 0 }}
  >
    {number || 0}
  </AnimateNumber>
  {suffix && <span style={{ color: "var(--primary-hl)" }}>{suffix}</span>}
</span>
```

**Recharts** (recharts) — Bare recharts for all charts. Series colors from `var(--chart-1)` through `var(--chart-5)` directly.

```tsx
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

<ResponsiveContainer width="100%" height="100%">
  <AreaChart data={chartData} margin={{ top: 24, right: 24, left: 0, bottom: 16 }}>
    {{#if molecular.chart.grid_dasharray}}<CartesianGrid stroke="var(--border-strong)" strokeDasharray="{{molecular.chart.grid_dasharray}}" vertical={ {{molecular.chart.grid_vertical}} } />{{/if}}
    <XAxis dataKey="period" stroke="var(--foreground-2)" tickLine={false} axisLine={false} />
    <YAxis stroke="var(--foreground-2)" tickLine={false} axisLine={false} width={48} />
    <Area type="{{molecular.chart.area_type}}" dataKey="revenue" stroke="var(--chart-1)" fill="url(#fillRevenue)"
      strokeWidth={2} isAnimationActive={false}
      {{#if molecular.chart.last_point_treatment == "halo+dot"}}dot={(props) => { /* last-index only: halo r=10 primary 0.18 + dot r=5 primary */ }}
      activeDot={{ r: 6, fill: "var(--primary)", stroke: "var(--background)", strokeWidth: 2 }}{{/if}}
      {{#if molecular.chart.last_point_treatment == "activeDot"}}activeDot={{ r: 6, fill: "var(--primary)", stroke: "var(--background)", strokeWidth: 2 }}{{/if}} />
    <Tooltip {{#if molecular.chart.cursor_style == "dashed-stroke"}}cursor={{ stroke: "var(--primary)", strokeDasharray: "2 4", strokeOpacity: 0.5 }}{{/if}}{{#if molecular.chart.cursor_style == "fill-hover"}}cursor={{ fill: "var(--chart-hover)" }}{{/if}}
      {{#if molecular.chart.tooltip_card == "custom-component"}}content={<ChartTooltipCard />}{{/if}}{{#if molecular.chart.tooltip_card == "content-style"}}contentStyle={{ background: "var(--surface-l2)", border: "1px solid var(--border-strong)", color: "var(--foreground)" }}{{/if}} wrapperStyle={{ outline: "none" }} />
  </AreaChart>
</ResponsiveContainer>
```

Rules: `isAnimationActive={false}` always. `--chart-1` latest period only, prior step to `--chart-3`–`--chart-5`. Grid `var(--border-strong)` horizontal only. Axis `var(--foreground-2)`, no tickLine/axisLine. {{#if molecular.chart.area_fill_opacity == "gradient"}}Area gradient `stopOpacity={0.35}` → `{0}`.{{/if}}{{#if molecular.chart.area_fill_opacity != "gradient"}}Area flat `fillOpacity={ {{molecular.chart.area_fill_opacity}} }`.{{/if}} {{#if molecular.chart.last_point_treatment == "halo+dot"}}Last-point: `dot` fn returns halo `r=10 fill=primary fillOpacity=0.18` + dot `r=5` on last index only.{{/if}} Three treatments: (1) Bar + `<LabelList position="top">`; (2) Area + {{#if molecular.chart.area_fill_opacity == "gradient"}}gradient{{/if}}{{#if molecular.chart.area_fill_opacity != "gradient"}}flat fill{{/if}} + {{#if molecular.chart.last_point_treatment != "none"}}last-point{{/if}}{{#if molecular.chart.last_point_treatment == "none"}}no last-point ornament{{/if}}; (3) Sparkline `h-12` no axes.

**Bar chart fill must be explicitly set on every Bar — recharts' default Bar fill is solid black (`#000`), so omitting `fill` produces an entirely black chart.** Apply token fills directly via `fill="var(--chart-N)"` on the `<Bar>` element for single-color series, or per-data-point via `<Cell>` children when colors vary by index. Never rely on recharts default fill, never use Tailwind palette, never use hex literals — always `var(--chart-1)` through `var(--chart-5)` tokens. Highlighted / latest bar uses `var(--chart-1)` brand accent; prior bars step to `var(--chart-3)` through `var(--chart-5)`.

**Every `<Tooltip>` must set `contentStyle` or wire `<ChartTooltipCard />`** — recharts default `contentStyle` renders as a black card in dark mode and on PieChart / DonutChart where no `cursor` prop applies. Use `contentStyle={{ background: "var(--surface-l2)", border: "1px solid var(--border-strong)", color: "var(--foreground)" }}` for inline tooltips, or pass `content={<ChartTooltipCard />}` to wire the custom component (already defined below).

**BarChart Tooltip cursor must be explicitly set** — recharts BarChart cursor defaults to a fill rectangle that may render `#000` solid black in certain versions or theme contexts. Apply `cursor={{ fill: 'var(--chart-hover)' }}` to use the hover token, or `cursor={false}` to disable the cursor highlight entirely and rely on `<ChartTooltipCard>` alone for hover feedback. Never rely on recharts default cursor for BarChart.

### Inline-injected

{{#if style_meta.decorative_pack == "editorial"}}
**ChartTooltipCard** — Custom chart tooltip.

```tsx
function ChartTooltipCard({
  active, payload, label,
  periodSuffix = "",
  unitSuffix = "",
}: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="px-4 py-3" style={{
      background: "var(--surface-l2)", borderRadius: 12,
      boxShadow: "0 4px 16px rgba(0,0,0,0.06)", minWidth: 140,
    }}>
      <div className="text-[10px] uppercase mb-2" style={{
        fontFamily: "'Geist Mono', monospace",
        letterSpacing: "{{atomic.typography.eyebrow_tracking_em}}em", color: "var(--foreground-3)",
      }}>{label} {periodSuffix}</div>
      {payload.map((entry, i) => (
        <div key={entry.dataKey ?? i} className="flex items-center gap-2">
          <span className="block size-2 rounded-full" style={{ background: "var(--primary)" }} aria-hidden />
          <span className="text-[15px] font-medium" style={{ color: "var(--foreground)" }}>{entry.value}</span>
          <span className="text-[12px] font-normal" style={{ color: "var(--foreground-3)" }}>{unitSuffix}</span>
        </div>
      ))}
    </div>
  );
}
// Wire: <Tooltip content={(p) => <ChartTooltipCard {...p} periodSuffix="年" unitSuffix="亿元" />} />
```

`borderRadius: 12` (< card chrome 16). No border. Cursor: brand dashed 0.5 opacity.

**DeltaIndicator** — Inline glyph, no pill/border/background. Up: `▲` `--primary-hl`; down: `▼` `--foreground-2`. `text-[13px] md:text-[14px] font-medium whitespace-nowrap`. Arrow `0.85em`, optional label `font-normal opacity-80`.

**Hero ember wash** — CSS radial `var(--ember-wash)` 800×600 at `top:38%` `z:15`. Outro mirrors 600×400 at `top:55%`.

**ChapterStamp** — Inline-flex column: `No.` 10px 500 `tracking-[0.08em]` `--foreground-3` + numeral 18px 500 `--primary`. Mono. Zero-padded. ≤ 3× per page.

**ChapterBanner** — `--border-strong` hairline + `CHAPTER · NN` `text-[11px] md:text-[12px]` `tracking-[{{atomic.typography.eyebrow_tracking_em}}em]` `--primary` + bilingual label `tracking-[{{atomic.typography.meta_tracking_em}}em]` `--foreground-3` + title `text-[34px] md:text-[44px] lg:text-[{{atomic.typography.section_primary_lg}}px] font-medium tracking-[-0.03em]` `--foreground`. `whileInView` + `viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}`, `duration: 1.2, ease: EASE.spring`.

**ChapterDivider** — `1px --border` + `· · ·` Mono `text-[13px] tracking-[0.8em] --foreground-3`. At most once within a chapter.

**QuoteBracket** — SVG 40×40 L-shape: `stroke="var(--primary)" strokeWidth="1" strokeOpacity="0.6" strokeLinecap="square" fill="none"`. Top-left `M 2 38 L 2 2 L 38 2`; bottom-right `M 38 2 L 38 38 L 2 38`.

**OutroSignature** — Two brand hairlines + diamond rotate 0→45°.
```tsx
function OutroSignature() {
  return (
    <div className="relative z-10 mt-24 flex items-center justify-center gap-6" aria-hidden>
      <motion.span initial={{ scaleX: 0 }} whileInView={{ scaleX: 1 }}
        viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}
        transition={{ duration: 1.0, ease: EASE.out, delay: 0.7 }}
        className="block h-px w-32 md:w-40 origin-right" style={{ background: "var(--primary)" }} />
      <motion.span initial={{ rotate: 0, opacity: 0 }} whileInView={{ rotate: 45, opacity: 1 }}
        viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}
        transition={{ duration: 0.8, ease: EASE.out, delay: 0.9 }}
        className="block size-2" style={{ background: "var(--primary)" }} />
      <motion.span initial={{ scaleX: 0 }} whileInView={{ scaleX: 1 }}
        viewport={{ once: true, margin: "{{atomic.motion_timing.inview_margin}}" }}
        transition={{ duration: 1.0, ease: EASE.out, delay: 0.7 }}
        className="block h-px w-32 md:w-40 origin-left" style={{ background: "var(--primary)" }} />
    </div>
  );
}
```
Colophon below: `text-[12px] font-medium uppercase tracking-[0.20em]` Mono `--foreground-3`.

**Tags** — Shadcn `Badge variant="outline"`. Brand hover: `hover:bg-[color:var(--ember-wash)]`.
{{/if}}

{{#if style_meta.decorative_pack == "theatrical"}}
**DeltaIndicator** — Pill with thin border.

```tsx
function DeltaIndicator({ direction, value }: { direction: "up" | "down"; value: string }) {
  const isUp = direction === "up";
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-[4px]"
      style={{
        border: "1px solid var(--border-strong)",
        background: "var(--surface-l2)",
        color: isUp ? "var(--primary)" : "var(--foreground-2)",
      }}>
      <span className="text-[12px] font-semibold">{isUp ? "▲" : "▼"}</span>
      <span className="text-[13px] font-medium">{value}</span>
    </span>
  );
}
```

**ChapterStamp** — SVG circular badge: 1.5px `--primary` border ring (40×40), centered mono numeral `font-semibold` `--primary`. Optional bilingual label below, mono `tracking-[{{atomic.typography.eyebrow_tracking_em}}em] --foreground-3`.

**Double-Bezel card** — Outer `p-1.5 ring-1 ring-white/5 rounded-[6px]` → inner `rounded-[4px] bg-surface-l2 p-6 md:p-8`. Cluster cells use this exclusively.

**Tags** — Shadcn `Badge variant="outline"`. Brand hover: thin border ring on `--surface-l2` background.

**Tooltip contentStyle** — Use inline `contentStyle={{ background: "var(--surface-l2)", border: "1px solid var(--border-strong)", color: "var(--foreground)", borderRadius: 4 }}` directly on `<Tooltip />`.
{{/if}}

{{#if style_meta.decorative_pack == "instrumental"}}
**DeltaIndicator** — Pill with thin border, instrument-panel signal.

```tsx
function DeltaIndicator({ direction, value }: { direction: "up" | "down"; value: string }) {
  const isUp = direction === "up";
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-[4px]"
      style={{
        border: "1px solid var(--border-strong)",
        background: "var(--surface-l2)",
        color: isUp ? "var(--primary)" : "var(--foreground-2)",
      }}>
      <span className="text-[12px] font-semibold">{isUp ? "↑" : "↓"}</span>
      <span className="text-[13px] font-medium">{value}</span>
    </span>
  );
}
```

{{#if atomic.motion_timing.spotlight_drift_s}}{{#if molecular.hero_geometry.radial_wash_css}}
**SpotlightGradient** — Hero overlay above shader, below text. CSS radial with slow drift, `{{atomic.motion_timing.spotlight_drift_s}}s/cycle infinite`, paused via reduced-motion.

```tsx
function SpotlightGradient() {
  return (
    <div className="absolute inset-0 pointer-events-none" style={{ zIndex: 15 }} aria-hidden>
      <div style={{
        position: "absolute", inset: 0,
        background: "{{molecular.hero_geometry.radial_wash_css}}",
        animation: "spotlight-drift {{atomic.motion_timing.spotlight_drift_s}}s ease-in-out infinite alternate",
      }} />
    </div>
  );
}
```
{{/if}}{{/if}}

**ChapterStamp** — SVG circular badge: 1.25px `--primary` border ring (40×40), centered mono numeral `font-semibold` `--primary`. Optional bilingual label below.

**Drawn-horizon SVG line** — Hero anchor line (Design Tokens preview only; Report Example does not render). `<motion.line>` `var(--primary)` 1px stroke, `pathLength: 0→1`, `delay 0.4s, duration {{atomic.motion_timing.curve_path_s_range.1}}s, ease: EASE.out`. Placed at Hero focal y-coordinate, full-bleed width.

**Page noise overlay** — `<svg>` element fixed `inset-0 z-1 pointer-events-none`, `<filter>` with `<feTurbulence baseFrequency="0.65" numOctaves="3" />` + `<feColorMatrix>` desaturate, full-page `<rect fill="url(#noise)" opacity="0.1" />` mix-blend-mode overlay. Renders once, never animates.

**Tooltip contentStyle** — Use inline `contentStyle={{ background: "var(--surface-l2)", border: "1px solid var(--border-strong)", color: "var(--foreground)", borderRadius: 4 }}` directly on `<Tooltip />`.
{{/if}}

{{#if style_meta.decorative_pack == "systematic"}}
**ChapterBanner** — Shadcn `Badge variant="outline"` chapter index (mono ALL-CAPS `01` / `02` / `03`, sans 700, `border-strong` outline) + ALL-CAPS chapter title sans 700 to the right + `ShadSeparator` (Radix-based) full-width below. No SVG, no solid-fill, no kicker.

**ShadSeparator** — Radix-based separator (`@radix-ui/react-separator`), full-width 1px rule, no gradient, no dot, no fade. Use the shadcn `<Separator />` primitive — token-styled per pack.

**SharpTag** — Replaces pill / `Badge`. **Sharp 0px corner radius** outline only. Thin border + sans 500 label.

```tsx
function SharpTag({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex items-center px-2 py-0.5"
      style={{
        border: "1px solid var(--border-strong)",
        borderRadius: 0,
        fontSize: 12, fontWeight: 500,
        color: "var(--foreground-2)", background: "transparent",
      }}>{children}</span>
  );
}
```

**Inline DeltaIndicator** — No pill, no border, no background. Sans 700 weight character + value. Up: `▲` `--primary`; down: `▼` `--foreground-2`.

```tsx
function DeltaIndicator({ direction, value }: { direction: "up" | "down"; value: string }) {
  const isUp = direction === "up";
  return (
    <span className="inline-flex items-baseline gap-1 whitespace-nowrap">
      <span style={{ fontWeight: 700, color: isUp ? "var(--primary)" : "var(--foreground-2)" }}>{isUp ? "▲" : "▼"} {value}</span>
    </span>
  );
}
```

**Systematic discipline (Swiss / IBM)** — Page-wide 0px corner radius (no `rounded-*` anywhere). Hairline-only depth: no `box-shadow`, no `backdrop-blur`, no `noise overlay`, no `drawn-horizon`, no `SpotlightGradient`, no `OutroSignature`. ALL CAPS reserved for Hero focal title and eyebrows only. Hero background is the static CSS dot-grid layer (above), not a WebGL shader.

**Tooltip contentStyle** — Use inline `contentStyle={{ background: "var(--surface-l1)", border: "1px solid var(--border-strong)", color: "var(--foreground)", borderRadius: 0 }}` directly on `<Tooltip />`. Sharp corner, no shadow.
{{/if}}

{{#if style_meta.decorative_pack == "festive-royal"}}
**SealStamp** — SVG solid-fill square or circle (28-40px). No border ring. `fill="var(--primary)"`. Centered serif numeral 700 weight in `var(--background)` color (reverse). Optional bilingual ceremonial label below (e.g. `第一章 · CHAPTER ONE`) `--foreground` serif `font-medium`. One per chapter opener. Hero section never receives a SealStamp (Hero ≠ chapter).

```tsx
function SealStamp({ n, label }: { n: string; label?: string }) {
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="36" height="36" viewBox="0 0 36 36" aria-hidden>
        <rect width="36" height="36" rx="2" fill="var(--primary)" />
        <text x="18" y="25" textAnchor="middle"
          fontFamily="'Cormorant Garamond', 'Noto Serif SC', serif"
          fontWeight="700" fontSize="18" fill="var(--background)">{n}</text>
      </svg>
      {label && <span style={{ fontSize: 11, fontWeight: 500, color: "var(--foreground)", fontFamily: "'Cormorant Garamond', serif", letterSpacing: "0.14em" }}>{label}</span>}
    </div>
  );
}
```

**GoldenHairline** — Full-width 1px rule, gold primary at 0.4 alpha. Replaces HairlineRule for festive-royal chapters.

```tsx
function GoldenHairline() {
  return <hr style={{ border: "none", borderTop: "1px solid oklch(var(--primary) / 0.4)", margin: 0 }} aria-hidden />;
}
```

**Inline DeltaIndicator** — No pill, no border, no background. Serif 700 weight character + value. Up: `▲` `--primary`; down: `▼` `--foreground-2`.

```tsx
function DeltaIndicator({ direction, value }: { direction: "up" | "down"; value: string }) {
  const isUp = direction === "up";
  return (
    <span className="inline-flex items-baseline gap-1 whitespace-nowrap">
      <span style={{ fontWeight: 700, fontFamily: "'Cormorant Garamond', serif", color: isUp ? "var(--primary)" : "var(--foreground-2)" }}>{isUp ? "▲" : "▼"} {value}</span>
    </span>
  );
}
```

**ChartTooltipCard** — Custom chart tooltip with gold border on muted crimson background.

```tsx
function ChartTooltipCard({ active, payload, label, periodSuffix = "", unitSuffix = "" }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: "var(--surface-l2)", border: "1px solid oklch(var(--primary) / 0.4)",
      borderRadius: 2, padding: "12px 16px", minWidth: 140,
    }}>
      <div style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: 11, letterSpacing: "0.14em", color: "var(--foreground-3)", marginBottom: 8 }}>{label} {periodSuffix}</div>
      {payload.map((entry: any, i: number) => (
        <div key={entry.dataKey ?? i} style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ display: "block", width: 8, height: 8, background: "var(--primary)", borderRadius: 0 }} aria-hidden />
          <span style={{ fontSize: 15, fontWeight: 700, color: "var(--foreground)", fontFamily: "'Cormorant Garamond', serif" }}>{entry.value}</span>
          <span style={{ fontSize: 12, color: "var(--foreground-3)" }}>{unitSuffix}</span>
        </div>
      ))}
    </div>
  );
}
```

**Tags** — `SharpTag` style: `inline-flex items-center px-2 py-0.5` sharp 2px corner radius, `1px solid var(--border-strong)`, serif `font-medium`, no pill, no rounded-full.

**Festive-Royal discipline** — Full chromatic crimson ground. Gold hairline-only depth: no `box-shadow`, no `backdrop-blur`, no `noise overlay`, no `SpotlightGradient`, no editorial `OutroSignature`, no theatrical double-bezel. All type uses declared serif stack (Cormorant Garamond / Noto Serif SC). ALL-CAPS not used (Royal register uses sentence case with tracking). Hero uses GrainGradient shader + `radial_wash_css` gold focal wash. Chapter opener SealStamp + GoldenHairline rule every non-Hero chapter.

**Tooltip** — Use `<ChartTooltipCard />` custom component. No `contentStyle` plain inline — festive-royal always uses the gold-border custom card.
{{/if}}

{{#if style_meta.decorative_pack == "festive-editorial"}}
**ChapterNumeralLarge** — Chapter index numeral rendered at Section Primary scale or larger. No SVG, no ring, no badge — pure text. Crimson primary color, 800 weight sans, baseline-aligned next to chapter title.

```tsx
function ChapterNumeralLarge({ n }: { n: string }) {
  return (
    <span style={{
      color: 'var(--primary)',
      fontWeight: 800,
      fontSize: 'clamp(64px, 8vw, 96px)',
      lineHeight: 0.9,
      letterSpacing: '-0.04em',
      fontFamily: 'var(--display-stack)',
    }}>{n}</span>
  );
}
```

**HairlineRule** — Full-width 1px rule. No gradient, no dot, no fade.

```tsx
function HairlineRule() {
  return <hr style={{ border: 'none', borderTop: '1px solid var(--border-strong)', margin: 0 }} aria-hidden />;
}
```

**SharpTag** — Sharp 0px corner radius outline only. No fill, no pill.

```tsx
function SharpTag({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex items-center px-2 py-0.5"
      style={{
        border: '1px solid var(--border-strong)',
        borderRadius: 0,
        fontSize: 12, fontWeight: 500,
        color: 'var(--foreground-2)', background: 'transparent',
      }}>{children}</span>
  );
}
```

**Inline DeltaIndicator** — No pill, no border, no background. Sans 800 weight character + value. Up: `▲` `--primary`; down: `▼` `--foreground-2`.

```tsx
function DeltaIndicator({ direction, value }: { direction: 'up' | 'down'; value: string }) {
  const isUp = direction === 'up';
  return (
    <span className="inline-flex items-baseline gap-1 whitespace-nowrap">
      <span style={{ fontWeight: 800, color: isUp ? 'var(--primary)' : 'var(--foreground-2)' }}>{isUp ? '▲' : '▼'} {value}</span>
    </span>
  );
}
```

**ChartTooltipCard** — Content-style: white/ivory background + black text. No gold border.

```tsx
function ChartTooltipCard({ active, payload, label, periodSuffix = '', unitSuffix = '' }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'var(--surface-l1)', border: '1px solid var(--border-strong)',
      borderRadius: 0, padding: '12px 16px', minWidth: 140,
    }}>
      <div style={{ fontFamily: 'var(--display-stack)', fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'var(--foreground-3)', marginBottom: 8 }}>{label} {periodSuffix}</div>
      {payload.map((entry: any, i: number) => (
        <div key={entry.dataKey ?? i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ display: 'block', width: 8, height: 8, background: 'var(--primary)', borderRadius: 0 }} aria-hidden />
          <span style={{ fontSize: 15, fontWeight: 800, color: 'var(--foreground)' }}>{entry.value}</span>
          <span style={{ fontSize: 12, color: 'var(--foreground-3)' }}>{unitSuffix}</span>
        </div>
      ))}
    </div>
  );
}
```

**Festive-Editorial discipline** — Light ivory ground. Hairline-only depth: no `box-shadow`, no `backdrop-blur`, no `noise overlay`, no `SpotlightGradient`, no `OutroSignature`, no theatrical double-bezel, no systematic Dithering, no festive-royal SealStamp / GoldenHairline. All type uses declared sans stack (Helvetica Neue / IBM Plex Sans / Inter / Noto Sans SC). 0px corner radius everywhere. Hero uses GrainGradient red shader; Hero ≠ chapter (no ChapterNumeralLarge in Hero). Chapter opener ChapterNumeralLarge + HairlineRule every non-Hero chapter.

**Tooltip** — Use `<ChartTooltipCard />` custom component with white bg + black text style.
{{/if}}

**Inline number+unit** — `inline-flex items-baseline gap-2 whitespace-nowrap`. Fits within card padding.

**Focal numeric font-size must scale down for long values** — apply length-based conditional `className` on the focal Display Number derived from `displayNumber.length`: ≤ 7 char default scale (§3 table) / 8–11 char drop one tier / ≥ 12 char drop two tiers. Parent must `min-w-0` AND child `whitespace-nowrap` — `min-w-0` alone makes Grid cells shrink but text won't auto-resize, only `overflow:hidden` truncates (data loss). **Don't** rely on `min-w-0` alone or `clamp()` (sub-pixel jitter degrades AnimateNumber spring per §3).

### Component mapping (non-chart)

| Archetype | Primary |
|---|---|
| Hero | `motion.div` stack {{#if molecular.hero_shader}}+ paper-shaders Hero shader{{/if}}{{#if !molecular.hero_shader}}+ static CSS background layer (dot-grid / line-grid){{/if}} |
| Cluster | {{#if atomic.radius.card_chrome == "double-bezel"}}Double-Bezel cells{{/if}}{{#if atomic.radius.card_chrome != "double-bezel"}}CSS grid card-chrome cells{{/if}} |
| Ranking | Stacked rows or shadcn `Item`+`ItemGroup` |
| Sequence | Shadcn `Item`+`ItemGroup` + track |
| Peer Set | Shadcn `Card` grid (border-0) |
| Quote | `<figure>` + {{#if style_meta.decorative_pack == "editorial"}}SVG brackets{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}lucide Quote{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}lucide Quote{{/if}}{{#if style_meta.decorative_pack == "systematic"}}leading en-dash `—`{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}CJK bracket `「 」` lead-in / lead-out{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}em-dash `—` lead-in / lead-out{{/if}} |
| Outro | `motion.div` + {{#if style_meta.decorative_pack == "editorial"}}`OutroSignature`{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}closing `ChapterStamp` (ring){{/if}}{{#if style_meta.decorative_pack == "instrumental"}}closing `ChapterStamp` + terminal hairline{{/if}}{{#if style_meta.decorative_pack == "systematic"}}terminal `ShadSeparator`{{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}closing solid-fill `SealStamp` (square) + `GoldenHairline`{{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}closing `ChapterNumeralLarge "END"` + `HairlineRule`{{/if}} |
| Loading | Shadcn `Skeleton` |
| Divider | Shadcn `Separator` |
| Tag | {{#if style_meta.decorative_pack == "editorial"}}Shadcn `Badge variant="outline"`{{/if}}{{#if style_meta.decorative_pack == "theatrical"}}Shadcn `Badge variant="outline"`{{/if}}{{#if style_meta.decorative_pack == "instrumental"}}Shadcn `Badge variant="outline"`{{/if}}{{#if style_meta.decorative_pack == "systematic"}}`SharpTag` (sharp 0px corner outline){{/if}}{{#if style_meta.decorative_pack == "festive-royal"}}`SharpTag` (sharp 2px corner, serif — no pill, no rounded-full){{/if}}{{#if style_meta.decorative_pack == "festive-editorial"}}`SharpTag` (sharp 0px corner, sans — no pill, no rounded-full){{/if}} |

## 18. Component Constraints

Use top-level hooks, typed props, `motion/react`, `motion-plus/react`, numeric easing arrays, `aria-hidden` for decorative visuals, semantic labels for readable values, `isAnimationActive={false}` on Recharts, and reduced-motion fallbacks for AnimateNumber{{#if molecular.hero_shader}}, WebGL{{/if}}{{#if atomic.motion_timing.spotlight_drift_s}}, spotlight{{/if}}, and off-screen continuous motion.
