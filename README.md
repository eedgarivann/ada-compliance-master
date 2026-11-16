# ADA Compliance Master

[![Validate](https://github.com/eedgarivann/ada-compliance-master/actions/workflows/validate.yml/badge.svg)](https://github.com/eedgarivann/ada-compliance-master/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A plugin of seven [Agent Skills](https://agentskills.io/specification) for digital accessibility work. It helps you audit websites and web apps against **WCAG 2.2 AA**, write a prioritized plain-language fix plan for any common platform, and explain ADA and related accessibility law with dated, cited sources.

It is meant for site owners, designers, developers, agencies and public bodies. It is not a law firm, and it is not a certification body.

> **Not legal advice. Never a compliance certification.** A clean scan, a high Lighthouse score, or “no failures found in this sample” does not mean a site “conforms” or is “ADA compliant,” and it does not prevent complaints or lawsuits. Law answers are general information with sources and dates; a demand letter, complaint or agency notice is a reason to contact qualified counsel now.

The scripted, read-only audit checks live in a companion repo: **[ada-audit-scripts](https://github.com/eedgarivann/ada-audit-scripts)** (current pin: `v4.2.1`).

## Install

Once the plugin is listed, install **ADA Compliance Master** from the plugin marketplace in [Grok Bot](https://x.ai/bot), Grok, or [Cursor](https://cursor.com).

In Cursor you can also add this GitHub repository from **Customize → Plugins**. There are no API keys and no login to configure. Live audits are read-only: the skills never log in, submit, buy or change a production site.

## Skills

| Skill | When to use it |
|---|---|
| [ada-compliance-master-core](skills/ada-compliance-master-core/SKILL.md) | Every accessibility conversation: identity, stance, modes, tone and honest limits. |
| [ada-accessibility-getting-started](skills/ada-accessibility-getting-started/SKILL.md) | The first time someone asks for help: learn the site, journeys, platform, jurisdictions and any legal matter. |
| [ada-accessibility-audit](skills/ada-accessibility-audit/SKILL.md) | A live or staging site or web app: WCAG-EM scope, journeys, read-only scripted tests, evidence and a priority plan. |
| [ada-accessibility-deliverables](skills/ada-accessibility-deliverables/SKILL.md) | Reports, accessibility statements, remediation logs, monitoring plans and design handoff cards. |
| [ada-accessibility-practice](skills/ada-accessibility-practice/SKILL.md) | Design annotation, ACR/VPAT, CI, real screen-reader tests, content/PDF/media, disabled-user testing, platform playbooks. |
| [ada-accessibility-law](skills/ada-accessibility-law/SKILL.md) | ADA, Section 504/508, Fair Housing, state laws, EAA, AODA, Accessible Canada Act, demand letters — cited and dated, not legal advice. |
| [wcag22-criteria-test-map](skills/wcag22-criteria-test-map/SKILL.md) | Every WCAG 2.2 A/AA success criterion: what it means, how to test it, and a typical fix. |

## Example prompts

- Audit `https://www.w3.org/WAI/demos/bad/before/home.html` against WCAG 2.2 AA.
- We received an ADA demand letter about our website. What should we do?
- Design an accessible focus ring and color palette for a Shopify store.
- Write an accessibility statement for a small nonprofit.

See [TESTING.md](TESTING.md) for what a good answer to each of those looks like.

## Limits

- Live sites are read-only. Logins, payments and server-side form validation are untested unless you provide a staging copy or an approved test account through a secure channel.
- Automated checks and simulated screen-reader output find only part of the barriers on a site. Confidence needs real keyboard and screen-reader testing, ideally with disabled users.
- Platform lock-in (hosted checkout, locked templates, third-party widgets) is recorded as a dependency, not ignored.
- Law changes and courts disagree. Volatile facts in the law skill should be re-verified before they are stated.

## Run the audit scripts

```sh
npx -y playwright@1.65.1 install chromium       # once
npx -y github:eedgarivann/ada-audit-scripts#v4.2.1 \
  https://example.org/ https://example.org/contact \
  --journey "Contact=https://example.org/contact" \
  --format json,md,html
```

Pin the tag so results are reproducible. Full usage: [ada-audit-scripts](https://github.com/eedgarivann/ada-audit-scripts).

## License

[MIT](LICENSE) © 2026 eedgarivann.
