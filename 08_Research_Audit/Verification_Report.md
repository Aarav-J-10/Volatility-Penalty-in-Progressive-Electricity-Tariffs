# Verification report (computation/economics/mathematics referee)

## Critical
* C1 — Empirical application missing (no observed data). **Unresolved.** Mitigation: manuscript explicitly synthetic; title and abstract state it. Author must decide whether to submit as a theory+simulation paper or wait for data.

## Major
* M1 — Tariff from secondary source; primary UPERC order not retrieved. **Unresolved** (author action).
* M2 — Novelty search limited; possible overlap of Thm 3 with SDP multi-option bounds (Bertsimas–Popescu). **Unresolved** (mentor check).
* M3 — Word rendering of the DOCX not verified (LibreOffice 24.2 used for PDF). Page 9 has ~30% spare space as buffer. **Partially resolved.**
* M4 — Corresponding e-mail and funding/conflict statements supplied by the author. **Resolved.** Affiliation postcode still missing (author action).

## Minor
* m1 — Sharpness of Thm 2 conjectural (stated as such). Resolved by wording.
* m2 — Prop. 4 one-sided derivative statement corrected. Resolved.
* m3 — Affordability constraint claimed binding in an early draft; corrected to slack (Rs 549.89 < 550). Resolved.
* m4 — Design E revenue ratio initially assumed; verified (0.990). Resolved.
* m5 — Appendix numbering aligned with manuscript. Resolved.
* m6 — Scarf (1958) chapter and ISBN-based references verified by search, not by publisher pages. Accepted.

## Checks that passed
* 26/26 pytest tests; validate.py: all independent recomputations match (household penalties, decomposition, all bounds non-violated, design V_max and revenue).
* Adversarial searches: no bound violation; Thm 1/3 attained; Thm 2 matched in 148/148 cases.
* PDF page counts: identified 12, blinded 12 (pypdf + pdfinfo); every page visually inspected; no broken glyphs (text scan for U+00BF).
* Archive extracted to a clean directory and tests re-run (see Reproduction_Status.md).
