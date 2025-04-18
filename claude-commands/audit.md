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
    - Generate plan using architect:
        ```bash
        architect --instructions SECURITY_AUDIT.md --output-dir architect_output --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model o4-mini --model gpt-4.1 ./
        ```
    - **Review & Synthesize:**
        1. Review all `architect_output` files.
        2. ***Think hard*** & synthesize into a single `SECURITY_PLAN.md`.
    - Verify `SECURITY_PLAN.MD` includes: Summary, Detailed Findings (location, evidence, impact, severity), Specific Remediation Steps, Verification Procedures.

