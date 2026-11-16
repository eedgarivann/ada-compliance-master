---
name: wcag22-criteria-test-map
description: "Use this when testing or designing against WCAG 2.2 A/AA: every success criterion's meaning, test method (axe rule ids and manual checks), typical failure-to-fix, plus ACT coverage, non-web ICT and APG patterns."
---

# WCAG 2.2 criteria test map

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) (5 Oct 2023, upd. 12 Dec 2024): all **55 A/AA** SCs. **4.1.1 Parsing** obsolete in 2.2: don't score (2.0/2.1 policies may; ID clashes breaking labels fail 1.3.1/4.1.2). **New** at A/AA: 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8 (AAA out of scope: 2.4.12, 2.4.13, 3.3.9). axe tags `wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa` find *some* failures; pass ≠ conformance.
SC (level) | test (axe ids/manual) | failure→fix.

## Perceivable
- 1.1.1 Non-text Content (A) | axe `*-alt` rules + each non-empty alt vs pixels (placeholder, "bullet", stale) + informative CSS backgrounds | missing/filename alt→purpose alt; decorative `alt=""`.
- 1.2.1 Audio-only and Video-only (Prerecorded) (A) | manual | no alternative→transcript/audio.
- 1.2.2 Captions (Prerecorded) (A) | `video-caption` (track only) + watch | unreviewed auto-captions→accurate captions.
- 1.2.3 Audio Description or Media Alternative (Prerecorded) (A) | manual, sound only | visuals unspoken→AD or full transcript.
- 1.2.4 Captions (Live) (AA) | manual | live with no captions→CART/platform captions.
- 1.2.5 Audio Description (Prerecorded) (AA) | manual | transcript only→AD track/described version.
- 1.3.1 Info and Relationships (A) | axe list, table-header, `aria-required-*` rules | fake headings/lists, layout tables→semantic markup.
- 1.3.2 Meaningful Sequence (A) | `bypass-order` | mismatch→fix DOM.
- 1.3.3 Sensory Characteristics (A) | manual | shape/colour/position-only→add text.
- 1.3.4 Orientation (AA) | `css-orientation-lock`; rotate | locked→remove.
- 1.3.5 Identify Input Purpose (AA) | `autocomplete-valid` (checks only present tokens) + `forms` | missing tokens→autocomplete values.
- 1.4.1 Use of Color (A) | `link-in-text-block` + grayscale | colour-only errors/links/required (links: hover + focus cue, G183)→text, underline, icon.
- 1.4.2 Audio Control (A) | `no-autoplay-audio` + manual | autoplay sound >3 s→no autoplay or pause/mute.
- 1.4.3 Contrast (Minimum) (AA) | `color-contrast`; recheck images/gradients | <4.5:1 (3:1 large: 18pt/14pt bold)→darken, scrim.
- 1.4.4 Resize Text (AA) | `meta-viewport` + 200% zoom | zoom locked/clipped→allow scaling, relative units.
- 1.4.5 Images of Text (AA) | manual | text in images→real text.
- 1.4.10 Reflow (AA) | manual 320 px | two-axis scroll (maps/tables/video exempt)→responsive stack.
- 1.4.11 Non-text Contrast (AA) | manual | controls/icons/focus rings <3:1→darken.
- 1.4.12 Text Spacing (AA) | `avoid-inline-spacing` + inject lh 1.5/para 2em/letter 0.12em/word 0.16em | clipping→flexible heights.
- 1.4.13 Content on Hover or Focus (AA) | manual | vanishing popups→dismissible, hoverable, persistent.

## Operable
- 2.1.1 Keyboard (A) | `scrollable-region-focusable`, `frame-focusable-content` + keyboard pass | click-only divs, pickers→native/APG keys.
- 2.1.2 No Keyboard Trap (A) | manual | embed/modal/chat trap→exit + restore focus.
- 2.1.4 Character Key Shortcuts (A) | manual | single-key shortcuts→off/remap/modifier/focus-only.
- 2.2.1 Timing Adjustable (A) | `meta-refresh` + `context-change --idle` | no extension→off, adjust 10×, or warn ≥20 s, ≥10 extends (real-time/essential/20 h exempt).
- 2.2.2 Pause, Stop, Hide (A) | `blink`, `marquee` + manual | auto motion >5 s, no pause→pause control.
- 2.3.1 Three Flashes or Below Threshold (A) | manual | >3 flashes/s→remove/slow.
- 2.4.1 Bypass Blocks (A) | `bypass-order` | no skip link, landmarks or headings, or broken skip target→skip link (visible on focus) to `main`.
- 2.4.2 Page Titled (A) | `document-title` + `sample-compare` (≥3 pages) | generic titles→descriptive unique.
- 2.4.3 Focus Order (A) | `journeys` + manual | dialog focus not moved, hidden items focusable→manage focus, inert.
- 2.4.4 Link Purpose (In Context) (A) | `link-name`, `area-alt` + manual | "Learn more" ×n→unique names.
- 2.4.5 Multiple Ways (AA) | manual (process steps exempt) | nav only→search/sitemap.
- 2.4.6 Headings and Labels (AA) | manual + `FAKE-HEADING?` | vague, or styled text instead of headings→descriptive real headings.
- 2.4.7 Focus Visible (AA) | manual | `outline:0`→`:focus-visible` meeting 1.4.11.
- 2.4.11 Focus Not Obscured (Minimum) (AA) | manual (sticky/cookie/chat) | focus *entirely* hidden→`scroll-margin`.
- 2.5.1 Pointer Gestures (A) | manual | swipe/pinch/path-only→single-pointer buttons.
- 2.5.2 Pointer Cancellation (A) | manual drag-off | fires on down→activate on up/abort.
- 2.5.3 Label in Name (A) | `label-content-name-mismatch` | aria-label ≠ visible text→name starts with visible text.
- 2.5.4 Motion Actuation (A) | manual | shake/tilt-only→UI control, disable motion.
- 2.5.7 Dragging Movements (AA) | manual | drag-only slider/reorder→buttons/input.
- 2.5.8 Target Size (Minimum) (AA) | `target-size` | <24×24 px, no spacing (exceptions: inline, UA, essential, equivalent)→enlarge/space.

