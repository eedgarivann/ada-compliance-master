---
name: ada-accessibility-practice
description: "Use this when designing accessible components, writing an ACR or VPAT, setting up accessibility CI, testing with real screen readers, annotating designs, creating content, PDFs or media, involving disabled testers, or applying WordPress, Shopify, Webflow, Framer, Squarespace, Wix or React platform fixes."
---

# ADA accessibility practice

See also **ada-accessibility-audit**, **ada-accessibility-deliverables**, **wcag22-criteria-test-map**, **ada-accessibility-law**.

## 1. ACR (VPAT)
ACR = filled **ITI VPAT 2.5Rev (24 Apr 2025)** ([ITI](https://www.itic.org/policy/accessibility/vpat); not ITI-certified). Editions: 508 (WCAG 2.0), EU (EN 301 549, WCAG 2.1), WCAG (2.0/2.1/2.2, optional AAA), INT (all, 2.2). EN 301 549 V4.1.1 (Sep 2026) moves to WCAG 2.2; EAA presumption only once cited in EU Official Journal. Required: product/version, date, description, contact, methods (tools+versions, AT/browsers, manual, tester), standards, notes. Levels only: Supports (incl. equivalent facilitation), Partially Supports, Does Not Support, Not Applicable; "Not Evaluated" AAA only. Non-Supports remarks name feature, impact, workaround. Never Supports from automation alone; never N/A for existing failing content; base on dated WCAG-EM evaluation. Not a certification; counsel reviews contract reliance.
**Vendor ACRs:** check edition, date, version, WCAG level, methods, tester. Red flags: all Supports, no methods, old version, overlay as remedy. Ask for roadmap, contact/SLA, contract terms (warranty, remediation, indemnity; counsel). Keep a staffed alternative; log dependency.

## 2. Regression prevention (doesn't prove accessibility)
- Lint: jsx-a11y, vuejs-accessibility, or `@angular-eslint/template`; errors fail build. Components: `jest-axe`/`vitest-axe`, Storybook a11y.
- E2E: Playwright + `@axe-core/playwright` on each CUJ page and state; pin axe + WCAG 2.0–2.2 A/AA tags from test map; fail on new violations; add keyboard asserts (order, dialog focus, Esc, visible focus).
- Site: `pa11y-ci` or `@axe-core/cli`; Lighthouse CI as trend, never sole gate. Baseline legacy issues; log tracks them.
- Pre-release: scans, keyboard run of changed CUJs, focus, 200%/320 px, contrast, names/states, errors announced, media alternatives, SR spot check, statement accurate.

### Real screen-reader CI (Guidepup)
Repo + CI: [`@guidepup/playwright`](https://github.com/guidepup/guidepup-playwright) (`nvdaTest`/`voiceOverTest`, `withGuidepup()`, serial, headed) + [`@guidepup/guidepup`](https://github.com/guidepup/guidepup); [`@guidepup/setup`](https://github.com/guidepup/setup) (`--ci`, then `install`; setup-action unsupported). Workflow YAML (windows/NVDA/chromium, macos/VoiceOver/webkit): guidepup-playwright repo. Assert a real heading via `lastSpokenPhrase()`, one spec per reader; staging only; retries for flakes; upload `test-results/`.
**Local Mac VoiceOver:** VoiceOver Utility: allow control by AppleScript; accept Terminal's Automation prompts; Terminal needs Full Disk Access (app helpers get EPERM); headed WebKit via `@guidepup/playwright`; hands off while it speaks.
**JAWS**: no free automation; manual or paid real-AT clouds ([Assistiv Labs](https://assistivlabs.com/), [BrowserStack](https://www.browserstack.com/accessibility-testing); check plans).

### Mobile SR script (10 min)
CUJ start to step before submit/pay; never submit/pay or call a site compliant. Results = `Screen reader` (AT, OS, versions), never `Simulated SR`.
Swipe right/left, double-tap. Check names/states, labels/required/errors, alt/decorative, dialog focus in/back, zoom, large text, 320 px reflow, orientation.
**VoiceOver:** Settings > Accessibility > VoiceOver, or Accessibility Shortcut (triple-click Side/Home). Rotor: 2-finger twist, swipe up/down (Headings, Links). Zoom: 3-finger double-tap; Larger Text. Off: shortcut/Siri.
**TalkBack 14-15:** Settings > Accessibility > TalkBack; or hold both volume keys. Menu: 3-finger tap or down-then-right. Controls: 3-finger swipe up/down, swipe down/up (Headings, Links, Controls). Magnify: 2-finger drag/pinch. Off: volume keys/Assistant.
SCs 1.1.1 1.3.1 1.3.4 1.4.4 1.4.10 2.4.3 2.4.6 2.5.8 3.3.1 3.3.2 4.1.2. Sheet: step|expected|P/F|notes.
2026-11-15: support.apple.com VoiceOver; support.google.com TalkBack.

## 3. Design annotation
Annotate: headings (one H1), landmarks (named navs, main, search), numbered focus order + dialog focus + skip target, accessible names (icons, alt or decorative), roles/states/keyboard (native or APG), error/status copy + announcement, reading order if visual ≠ DOM, tokens (4.5:1 text, 3:1 non-text, focus ring, 24×24 targets, reduced motion).
**Review:** contrast in every state, no colour-only info, focus on all controls, targets, 200%/320 px, no hover/drag-only, visible labels, consistent help, no sign-in puzzles, pausable motion. Spec card per component (deliverables N).

## 4. Content, documents, media
**COGA** ([W3C Note 29 Apr 2021](https://www.w3.org/TR/coga-usable/)): purpose, findability, clear content, prevent/correct mistakes, focus, no memory reliance, help, personalization. One idea per sentence, common words, numbered steps, no time pressure, human help; beyond A/AA = recommendations.
**PDFs:** prefer HTML on CUJs. Author accessibly → tagged PDF (OCR scans). **PDF/UA** (ISO 14289-1; 14289-2:2024 for PDF 2.0); PAC + Acrobat Pro, then manual: order, headings, table headers, alt, fields, bookmarks, title. Old PDFs under Title II: law skill (28 CFR 35.201(b)).
**Media** ([W3C](https://www.w3.org/WAI/media/av/)): describe visuals in script; edited captions (WebVTT/SRT, not burned-in); AD for 1.2.5 (transcript meets 1.2.3, not 1.2.5); transcripts for audio-only; keyboard player with caption/AD toggles, no autoplay sound, pause >5 s; live = CART + accessible recording.

## 5. Disabled-user testing
Per [W3C](https://www.w3.org/WAI/test-evaluate/involving-users/): mixed disabilities (SR, magnifier, keyboard/switch, voice, deaf/HoH, cognitive); 3–5 per CUJ find major barriers; pay them; own setups, real tasks. Record success, blockers, quotes; map to WCAG + non-WCAG issues. One participant ≠ conformance; WCAG pass ≠ usable.

## 6. Platforms (check current docs)
- WordPress: child theme, patterns, plugin settings/replacement; never edit parent theme. Culprits: core Navigation block (overlay, nested Page List; report upstream), page builders, sliders, forms, calendars, Woo add-ons, demo content.
- Shopify: theme Liquid (cards, variants, quick-add, cart drawer, menus, media sliders focusing off-screen slides, duplicate IDs in repeated selectors) is yours; hosted checkout → report to Shopify, use checkout extensibility; test apps, escalate to vendor.
- Webflow: tags, aria, alt, focus editable; interactions need reduced motion; check menu button by keyboard, `<html lang>`, a `main` tag, names on image link blocks, deleted form labels. Framer: headings, link-wrapped cards, appear animations, CMS alt, menu focus; code overrides.
- Squarespace: note `templateVersion`; 7.0 burgers can be click-only divs (2.1.1: move to 7.1 or code injection); image blocks have no alt text until the owner adds it on the block's Content tab; the focus outline is built in, so restore it if custom CSS removed it; check Site Styles contrast.
- Wix: test mobile with a phone UA (separate site); fixed-width desktop layouts scroll sideways at 400% zoom (1.4.10). Defaults: mobile menu ignores Esc, no aria-expanded; Quick Action Bar can stop Tab. Owner: Accessibility Wizard (skips CMS, apps, checkout), alt, heading tags, contrast; else report to Wix.
- React/Next/Vue: native first, focus on route change/modals, live regions, axe CI, jsx-a11y; no `aria-label` on card links (hides price/sold-out; 2.5.3); dots/icons ≥24 px.
Blocked fix → staffed phone/email workaround + dependency.
