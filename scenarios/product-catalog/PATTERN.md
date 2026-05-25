---
type: pattern-block
scenario: product-catalog
status: stub — ready for designer to fill
based_on: scenarios/campaign-report/PATTERN.md (reference)
---

# PATTERN · product-catalog

> Stub. Designer fills archetype details per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md). Reference the mature [`../campaign-report/PATTERN.md`](../campaign-report/PATTERN.md) for prose tone, density-rule wording, and slot-mapping table format. Reuse the 9 composition treatments and 6 dominant moves verbatim.

A product-catalog page is a **multi-product browse experience** — a structured grid of peers (products, design resources, brands, models) that the visitor scans to pick one. Its job is to give the eye purchase on the set, support filter and sort without overpowering them, and let each card lean on a single focal artifact.

---

## Chapter cadence (5–7 sections)

| # | Chapter | One-line purpose | Required |
|---|---|---|---|
| 1 | **Catalog Hero** | Anchors the catalog identity (collection name, range, count, brief framing line). | required |
| 2 | **Filter Rail** | Filter + sort controls; horizontal rail or sticky sidebar. | required |
| 3 | **Featured Set** | 1–3 hand-picked items, larger cards, before the main grid. | optional |
| 4 | **Catalog Grid** | The main browse grid — N×M ProductCard cells. | required |
| 5 | **Category Breaks** | Optional band dividers between sub-collections inside the grid. | optional |
| 6 | **Pagination / Load More** | Continuation mechanism. | required when N > one viewport |
| 7 | **Outro Reverent** | Closes with collection caveats (period, total count, source, last-updated). | required |

<!-- TODO 设计师: 为每个 chapter 写 archetype 段(Trigger / Slots / Treatments / Dominant Move),参照 campaign-report/PATTERN.md §11.3 体例。Catalog Hero 通常 Typographic Field 而非 Display Number(catalog 不为数字而是为集合服务);Filter Rail 是新 archetype,Slots: facet-labels · facet-values · sort-control;Catalog Grid 是 Peer Set / Catalog 的极致表达,Matrix Grid 6+ 列。 -->

---

## Composition treatments

Reuse the 9 treatments from campaign-report PATTERN §11.1 verbatim.

Favored treatments for product-catalog: **Typographic Field** for the Catalog Hero (catalog identity is a name, not a number), **Annotation Rail** or sticky sidebar for the Filter Rail, **Matrix Grid** for the main Catalog Grid (this is the scenario's signature — equal-weight peer cells), **Stacked Band** for Category Breaks. Avoid Proportion Rail (catalog rarely tells a parts-of-whole story unless filters expose category share — that's a tool, not a page).

---

## Dominant moves

Reuse the 6 dominant moves from campaign-report PATTERN §11.2 verbatim.

Catalog-specific note: **the Matrix Grid leads with steady moves only** — scale jump on Featured Set cells, single stroke on dividers, no crop/bleed on individual cards (cropped cards read as broken images). Disruptive moves stay in the Hero and the Featured Set.

---

## Rhythm discipline

Reuse the four rules from campaign-report PATTERN §12.2 verbatim. Three scenario-specific notes:

- **Grid density** — the Catalog Grid is `dense` by definition. The rest of the page must rotate to `medium` and `spacious` so the grid lands with weight rather than blending into wallpaper.
- **Card chrome consistency** — every ProductCard in one grid uses the same chrome variant. Mixing card chromes inside one grid breaks scan rhythm.
- **No card decoration drift** — hover states, badge styles, price treatments stay identical across every card. The decoration is the data variation, not the chrome variation.

---

## Don'ts (additions to the §16 list)

<!-- TODO 设计师: 加 5-8 条 product-catalog 特定 don't。提示:cards with mixed aspect ratios in one grid / badge overload (Sale + New + Hot 三连击) / 缩略图配 12 个不同颜色的 swatch / filter rail 折叠到 hamburger 在 desktop / "showing 1-24 of 4827 results" 出现在每个 chapter 顶部 / hover lift > 4px。 -->
