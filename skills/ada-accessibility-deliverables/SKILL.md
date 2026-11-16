---
name: ada-accessibility-deliverables
description: "Use this when writing an accessibility audit report, statement, remediation log, monitoring plan or design handoff: the A–N deliverable formats, evidence rules, and the accessibility statement template."
---

# ADA accessibility deliverables

Full report = A–J; K–N appendices. Evidence/priority: **ada-accessibility-audit**; SCs: **wcag22-criteria-test-map**; law: **ada-accessibility-law**. ACR/VPAT: use **ada-accessibility-practice**, not this format. Chat: core "Tone and length"; full report in a file or page.

**A. Executive summary** (≤200 words): scope, methods, date; 3–5 biggest problems in plain language + the journey each breaks; proportionate risk; 30/60/90-day plan with effort.
**B. Scope and methods (WCAG-EM 1–3):** target, baseline, sample (structured + random, complete processes) + audit §4 scope fields. Only methods actually run. If no screen reader used, say so.
**C. What works:** specific credits; first-party runtime fixes (move into source).
**D. Priority checklist:** Fix now / Fix next / Monitor: `[ ] item · journey · SC · effort · owner`.
**E. Findings:** table `| ID | Issue | Journey | SC (level) | Severity | Effort | Plan |`, then one card per ID (F-001…) using audit §4 fields (draft from the CLI report; keep only confirmed items). Mark best practice/AAA as not failures. Simulated SR is never a real screen-reader test. Order: confirmed, inconclusive (both runs), best practice/AAA. Tag inferred causes `Inferred`.
**F. Third-party table:** vendor · journey · issue · what to ask (ACR, roadmap, contact) · workaround.
**G. Not tested:** each gap + reason (login/payment, server-side validation, no screen reader, native app, PDFs unopened) + what closes it (staging, test account, approved submission, professional AT testing). JAWS, NVDA, VoiceOver, TalkBack stay here unless a human ran them.
**H. Environment limits:** artifacts ruled out and how (blocked CDN images, direct fetch valid → not reported); flaky results.
**I. Other risks (not accessibility):** demo content, wrong contacts, dead links, placeholders, broken integrations; one line each + location.
**J. Legal context:** general, cited, dated, from law skill, with "This is general information, not legal advice."

**K. Accessibility statement template:**
> **Accessibility statement for [Organization]**
> [Organization] wants [site/app] to be usable by everyone, including people with disabilities. We aim to meet WCAG 2.2 AA [or 2.1 AA].
> **Status:** We are working toward this standard. Last reviewed [date] using [methods actually run, verbatim from B].
> **Known limitations:** each barrier + a working, staffed alternative, including third-party components and what's being done.
> **Feedback and help:** contact [email]/[phone]/[form]. Aim to respond within [X business days] and provide the information or service another way.
> **Ongoing work:** [review cadence].
Rules: "Last reviewed using" matches what ran, nothing added; every alternative staffed and working; no "fully compliant", no overlay advertising; counsel reviews if there's a legal matter.

**L. Remediation log:** `| Date found | ID | Page/component | Issue | WCAG SC | Severity | Owner | Status (Open/In progress/Fixed/Verified/Vendor) | Fix date | Verified by, method, date | Notes |`

**M. Monitoring:** release: scan changed templates + keyboard. Monthly: CUJ re-scan, new media/PDFs. Quarterly: keyboard + SR per CUJ (desktop, mobile), vendors. Yearly/redesign: fresh audit, statement, ACRs. Reported barriers first.

**N. Design handoff:** one spec card per component (practice annotation + review): name, role, states, keyboard, focus, contrast tokens, target size, motion, acceptance tests.
