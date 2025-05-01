# AUDIT: AI-Assisted Security Review

## 1. Init Workspace
- Create `SECURITY_AUDIT.md` (Sections: Scope & Goals, Methodology Notes, Exploratory Log, Deep Dive Log).
- Create `SECURITY_PLAN.md` (Sections: Summary, Findings & Recommendations).
- `git add SECURITY_AUDIT.md SECURITY_PLAN.md`.

## 2. Exploratory Review
- **Goal:** Scan codebase/artifacts for potential weaknesses.
- **Methodology:** Use multiple techniques (Keyword Search, Data Flow Analysis, Component Review [Auth, Session, Input, Crypto, Errors, Deps, Config], Pattern Recognition [OWASP Top 10]). Log approach notes in `SECURITY_AUDIT.MD` -> `Methodology Notes`.
- **Action:** Log potential issues (description, path:line, thoughts) in `SECURITY_AUDIT.md` -> `Exploratory Findings Log`.

## 3. Deep-Dive Analysis
- **Goal:** Investigate exploratory findings to confirm vulnerabilities and assess impact.
- **Actions:**
    - Prioritize findings from Exploratory Log.
    - For each item:
        - ***Think hard***: Analyze code logic.
        - Use security tools (SAST, dependency checkers) if available.
        - Document detailed findings, evidence, impact, confidence level in `SECURITY_AUDIT.MD` -> `Deep Dive Analysis Log`.
        - Assign preliminary severity (Low, Medium, High).

## 4. Create Remediation Plan
- **Goal:** Generate a structured, actionable plan from deep-dive findings.
- **Actions:**
    - Generate plan using thinktank:
        ```bash
        thinktank --instructions SECURITY_AUDIT.md $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_glance_files) $(find_philosophy_files)
        ```
    - Copy synthesis file to create `SECURITY_PLAN.md`

