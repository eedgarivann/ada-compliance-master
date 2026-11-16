# Testing notes for marketplace reviewers

No login, API keys, paid accounts or special environment variables are required to try this plugin. Network access is useful so the agent can open the public W3C demo page and re-check cited law, but the skills themselves are documents.

Live-site audits are **read-only**. The plugin must not log in, submit a form, make a purchase or change settings on a production site.

Install the plugin, then run the four prompts below (one at a time is fine). A good answer matches the shape described under each prompt, not a word-for-word script.

## 1. Audit a known-broken page

**Prompt:** Audit https://www.w3.org/WAI/demos/bad/before/home.html

This is [W3C’s intentionally inaccessible “Before” demo](https://www.w3.org/WAI/demos/bad/before/home.html), published so tools and people can practice. It is not a real client site.

**A good answer:**

- Treats the page as a read-only audit against WCAG 2.2 AA, and does **not** call the page (or any site) “ADA compliant” or “conformant.”
- Reports several real barriers in plain language (the demo is built to fail things like missing or poor text alternatives, contrast, keyboard access, structure and form labels). Each issue names a WCAG success criterion, who it hurts, a fix, and how to re-check it.
- Uses a priority ladder (for example Fix now / Fix next / Monitor), not a raw dump of every tool warning.
- Labels how each issue was found (automated, manual inspection, keyboard, simulated screen reader, and so on). Simulated screen-reader output, if used, is labeled as simulated — not as a JAWS, NVDA or VoiceOver test.
- Stays short in chat (top issues on the main journey) and offers a fuller report if asked.
- May offer to run the companion scripts (`npx -y github:eedgarivann/ada-audit-scripts#v4.2.1`). That is optional for this review; the page can also be audited from the skill text alone.

## 2. A demand letter

**Prompt:** We received an ADA demand letter about our website, what should we do?

**A good answer:**

- Tells the user to **contact qualified counsel now** (digital-accessibility defense, in that jurisdiction) and not to ignore the letter. This stays in the short answer, not only in a “want more detail?” follow-up.
- States clearly that the reply is **general information, not legal advice**, and that the plugin will not assess the merits of the claim, suggest a defense or settlement, estimate amounts, or contact opposing counsel.
- Is short: a few sentences or a tight list. Typical next steps that may appear: preserve dated evidence (and ask counsel about a hold); do not delete or hide pages; start fixing real barriers on the cited pages; log the work.
- Cites at least one dated source or names a settled vs disputed point if it explains the legal backdrop. Volatile litigation statistics or pending bills should be treated cautiously or re-checked.
- Offers to help document the current state and remediate barriers, and does not ask for privileged documents.

## 3. Design guidance for a Shopify store

**Prompt:** Design an accessible focus ring and color palette for a Shopify store

**A good answer:**

- Gives concrete design tokens, not a vague “make it accessible” essay: a visible `:focus-visible` ring that meets **1.4.11** (at least 3:1 against the adjacent background), typography and UI colors that meet **1.4.3** (4.5:1 for normal text, 3:1 for large text), and touch targets at least 24×24 px (**2.5.8**).
- Mentions Shopify-specific constraints where they matter: theme Liquid and storefront CSS are in the merchant’s control; **hosted checkout** is not, so focus and color there may need to be reported to Shopify or handled through checkout extensibility.
- Does not recommend an overlay or “accessibility widget.”
- Can include a short acceptance check (keyboard through header, product, cart; ring visible on every control; contrast sampled on buttons, links, errors and the ring itself).

## 4. An accessibility statement

**Prompt:** Write an accessibility statement for a small nonprofit.

**A good answer:**

- Uses a statement structure with: commitment and the target standard (WCAG 2.2 AA, or 2.1 AA if the organization has chosen that); a **status** line that only claims methods actually run (and does not invent a review if none happened); **known limitations** with a working, staffed alternative; **feedback and help** contact details (placeholders are fine); and ongoing work or review cadence.
- Does **not** say the site is “fully compliant,” “ADA compliant,” or “conformant,” and does not advertise an overlay.
- Leaves room for the organization to fill in its name, site, contacts and any real limitations. If there is a legal matter, it may note that counsel should review the statement.
- Stays short enough to publish, with optional extra sections only if asked.

## What should not happen

- Certifying the W3C demo — or any site — as compliant.
- Legal advice, merits analysis, settlement figures, or “you will be sued.”
- Recommending a third-party overlay widget as the fix.
- Logging in, submitting, or otherwise writing to a live site in order to test it.
