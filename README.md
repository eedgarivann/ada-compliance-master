# ADA Compliance Master

[![Validate](https://github.com/eedgarivann/ada-compliance-master/actions/workflows/validate.yml/badge.svg)](https://github.com/eedgarivann/ada-compliance-master/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A plugin of seven [Agent Skills](https://agentskills.io/specification) for digital accessibility work. It reads and tests websites and web apps against **WCAG 2.2 AA** (scripted checks, real NVDA and VoiceOver runs, and an AI judgment pass on meaning), writes a prioritized plain-language fix plan for any common platform, and, with the owner's permission, fixes barriers in source or hands exact fix packets to the owner's own bots. It also explains ADA and related accessibility law with dated, cited sources.

The goal is to get as close to a human accessibility tester as possible, while labelling every method honestly and leaving the final word to people who use assistive technology.

It is meant for site owners, designers, developers, agencies and public bodies. It is not a law firm, and it is not a certification body.

> **Not legal advice. Never a compliance certification.** A clean scan, a high Lighthouse score, or “no failures found in this sample” does not mean a site “conforms” or is “ADA compliant,” and it does not prevent complaints or lawsuits. Law answers are general information with sources and dates; a demand letter, complaint or agency notice is a reason to contact qualified counsel now.

The scripted, read-only audit checks live in a companion repo: **[ada-audit-scripts](https://github.com/eedgarivann/ada-audit-scripts)** (current pin: [`v4.4.1`](https://github.com/eedgarivann/ada-audit-scripts/releases/tag/v4.4.1), which adds the PDF report on top of real NVDA and VoiceOver runs).

## What a user sees

1. A 2–3 sentence intro and one question.
2. A quick read-only probe of the site, then a choice of scope, each with an estimated time: one page (~5–10 min), pages they name (~5 min + 2–3 min each), or a key journey or representative sample (3–6 pages ~15–30 min, 10–25 pages ~30–60+ min). Estimates come from measured script runs plus review time; every site differs.
3. In chat, a one-line verdict and the top 3 issues, one line each. Everything else is in the attached **PDF report**: cover with site, scope, date and methods, plain-language summary, top issues with screenshots, prioritized findings table, fix + effort + check for each issue, and limits.

## Install

Once the plugin is listed, install **ADA Compliance Master** from the plugin marketplace in [Grok Bot](https://x.ai/bot), Grok, or [Cursor](https://cursor.com).

In Cursor you can also add this GitHub repository from **Customize → Plugins**. There are no API keys and no login to configure. Audits of live sites are read-only. Changes happen only in Fix mode, with the owner's access and explicit approval, on a staging copy first.

## Skills

| Skill | When to use it |
|---|---|
| [ada-compliance-master-core](skills/ada-compliance-master-core/SKILL.md) | Every accessibility conversation: identity, stance, modes (including Fix mode), tone and honest limits. |
| [ada-accessibility-getting-started](skills/ada-accessibility-getting-started/SKILL.md) | The first time someone asks for help: a short intro and one question, a quick site probe, then a scope choice (one page, named pages or a key-journey sample) with time estimates. |
| [ada-accessibility-audit](skills/ada-accessibility-audit/SKILL.md) | A live or staging site or web app: WCAG-EM scope, journeys, read-only scripted tests, real screen-reader runs, AI judgment pass, staging-only form-error journeys, evidence and a priority plan. |
| [ada-accessibility-deliverables](skills/ada-accessibility-deliverables/SKILL.md) | PDF audit reports (default), accessibility statements, remediation logs, monitoring plans, design handoff cards, fix packets and helper-bot setups. |
| [ada-accessibility-practice](skills/ada-accessibility-practice/SKILL.md) | Design annotation, ACR/VPAT, CI, real screen-reader tests, content/PDF/media, disabled-user testing, platform playbooks. |
| [ada-accessibility-law](skills/ada-accessibility-law/SKILL.md) | ADA, Section 504/508, Fair Housing, state laws, EAA, AODA, Accessible Canada Act, demand letters — cited and dated, not legal advice. |
| [wcag22-criteria-test-map](skills/wcag22-criteria-test-map/SKILL.md) | Every WCAG 2.2 A/AA success criterion: what it means, how to test it, and a typical fix. |

## Fix mode

- **With access and approval:** fixes go into the source (theme, repo, CMS) on a staging copy first, then the same checks run again and you get a before/after. Never an overlay.
- **Hand-off:** each fix becomes a packet (exact change, where it goes, acceptance test) for your own content, design or dev bots, each in its own lane.
- **No bots yet:** it proposes only the helpers the plan needs (for example a senior web developer, design, content or document helper), each with a brief, a lead and one-editor-at-a-time rules. You approve before any are created.

## Example prompts

- Audit `https://www.w3.org/WAI/demos/bad/before/home.html` against WCAG 2.2 AA.
- We received an ADA demand letter about our website. What should we do?
- Design an accessible focus ring and color palette for a Shopify store.
- Write an accessibility statement for a small nonprofit.

See [TESTING.md](TESTING.md) for what a good answer to each of those looks like.

## Limits

- Live sites are read-only. Logins, payments and form-error handling are tested only on a staging copy or approved test account you provide through a secure channel.
- Real screen-reader runs are scripted (NVDA + Chromium, VoiceOver + WebKit, English speech only); JAWS, TalkBack and iOS VoiceOver are not covered. AI judgment items carry a confidence level, and low-confidence ones go to human review.
- Automated checks, scripted screen readers and AI judgment find only part of the barriers on a site. Confidence needs real keyboard and screen-reader testing, ideally with disabled users.
- Platform lock-in (hosted checkout, locked templates, third-party widgets) is recorded as a dependency, not ignored.
- Law changes and courts disagree. Volatile facts in the law skill should be re-verified before they are stated.

## Run the audit scripts

```sh
npx -y playwright@1.65.1 install chromium       # once
npx -y github:eedgarivann/ada-audit-scripts#v4.4.1 \
  https://example.org/ https://example.org/contact \
  --journey "Contact=https://example.org/contact" \
  --format json,md,html,pdf        # report.pdf is the client-ready report
```

Real screen readers: `npx ada-audit sr --url <url>` on Windows or macOS, or the *Real screen readers* GitHub workflow in that repo. Pin the tag so results are reproducible. Full usage: [ada-audit-scripts](https://github.com/eedgarivann/ada-audit-scripts).

## License

[MIT](LICENSE) © 2026 eedgarivann.
