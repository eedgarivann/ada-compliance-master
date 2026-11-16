---
name: ada-accessibility-audit
description: "Use this when auditing a live or staging website or web app for accessibility (WCAG 2.2 AA, ADA): WCAG-EM scope and sampling, journey mapping, read-only scripted tests, evidence standard, severity ladder, platform fixes and vendor risk."
---

# ADA accessibility audit

Rules: **ada-compliance-master-core**. SC tests: **wcag22-criteria-test-map**. Law: **ada-accessibility-law**. Formats: **ada-accessibility-deliverables**. ACR, CI, docs, media, user tests: **ada-accessibility-practice**.

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
Confirm in one message (else write "assumed"). List third parties per journey (payment, booking, chat, maps, video, cookies, CAPTCHA, embeds). No site access → findings limited to what was provided.

## 2. Read-only (live sites)
Never log in, submit, buy, post or change settings (only exception: core rule 3); opening menus/dialogs/tabs is fine. All scripts use `safePage` (never remove it). Don't follow acting GET links (logout, unsubscribe, add-to-cart). Server-validated forms (common plugins or hosted checkout): `forms.mjs --try-empty-submit` detects it; then error handling = "not tested" unless tested under core rule 3.

## 3. Checks
`scripts/` beside this skill, else `npx -y github:eedgarivann/ada-audit-scripts#v4.2.1` (or clone; `npm ci`) after `npx -y playwright@1.65.1 install chromium`; if neither, build per appendix. Default: `npx ada-audit -c cfg.json` (sample, `--journey "Name=url,…"`, `--journeys --goal`, `--platform`, `--format json,md,html,sarif,csv`) runs 1–3, 6–8 in parallel on one read-only browser → `findings.json` (deduped, scored, fix steps) + report; then add states (`--click "<sel>;…"`), focus-state, menu-modal and confirm every candidate.
1. `inventory --site <origin>`: every published page is in scope; flag demo/placeholder pages, leftovers, overlays.
2. `axe-scan` at 390 + 1440 px and key states (menu, dialog, error, cart, calendar); record version.
3. `tab-walk` per CUJ page, both widths, then `--shift`.
4. `focus-state` on flagged stops and every primary CTA.
5. `menu-modal` per menu/dialog/drawer; re-run before reporting Esc/focus-return failure. Trigger not focusable, or click opens but Enter/Space don't = 2.1.1. Duplicated headers: target visible trigger (`>> visible=true`).
6. `forms --try-empty-submit` per CUJ form. 7. `reflow`, `motion`, `context-change` (`--idle 70` on timed steps); `sample-compare` on sample, `--process` per process; `bypass-order`; `journeys --goal <CUJ>` (simulated, not user testing).
8. `sr-transcript` on every CUJ page/state (390; add `--desktop`). Confirm appendix flags in DOM + screenshot; ignore verbosity.
Manual: every CUJ keyboard-only (Enter, Space, arrows, Esc; arrow through each select: navigation on change = 3.2.2); errors: text, linked, announced (alert/live or focused summary; 4.1.3); idle past time limits (2.2.1); 3.2.6, 3.3.7, 3.3.8, 2.5.7; captions; CUJ PDFs; alt vs pixels (`*_images.html`). Real SRs can't run here: "not tested" unless a human ran them (record AT, browser, OS, versions). Give owners a 10-min SR script per CUJ (desktop: headings, landmarks, Tab a form, trigger an error; mobile: practice); offer real-SR CI. Automation finds only part (never quote a fixed %); clean scan or Lighthouse 100 can hide blockers.

## 4. Evidence
Finding = ID, journey, location (URL + selector/label), SC, how found, observation, impact, severity, fix, effort, owner, retest. **How found:** Automated, Manual inspection, Keyboard test, Accessibility tree, Simulated SR (Guidepup Virtual Screen Reader), Screen reader, Zoom/reflow, or Inferred (record tool, browser, AT, OS, version). Tree or simulated SR ≠ "tested with a screen reader".
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
Don't audit without them; first try `npx -y github:eedgarivann/ada-audit-scripts#v4.2.1`. Node 20+, ESM `.mjs`. `package.json`: `ada-audit-scripts` 4.2.1, MIT, `"type":"module"`, engines node >=20; pin `playwright` 1.65.1, `axe-core` 4.14.0, `@axe-core/playwright` 4.14.0, `@guidepup/virtual-screen-reader` 0.33.0; lockfile; `npx playwright install chromium`; record versions. Flags: `--out` (./audit-output), `--channel chrome`, `--click` (refuse submit controls), `--urls` file (`#` line comments; keep URL fragments) or comma list. Outputs are candidates.
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