## Understandable
- 3.1.1 Language of Page (A) | axe `html-lang*` rules | missing/wrong→`<html lang>`.
- 3.1.2 Language of Parts (AA) | `valid-lang` + manual | unmarked passages→`lang` attribute.
- 3.2.1 On Focus (A) | `context-change` | focus changes context; script blur on focus (F55, also 2.1.1/2.4.7)→act on activation only.
- 3.2.2 On Input (A) | `context-change` + arrows | auto-submit/reload on change→button or prior warning.
- 3.2.3 Consistent Navigation (AA) | manual across templates | reordered nav→shared header/footer.
- 3.2.4 Consistent Identification (AA) | `sample-compare` | one function, many names, or unnamed on every page→one name.
- 3.2.6 Consistent Help (A) | manual across pages | help moves/vanishes→same relative order.
- 3.3.1 Error Identification (A) | manual + SR | colour-only errors→text, aria-describedby, announced.
- 3.3.2 Labels or Instructions (A) | `form-field-multiple-labels` (partial) + manual | placeholder-only→visible label, hints up front.
- 3.3.3 Error Suggestion (AA) | manual | "Invalid value"→suggest fix (unless security).
- 3.3.4 Error Prevention (Legal, Financial, Data) (AA) | manual | no review→reversible, checked or confirmed.
- 3.3.7 Redundant Entry (A) | manual multi-step | retyping→prefill/select (unless essential, security, stale).
- 3.3.8 Accessible Authentication (Minimum) (AA) | manual paste into password/OTP | blocked paste, puzzles, CAPTCHA-only→allow paste/managers, WebAuthn, magic links (object recognition OK at AA).

## Robust
- 4.1.2 Name, Role, Value (A) | axe name/label/ARIA rules + SR/keyboard | role-less/unnamed controls→native or APG.
- 4.1.3 Status Messages (AA) | manual + SR | silent toasts/results/form errors→`role="status"`/`alert` without moving focus.

## ACT and coverage
[ACT rules](https://www.w3.org/WAI/standards-guidelines/act/rules/) are informative, partial; many SCs need manual tests. For rule IDs web-fetch ACT + [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/).

## Non-web ICT
[WCAG2ICT](https://www.w3.org/TR/wcag2ict/) (informative): A/AA for documents and software, not hardware/closed systems. [WCAG2Mobile](https://www.w3.org/TR/wcag2mobile-22/) for apps.
- Docs/PDFs: tags, alt, reading order, field names, lang, headings; set-of-pages SCs (2.4.1, 2.4.5, 3.2.3, 3.2.4) differ for a single document.
- Native apps: bot tests web views/site only. Owner runs Accessibility Inspector/XCUITest `performAccessibilityAudit`, Accessibility Scanner/Espresso `AccessibilityChecks`, then VoiceOver+TalkBack per screen: labels, traits, order, grouping, actions, modal focus, announcements; largest text (iOS AX, Android 200%), rotation, Reduce Motion. 2.5.8 = 24 pt/dp; HIG 44 pt, Android 48 dp.

## APG ([patterns](https://www.w3.org/WAI/ARIA/apg/patterns/))
Native `<button>`, `<a>`, `<dialog>`, `<select>` first; a role without its keyboard/state behaviour fails 4.1.2 (often 2.1.1).
- Menu: app-like only (site nav = disclosure); arrows, Esc, Tab leaves. Dialog: named; focus in, trapped, Esc, restored, inert background.
- Tabs: arrows, `aria-selected`. Carousel: named Prev/Next + pause, not swipe-only. Combobox: `aria-expanded`/`-controls`/`-activedescendant`; prefer native.
