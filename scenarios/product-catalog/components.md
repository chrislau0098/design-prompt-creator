---
type: component-spec
scenario: product-catalog
status: stub — ready for designer to fill
---

# Component Spec · product-catalog

> Stub. Designer fills component details per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md). Reference [`../campaign-report/components.md`](../campaign-report/components.md) for prose tone (Purpose / Props / DOM / Variants / Adaptive states / Banned).

**Three-library limit**: every component composes from **shadcn/ui**, **motion**, and **paper-shaders** (Catalog Hero background only). No carousel libraries, no grid frameworks beyond Tailwind.

---

## Required Components

### CatalogHero

**Purpose**: Catalog Hero archetype. Anchors collection identity (name, range, item count, brief framing line).

<!-- TODO 设计师: 写 props (collectionName / framingLine? / itemCount? / heroVisual?) + DOM + 变体 (Typographic Field default / Asymmetric Split with visual / Full-bleed Monolith for hero collections) + adaptive states (loading: skeleton on count; empty collection: render Hero with "Collection coming soon" framing)。Note: 通常**不**用 Display Number — catalog 的焦点是集合身份不是单一数字。 -->

---

### FilterRail

**Purpose**: Filter + sort controls. Horizontal rail above grid or sticky sidebar to grid's left.

<!-- TODO 设计师: 写 props (facets: Array<{ label / values / type: 'multi' | 'single' | 'range' }> / sortOptions / activeFilters / onChange) + DOM + 变体 (top-rail / sidebar-sticky) + adaptive states (no active filters: hide "Clear all"; loading: skeleton on facet counts)。Note: filter chip 数量 ≤ 8 在 top-rail 模式;超过走 sidebar。 -->

---

### ProductCard

**Purpose**: One peer cell inside the Catalog Grid (Matrix Grid). The scenario's most-repeated component.

<!-- TODO 设计师: 写 props (image / title / attribute? / value? / badge? / hoverState?) + DOM + 变体 (default / featured (Featured Set, larger) / compact (dense mode)) + adaptive states (loading: skeleton image + text; empty image: foreground-3 placeholder, no broken-image icon; sold-out: opacity adjust + badge)。Hover: lift ≤ 4px, no scale > 1.02, no rotation。 -->

---

### CatalogGrid

**Purpose**: The Matrix Grid container. Holds N ProductCard cells; handles responsive column count.

<!-- TODO 设计师: 写 props (items / columns: { lg / md / sm } / cardVariant: 'default' | 'compact' / featuredCount: number) + DOM + 变体 (4-col default / 3-col tablet / 2-col mobile / 6-col dense for thumbnail catalogs) + adaptive states (empty: render 1 ChapterOpener-style empty message; partial load: keep card slots, show 4-8 skeleton cards)。 -->

---

### Pagination

**Purpose**: Continuation mechanism. Either page-numbered or Load-More button — pick one per page, never both.

<!-- TODO 设计师: 写 props (mode: 'page' | 'load-more' / current / total / onChange) + DOM + 变体 (page-numbered minimal / page-numbered with first-last / load-more single button) + adaptive states (only 1 page: hide entirely; loading: spinner inside Load More button, never outside it)。 -->

---

### Outro

**Purpose**: Outro Reverent — closes the catalog page with caveats (period, total count, source, last-updated).

<!-- TODO 设计师: 参照 [`../campaign-report/components.md`](../campaign-report/components.md) Outro — 同一 component,product-catalog 复用,caveat 内容变 ("Showing X of Y items · Last updated YYYY-MM-DD · Source")。 -->

---

## Banned Components

- Hero carousels at the top of the catalog — visitor came to browse, not watch.
- Cards with mixed aspect ratios in one grid — breaks scan rhythm.
- Quick-view modal triggered by hover — pre-click drawer is a tool, not a marketing pattern.
- Wishlist heart icons at Section Primary scale — affordance, not focal.
- "X people are viewing this now" fake-urgency badges.
- Auto-scroll on Load More — strips reader agency.

<!-- TODO 设计师: 加场景特定 ban,参照 campaign-report/components.md banned list 体例。 -->
