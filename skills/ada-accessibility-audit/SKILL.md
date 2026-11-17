---
name: ada-accessibility-audit
description: "Use this when auditing a live or staging website or web app for accessibility (WCAG 2.2 AA, ADA): WCAG-EM scope and sampling, journey mapping, read-only scripted tests, real NVDA/VoiceOver runs, AI judgment pass, staging-only form-error journeys, time estimate and scope choice, PDF report, evidence standard, severity ladder, platform fixes and vendor risk."
---

# ADA accessibility audit

Rules: **ada-compliance-master-core**. SC tests: **wcag22-criteria-test-map**. Law: **ada-accessibility-law**. Formats: **ada-accessibility-deliverables**. ACR, CI, docs, media, user tests: **ada-accessibility-practice**. Fixing: core **Fix mode**.

**Goal:** get as close to a skilled human tester as possible: real assistive technology where it can run, judgment on meaning, complete journeys on staging. Label every method honestly, list the rest as not tested, never claim human equivalence; disabled-user testing stays the final check.

## 0. WCAG-EM
Use [WCAG-EM](https://www.w3.org/TR/WCAG-EM/) (2.0 Group Note 23 Jul 2026; informative):
1. Scope: parts (domains, apps, third parties); target WCAG 2.2 AA unless law/contract names 2.1/2.0; AT/browser baseline.
2. Explore: common views, CUJs, page types/states, tech (HTML, ARIA, JS, PDF, video, widgets).
3. Sample: structured (each view, page type, CUJ step/state; ≥3 pages for 2.4.2, 3.2.3, 3.2.4, 3.2.6, else Not tested) + random ≈10% (record method) + all pages of complete processes.
4. Audit; if random pages show new types/failures, add pages and repeat.
5. Report steps, sample, methods. Any claim names date, scope, target, sample.
**§5.2 conformance:** level met in full; full pages; complete processes (one failing step fails it); accessibility-supported uses only; non-interference (1.4.2, 2.1.2, 2.3.1, 2.2.2 apply to all content). Unless all met: "no failures found in [scope]", never "conforms".

## 1. Journeys
Note business type, audience, jurisdictions, physical locations. Pick 3–6 CUJs:
- E-commerce: search → product (variants, quick-add, drawer) → checkout → payment → confirmation → returns. Hospitality: menu (PDF/image menus often fail), hours, order, reserve.
- Services/health: booking, intake, portal, bill pay, telehealth. SaaS: signup → auth (MFA/CAPTCHA) → onboarding → core task → billing.
- Nonprofit/public: donate, membership, events, volunteer, applications, housing inquiry, PDFs, meeting video. Portfolio: nav, work, contact.
Confirm in the scope question (else write "assumed"). List third parties per journey (payment, booking, chat, maps, video, cookies, CAPTCHA, embeds). No site access → findings limited to what was provided.

## 1a. Estimate and scope (before any run)
Probe first (≤1 min, read-only): page count from the sitemap or `inventory --site`, platform, home-page weight and request count. Then one multiple-choice question (the host's question tool, such as Cursor's AskQuestion, when available), each option with a time range:
- **One page:** ~5–10 min.
- **Pages you name:** ~5 min + 2–3 min per page.
- **Key journey or representative sample** (WCAG-EM): 3–6 pages ~15–30 min; 10–25 pages ~30–60+ min.
- Real screen-reader runs or staging form journeys: +15–30 min.
Say these are estimates from measured runs (the scripts take ~35 s for one live page, ~3 min for 4 pages and ~7 min for a 6-page WordPress site, plus confirming, the judgment pass and the PDF) and that every site differs: heavy pages, many forms, bot checks and slow hosts take longer. If the run goes past the range, tell the user once, with a new estimate.

## 2. Read-only (live sites)
Never log in, submit, buy, post or change settings (only exception: core rule 3); opening menus/dialogs/tabs is fine. All scripts use `safePage` (never remove it). Don't follow acting GET links (logout, unsubscribe, add-to-cart). Server-validated forms (common plugins or hosted checkout): `forms.mjs --try-empty-submit` detects it; then error handling = "not tested" unless the staging form-error journeys (§3c) ran.

## 3. Checks
`scripts/` beside this skill, else `npx -y github:eedgarivann/ada-audit-scripts#v4.4.1` (or clone; `npm ci`) after `npx -y playwright@1.65.1 install chromium`; if neither, build per appendix. Default: `npx ada-audit -c cfg.json` (sample, `--journey "Name=url,…"`, `--journeys --goal`, `--platform`, `--format`, default `json,md,html,pdf`) runs 1–3, 6–8 in parallel on one read-only browser → `findings.json` (deduped, scored, fix steps) + `report.pdf` and other reports; then add states (`--click "<sel>;…"`), focus-state, menu-modal and confirm every candidate.
1. `inventory --site <origin>`: every published page is in scope; flag demo/placeholder pages, leftovers, overlays.
2. `axe-scan` at 390 + 1440 px and key states (menu, dialog, error, cart, calendar); record version.
3. `tab-walk` per CUJ page, both widths, then `--shift`.
4. `focus-state` on flagged stops and every primary CTA.
5. `menu-modal` per menu/dialog/drawer; re-run before reporting Esc/focus-return failure. Trigger not focusable, or click opens but Enter/Space don't = 2.1.1. Duplicated headers: target visible trigger (`>> visible=true`).
6. `forms --try-empty-submit` per CUJ form. 7. `reflow`, `motion`, `context-change` (`--idle 70` on timed steps); `sample-compare` on sample, `--process` per process; `bypass-order`; `journeys --goal <CUJ>` (simulated, not user testing).
8. `sr-transcript` on every CUJ page/state (390; add `--desktop`). Confirm appendix flags in DOM + screenshot; ignore verbosity.
Manual: every CUJ keyboard-only (Enter, Space, arrows, Esc; arrow through each select: navigation on change = 3.2.2); errors: text, linked, announced (alert/live or focused summary; 4.1.3); idle past time limits (2.2.1); 3.2.6, 3.3.7, 3.3.8, 2.5.7; captions; CUJ PDFs; alt vs pixels (`*_images.html`). JAWS, Narrator, TalkBack, iOS VoiceOver and anything §3a didn't cover: "not tested" unless a human ran them (record AT, browser, OS, versions). Give owners a 10-min SR script per CUJ (desktop: headings, landmarks, Tab a form, trigger an error on staging; mobile: practice). Automation finds only part (never quote a fixed %); clean scan or Lighthouse 100 can hide blockers.

### 3a. Real screen readers
`ada-audit sr` (v4.3.0+) drives real NVDA (Windows) or VoiceOver (macOS) via Guidepup through headings, landmarks, form fields, buttons, links, graphics and Tab, records every spoken phrase and turns problems into findings with method `real-screen-reader` (`sr-transcript` stays `simulated-screen-reader`; never merge the labels).
- **Run:** on a Windows/Mac, `npx @guidepup/setup setup` + `install` once, then `npx ada-audit sr --url <url> [--journey f.json] -o out` (hands off while it speaks; Linux exits 2). Anywhere else: the repo's **Real screen readers** GitHub workflow (`screen-readers.yml`: NVDA + Chromium on Windows, VoiceOver + WebKit on macOS; artifacts `real-sr-*`), run from a fork or the owner's CI. Copy `real-sr/` into the suite's folder, `npx ada-audit report out`: a barrier both found = one *corroborated* finding.
- Run on every CUJ page when possible; a failed pass (`errors`, "Ran fully: no") is missing evidence, never a clean result.
- **Limits (state them):** scripted, no human listening or judging; read-only, so error announcements are never heard (`ERRORS-NOT-TESTED`; 3.3.1/4.1.3 stay not tested unless §3c ran); English speech parsing only; NVDA + Chromium and VoiceOver + WebKit only; JAWS, Narrator, TalkBack, iOS VoiceOver, braille and live-region timing not tested; long pages sampled at step caps.

### 3b. AI judgment pass
Tools check presence; you check meaning. For every CUJ image alt, form label, link text, page title, heading and error/status message, compare the settled screenshot (pixels, nearby text, purpose) with the DOM and accessible name: would someone who can't see the screen know what it is, what it does or where it goes, and what to do next?
- Fails include: alt that misdescribes, repeats nearby text or names a file; meaningful images marked decorative (or decorative ones narrated); accessible name missing the visible label (2.5.3); vague or duplicate link text to different targets (2.4.4); titles/headings that don't say what the page or section is (2.4.2, 2.4.6); errors that don't name the field or the fix (3.3.1, 3.3.3).
- Record `How found: Judgment (AI; screenshot + DOM)`, confidence **High/Medium/Low** and a one-line reason. High → finding; Medium → finding marked "confirm"; Low → **Human review** list, not a failure. Never upgrade judgment to confirmed without a second method or a human.

### 3c. Form-error journeys (staging only)
Never on a live site. Only on a staging copy or test environment, with the owner's explicit permission (core rule 3; labelled test data, never a real payment): submit each CUJ form empty, with invalid formats and with one field wrong. Check each error is shown in text and identifies the field (3.3.1), suggests the fix (3.3.3), is announced or focus moves to a summary (4.1.3; real SR if available), entered data is kept (3.3.7), and correction succeeds. Record "tested on staging" + date; without staging, "not tested".

## 4. Evidence
Finding = ID, journey, location (URL + selector/label), SC, how found, observation, impact, severity, fix, effort, owner, retest. **How found:** Automated, Manual inspection, Keyboard test, Accessibility tree, Simulated SR (Guidepup Virtual Screen Reader; `simulated-screen-reader`), Real SR (`real-screen-reader`: NVDA/VoiceOver + browser + OS + versions, scripted), Screen reader (human-run), Judgment (AI, confidence), Zoom/reflow, or Inferred (record tool, browser, AT, OS, version). Tree or simulated SR ≠ "tested with a screen reader"; scripted real SR ≠ user testing.
- Measure settled states (≥1 s) + screenshot. Script contrast ignores alpha/gradients/images: confirm on pixels.
- Rule out environment artifacts a second way (re-fetch asset, fresh viewport shot — full-page shots misplace fixed headers — other browser); they go under environment limits.
- Retests disagree → inconclusive, show both. Discard bot-check/challenge pages; rerun one site at a time.
- First-party patch scripts: test on, check no-JS, credit, recommend moving into source. Vendor overlays: check AT interference.
- Separate confirmed, `Inferred`, best practice, AAA. Missing H1/skipped level = best practice unless misleading (1.3.1).
- Scope: pages, widths, browsers, tools+versions, date, assumed CUJs, not tested.

## 5. Severity, ladder, plan
**Severity:** Blocker (can't complete CUJ), Critical (major difficulty or wrong-outcome risk), Serious (real friction/lost info on CUJ), Moderate (off path or workaround), Minor (polish/best practice).
**Ladder** (rung, then severity): 1 transactional/identity (forms, checkout, payment, donate, contact, book, login, account); 2 keyboard/focus 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11 (only if *entirely* hidden by author content; partial = 2.4.12 AAA); 3 contrast/alt 1.4.3, 1.4.11, 1.1.1 (text on images, icon-only controls); 4 structure/naming 1.3.1, 2.4.2, 2.4.4, 2.4.6, 3.1.1, 4.1.2; 5 rest (media, motion, reflow polish, cognitive, non-CUJ PDFs).
**Plan:** Fix now = Blocker/Critical in rungs 1–3 on any CUJ. Fix next = other Serious on CUJs, rung 4 sitewide templates, **any A/AA CUJ failure with Low effort regardless of severity**. Monitor = other Moderate/Minor, non-CUJ, vendor roadmap, regressions. Shared templates before single pages. **Effort:** Low <1 h (content/setting), Medium hours–1 day (template/CSS/JS), High days (rebuild/vendor).

## 6. Fixes, vendors, hand-off
Each fix names where on platform (theme file, CMS field, plugin/vendor setting, component prop); use practice playbooks + current docs. If platform blocks a fix: staffed phone/email workaround and a logged dependency. For CUJ third parties, request ACRs, judge per practice, log gaps. Write up per deliverables; legal context from law skill (re-verify volatile facts).

## Appendix: build scripts if `scripts/` is missing
Don't audit without them; first try `npx -y github:eedgarivann/ada-audit-scripts#v4.4.1`. Node 20+, ESM `.mjs`. `package.json`: `ada-audit-scripts` 4.4.1, MIT, `"type":"module"`, engines node >=20; pin `playwright` 1.65.1, `axe-core` 4.14.0, `@axe-core/playwright` 4.14.0, `@guidepup/virtual-screen-reader` 0.33.0, `@guidepup/guidepup` 0.40.0 (real SR, §3a; not rebuilt here); lockfile; `npx playwright install chromium`; record versions. Flags: `--out` (./audit-output), `--channel chrome`, `--click` (refuse submit controls), `--urls` file (`#` line comments; keep URL fragments) or comma list. Outputs are candidates.
- **lib.mjs:** viewports 390×844, 1440×900; `open` (networkidle, 90 s, settle 1.5 s), `scrollThrough`, WCAG `contrast` (ignores alpha), `DESCRIBE_FOCUS`. **safePage:** context `serviceWorkers:'block'`; route `**/*` on context (incl. popups); abort every method except GET/HEAD/OPTIONS (incl. form submits); log `"METHOD url"` to `page.blockedWrites`; never continue them. `--click` prep skips missing selectors and refuses `type=submit`/typeless form buttons and Enter in fields (GET forms pass method rule). DESCRIBE_FOCUS: role, name, ring (outline/box-shadow/NONE), fg/bg, inView, 5-point coverage (centre + inset corners; ignore focus's ancestors/descendants, transparent empty overlays, same-href twins): 5/5 = 2.4.11 candidate, else 2.4.12 AAA.
- **axe-scan:** `--widths 390,1440`; tags `wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa,best-practice`; JSON per URL/width, viewport shot, `summary.tsv`, axe version.
- **tab-walk:** `--width`, `--max 60`, `--settle 1000`, `--shift`; flags `NO-RING?`, `COVERED(entire?)`, `PARTLY-COVERED(n/5)`, `OFFSCREEN`, `TEXT n:1` (<4.5), `REPEAT(trap?)` (3+; halt at 10), `FOCUS-LOST` (focus to body before last tabbable; blur script, F55); crops. `NO-RING?` misses rings on an ancestor/`::after`; `COVERED` counts translucent headers: check crop.
- **focus-state:** `--stops`/`--selector`; settled hover/focus colours, contrast, shots.
- **menu-modal:** `--trigger`, `--container`; trigger focusable, opens by Enter/Space vs click (2.1.1)? no re-toggle before Esc; open by Enter, focus inside?, Tab 25× counting escapes (modals must contain focus), Esc, focus return, `aria-expanded`, shots.
- **forms:** per field label, placeholder-only, required (colour-only?), autocomplete vs purpose (1.3.5), paste blocked (3.3.8), CAPTCHA w/o alternative, display:none; flags `NO-LABEL`, `PLACEHOLDER-ONLY`, `HIDDEN-CONTROL`; controls outside `<form>` too; `ariaSnapshot()`; `--try-empty-submit` (abort navigations): blocked write = server-side, NOT TESTED; else diff: `ERROR-COLOUR-ONLY`, `ERROR-NOT-ANNOUNCED?`, `FOCUS-NOT-MOVED`.
- **reflow:** 320/640 px overflow (ignore hidden/carousels); 1.4.12 spacing at 1280, list clipped (skip visually-hidden).
- **motion:** reducedMotion no-preference vs reduce; moving elements (>3 px), video autoplay/controls, infinite animations, pause controls.
- **inventory:** title, lang, headings, landmarks, skip link, images (`ALT-*`, CSS backgrounds, `*_images.html`), `FAKE-HEADING?`, colour-only links (G183 hover + focus cue), overlays `accessibe|acsbapp|userway|audioeye|equalweb|maxaccess|accessibly|enable\.co\.il|purpose-?ai|allyable|reciteme`, demo regex `demo|sample|lorem|hello-world|placeholder|starter|test-?page|template|example|dummy`, dead `#` links, third-party hosts; re-fetch broken images outside browser (image response = `ENVIRONMENT ARTIFACT (not a finding)`); `--site`: sitemaps (cap 2,000) + WP REST; flag published URLs missing from sitemap (skip if capped).
- **sr-transcript:** `--desktop`, `--max 1500` (warn if hit), `--tabs 60`. Inject package's browser ESM via `page.evaluate` (rewrite `export{…}` to `window.__vsr`; no network). Linear read (skip `<noscript>`), heading/landmark lists, Tab pass. Every output starts: `Simulated screen reader output (Guidepup Virtual Screen Reader). Not JAWS, NVDA or VoiceOver; confirm with a real screen reader.` Flags: `NO-NAME`, `IMG-FILENAME(?)` (DOM: img without alt; virtual SR says only "image"), `VAGUE-LINK`, `DUPLICATE`, `REDUNDANT-LINK`, `GENERIC-CLICKABLE`, `FOCUSABLE-GENERIC`, `FOCUS-LOST` (not after last tabbable), `REPEAT(trap?)`, `POSITIVE-TABINDEX`, `LONG-NAME` (control/image name >150), `LAYOUT-TABLE?`, `HEADING-SKIP`, `NO-H1`, `NO-MAIN`, `NO-HEADINGS`.
- **context-change:** abort + log navigations; `FOCUS-REMOVED`, `CHANGE-ON-INPUT` (ArrowDown selects, typing), `MOUSE-ONLY` (click handler, not focusable), `TIMEOUT-NAV` (`--idle`). **sample-compare** (≥3 URLs): `DUP-TITLE`, `NAV-ORDER-DIFFERS`, `UNNAMED-REPEATED`, `INCONSISTENT-NAME`, `REPEATED-FIELD?` (`--process`).
- **bypass-order:** `READING-ORDER?`, `LAYOUT-TABLE-LINEAR?`, `FOCUS-ORDER-JUMP?`, skip-link Enter test, `BYPASS-NONE`. **journeys:** personas seek `--goal`; stop before submit/pay/login; output starts `SIMULATED persona journeys`.
