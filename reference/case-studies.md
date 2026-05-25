# Case Studies — Specific Bugs and How They Were Solved

> Eleven recurring bug shapes drawn from the example project's Round-Log §2 (R-83 through R-97). Each case is a *recognisable shape* — when you see the same shape in your project, jump to the prevention rule and skip the cost.
>
> Read top-to-bottom once; come back when an iteration round feels familiar. The principles in `99-principles.md` are the general rules; this file is the specific scars.

---

## Case 1 · Shader too loud, fixed with a `backdrop-filter` overlay

**Symptom.** Hero text becomes unreadable because the shader is too saturated or too dark. A sub-agent offers a `backdrop-filter: blur(8px)` div over the shader.

**Root cause.** The shader's own `colorFront` / `colorBack` / `softness` are out of range. The overlay is a hack — it adds a second layer to compensate for the first.

**Solution.** Tune the shader's props *at the source*. Lower `colorFront` lightness, raise `softness`, drop `chroma`, or shift `hue` toward neutral. Remove any wrapper that exists.

**Prevention.** Principle 1 + Principle 8. The shader is the source of truth for the Hero look. Every wrapper layer is debt. If the first tune doesn't go far enough, tune again — don't stop at "I already lowered it once".

(Example project: R-83 #8 Swiss Dithering `#1E3FB0 → #7E94CC`, then R-85 #13 `#7E94CC → #C8CACE` near-neutral. Two rounds of the same lesson.)

---

## Case 2 · Patch one render path, leave six unpatched

**Symptom.** A new pack (e.g. `festive-royal`) gets a custom chapter-opener ornament. Sub-agent's grep shows `isFestiveRoyal ? FestiveRoyalChapterOpener(...) : default` in *one* place. Renderer shows the ornament on chapter 1 only; chapters 2 through 7 still render the default ShadBadge.

**Root cause.** The page has N independent render branches (one per chapter, or one per view, or one per device). Sub-agent assumes "if the pattern is established in one branch, the others will naturally follow". They don't — each branch is a separate code path that must be touched.

**Solution.** Enumerate every render branch (`grep -nE 'function render.*<thing>|className.*<thing>-opener' <file>`) and patch each. Verify with a DOM count: `document.querySelectorAll('.rep-chapter-opener.<pack>').length === 7`.

**Prevention.** Principle 9. Sub-agent prompts must say "Enumerate every render path. Grep `function render.*Hero|className.*chapter-opener` and list the line numbers. Patch each. Report the count."

(Example project: R-90 #24 festive-royal 6 chapters unpatched. R-87 #18 ShadCard children prop dropped in 9 sites.)

---

## Case 3 · Inline data drifts from the external Slot

**Symptom.** Chris reloads the page and reports "the Hero shader colour didn't change". You re-grep the external Slot and confirm the new value is there. The renderer is still showing the old colour.

**Root cause.** The renderer has *two* Slot data sources: the external `<style>.slot.json` (Slot of truth) and an inline copy in the HTML / Vite component (for fast prototyping). The external Slot was patched but the inline copy was not.

**Solution.** Sync the inline data to the external Slot every time. Better: write a small script that asserts equality and runs in CI / pre-commit.

**Prevention.** Principle 9 + sync chain step 2 in `08-iterate.md`. This is the **single most-missed step** in the example project's iteration history — R-83, R-84, R-85, R-90 all stumbled on inline-vs-external drift.

(Example project: R-84 #11 — Cowork only patched `buildHeroCorner` for M-04 Design System, missed the M-08 Report Hero's separate IIFE *and* missed the inline `data-swiss` JSON. Same lesson, three sites.)

---

## Case 4 · Sub-agent claims "PASS", Cowork accepts, Chris finds the bug

**Symptom.** A sub-agent returns "all 6 styles verified, anti-slop 0 violations". Cowork accepts. Chris opens the renderer and points at an obvious filled-card with a border on it.

**Root cause.** The sub-agent did the work, then graded its own work with a softer eye than Cowork would. Sometimes the sub-agent argued away a real violation ("the active indicator is not a card double-decoration") and Cowork accepted the argument.

**Solution.** Cowork runs the same greps + DOM evals the sub-agent ran, independently. When the Slop Taxonomy detector flags a violation, the violation stands — sub-agent explanations do not exempt it.

**Prevention.** `02-roles.md` §After a sub-agent returns + Principle 9. The Slop Taxonomy is a *Blocking* gate; arguments do not override Blocking findings.

(Example project: R-87 #18 Cowork accepted "active indicator" framing; R-89 #22 Chris ruled it slop anyway. R-94 #35 inverse: Cowork wrongly accused the sub-agent of hallucination because Cowork's verify ran against the wrong path — see Case 5.)

---

## Case 5 · "Sub-agent hallucinated" — actually wrote to canonical path

**Symptom.** Sub-agent reports a long file list of produced files. Cowork runs `ls -la` on the sub-agent's worktree CWD and sees only `node_modules + bun.lock + a stub package.json`. Cowork records "sub-agent hallucination" and starts re-dispatching.

**Root cause.** The sub-agent used absolute paths to Edit/Write — those writes landed in the canonical project location (`/Users/.../Code/<project>/...`), not in the worktree CWD. Worktree isolation affects bash CWD and git branch; it does *not* affect where Edit/Write puts files when the tool is given an absolute path.

**Solution.** Run `ls -la <absolute canonical path>` instead. The sub-agent's work is there. Then patch the sub-agent prompt to require both `ls -la <abs canonical>` and `wc -l <abs canonical>` as verify proof.

**Prevention.** `02-roles.md` §D Verify proof requirements. Always pass absolute canonical paths to sub-agents and require them to report back from the same absolute path. Cowork's verify must match the destination, not the CWD.

(Example project: R-94 #35. Cowork wrongly accused a sub-agent who had actually completed 95 % of the work — the costliest mis-judgement of the project.)

---

## Case 6 · CSS pattern works in pack X, missing in pack Y

**Symptom.** Pack X (festive-royal) has `.rep-chapter-opener { flex-direction: column; align-items: flex-start; gap: 12px }`. Pack Y (festive-editorial) was added later by a different sub-agent. Pack Y's chapter title now wraps awkwardly — the row is squashed because the inherited `display: flex` puts the hairline and the title-row side by side.

**Root cause.** The new sub-agent worked from the spec for pack Y, never read pack X's per-pack CSS, and missed the structural override that pack X had already discovered the hard way.

**Solution.** When adding a new pack with a similar structure to an existing one, *list* every per-pack CSS rule in the analogous pack and confirm each is mirrored. The override list is part of the brief, not an unstated assumption.

**Prevention.** `02-roles.md` §Common failure modes — "list every CSS rule in pack X's per-pack block and confirm each is mirrored to pack Y". The cost of forgetting is one full iteration round.

(Example project: R-91 #25 festive-editorial missed `flex-direction: column` mirror — visible only after a render-time inspection.)

---

## Case 7 · `var(--primary)` doesn't mean the colour you think

**Symptom.** New ornament (e.g. an "imprint" SVG) is meant to be cinnabar red. CSS says `fill: var(--primary)`. The renderer shows a gold square instead.

**Root cause.** Brand tokens are pack-scoped and pack-specific. The pack's `--primary` happens to be gold in this style (it's the focal numeral colour, not a "red brand" colour). The ornament needs a value that's independent of the pack's `--primary`.

**Solution.** Either (a) hard-code the historical colour (`fill: #9D2933` for cinnabar) with a comment explaining why, or (b) introduce a new token (`--ornament-imprint-bg`) and declare it per-pack. Option (a) is right for one-off historical pigments; option (b) is right when the value will recur.

**Prevention.** Before using `var(--primary)` in a new ornament, verify the token's actual OKLCH for *that pack*. Brand tokens carry semantic weight (focal colour, default delta colour) — they do not carry decorative semantics (red / blue / gold).

(Example project: R-92 #26 issue 2 — Cinnabar Imprint rendered gold because `--primary` in festive-royal is gold.)

---

## Case 8 · `:not()` exclusion list misses the new child

**Symptom.** A new absolute-positioned child element is added to `.rep-hero`. It renders in the wrong layer (behind or shifted) because a parent rule like `.rep-hero > *:not(.rep-hero-shader):not(.rep-hero-corner) { position: relative; z-index: 2 }` is overriding its own `position: absolute`.

**Root cause.** The parent has a `:not()` whitelist that fights any new child. The whitelist was written for the children that existed at the time; the new child is implicitly forced into "relative + z-index 2".

**Solution.** Add the new child's selector to the `:not()` exclusion list.

**Prevention.** When adding any absolute-positioned child to a styled container, grep the parent's CSS for `:not(` and confirm the exclusion list is up to date. CSS specificity is a quiet enemy — the only sign of failure is a wrong visual position.

(Example project: R-92 #26 issue 1 — Cinnabar Imprint forced into `position: relative` until added to the `:not()` chain.)

---

## Case 9 · Template branch contradicts the Slot

**Symptom.** Slot says `weight_ceiling: 500`. Template says `font-extrabold (800)` for Hero Display Number. The produced Design Prompt md ships with the contradiction; downstream weak-model output is unpredictable.

**Root cause.** The Slot was patched (e.g. R-93 #29 lowered the ceiling) but the template's *other* branches were not updated. The injector renders both: the new Slot value *and* the old template branch text.

**Solution.** When changing any Slot constraint, grep the template for the old constraint value (`grep -nE 'extrabold|800|weight-800' <template>`) and fix every match. Re-inject the affected style. Three-way sync audit catches what the grep misses.

**Prevention.** Principle 12 + `08-iterate.md` §5 template branch change. Every Slot edit is followed by a `grep <old-value> <template>` for stale references — *then* re-inject.

(Example project: R-95 #41 — Festive Editorial Slot lowered `weight_ceiling 800 → 500`, template branches still said 800 *and* still referenced the deleted `END` outro element. Two contradictions in one round.)

---

## Case 10 · Fixing A breaks B (alignment trade-off)

**Symptom.** A round fixes "Timeline horizontal line doesn't pass through the dot centres". The next round reports "the dots are no longer left-aligned with their titles".

**Root cause.** The fix changed `.rep-tl-dot { align-self: center }` to align the dot's X with the line's endpoint X — which also broke the existing alignment between dot X and title X (titles were left-aligned to the cell).

**Solution.** When fixing one geometric constraint, verify the other geometric constraints in the same component. The fix has a trade-off; you must look for it explicitly.

**Prevention.** Principle 9 (multi-dimensional alignment). After any layout patch, sweep adjacent alignment relations — left-align, baseline-align, end-align — and screenshot each.

(Example project: R-85 #14 fixed line-through-dot; R-86 #15 caught the dot-vs-title regression. The fix was `align-self: flex-start` + adjust `left` and `right` on the `::before`.)

---

## Case 11 · Demo paths leak into the Skill's general docs

**Symptom.** While writing the Skill's general reference docs, the author hard-codes paths like `_Framework/design-system-renderer-vite/src/data/festive-royal.slot.json`. The user of the Skill (a different project) hits the docs and reads instructions that reference paths that don't exist in their project.

**Root cause.** When the Skill author is also the example project's maintainer, the example project's filesystem starts to feel canonical. Demo-specific paths leak into general prose.

**Solution.** Replace demo paths with placeholders (`<renderer>/src/data/<style>.slot.json`) and / or point readers to the example project explicitly: "see `examples/vibe-view-campaign-report/<path>` for a concrete instance".

**Prevention.** Treat the example project as one *instance* of the Skill, not the canonical filesystem. Skill docs use placeholders; example project docs use concrete paths. Cross-reference, do not merge.

(Example project: R-97 — Phase 8 Cowork docs accidentally mixed demo paths into general Skill prose. The fix was to extract the example into `examples/vibe-view-campaign-report/` and rewrite the general docs in placeholder form.)
