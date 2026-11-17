# Changelog

## 1.2.0 — 2026-11-16

- **PDF report by default:** every audit delivers a PDF (cover with site, scope, date and methods; plain-language summary; top issues with screenshots; prioritized findings table; fix, effort and check per issue; limits), made with `ada-audit report <out> --format pdf` from [ada-audit-scripts v4.4.1](https://github.com/eedgarivann/ada-audit-scripts/releases/tag/v4.4.1) (tagged PDF, A4 or Letter). HTML, CSV, SARIF and JSON only on request.
- **Shorter replies:** first reply is 2–3 sentences plus one question; audit results in chat are a one-line verdict and the top 3 issues, one line each, then the attached PDF. Getting started now asks far fewer questions up front.
- **Time estimate:** a quick read-only probe (page count, platform, page weight) before any run, then an estimated range, based on measured script runs (one live page ~35 s, 4 pages ~3 min, a 6-page WordPress site ~7 min, plus review time). Updated once if the run goes long.
- **Scope choice:** one page, pages the user names, or a key-journey / representative sample (WCAG-EM), each with its estimate, asked as one multiple-choice question.
- Audit, practice, README and testing notes pinned to `ada-audit-scripts#v4.4.1`; both manifests at 1.2.0.

## 1.1.0 — 2026-11-16

- **Real screen readers:** the audit skill now uses `ada-audit sr` and the *Real screen readers* GitHub workflow from [ada-audit-scripts v4.3.0](https://github.com/eedgarivann/ada-audit-scripts/releases/tag/v4.3.0) (NVDA + Chromium, VoiceOver + WebKit). Findings are labelled `real-screen-reader` or `simulated-screen-reader`, with stated limits.
- **AI judgment pass:** alt text, labels, link text, titles, headings and error messages are judged for meaning from a screenshot plus the DOM, with a confidence level; low-confidence items go to human review.
- **Form-error journeys:** staging only, with owner permission, checking 3.3.1, 3.3.3 and 4.1.3. Never on live sites.
- **Fix mode:** new core section plus deliverables O (fix packet) and P (helper-bot setup): apply fixes in source on staging with approval, or hand packets to the user's own bots by lane, or propose the helper bots the plan needs, with user approval before any are created. Re-verify after each fix.
- Goal stated: get as close to a human tester as possible, without claiming equivalence.
- Audit and README pinned to `ada-audit-scripts#v4.3.0`; description and testing notes updated.

## 1.0.1 — 2026-11-15

- Replaced the plugin logo with the author-provided navy-and-white circle mark (1024×1024 opaque PNG and a matching SVG).

## 1.0.0 — 2026-11-15

Initial public plugin release.

- Seven Agent Skills: core stance and limits, getting started, WCAG 2.2 AA audit method, deliverable formats, practice (ACR/VPAT, CI, design, platforms), cited accessibility law, and the WCAG 2.2 A/AA test map.
- Agent Plugins 1.0.0 manifest at the repo root, plus a Cursor plugin manifest with the logo path.
- Audit skill pinned to `npx -y github:eedgarivann/ada-audit-scripts#v4.2.1`.
