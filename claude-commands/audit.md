# AUDIT: AI-Assisted Security Review

## 1. Initialize Audit Workspace
- **Goal:** Set up documentation for tracking the audit process and findings.
- **Actions:**
    - Create `SECURITY_AUDIT.md`. Populate with initial sections: `Audit Scope & Goals`, `Methodology Notes`, `Exploratory Findings Log`, `Deep Dive Analysis Log`.
    - Create `SECURITY_PLAN.md`. Populate with initial sections: `Executive Summary`, `Detailed Findings and Recommendations`.
    - Add both `SECURITY_AUDIT.md` and `SECURITY_PLAN.md` to Git tracking (`git add`).

## 2. Systematic Exploratory Review
- **Goal:** Broadly scan the codebase and related artifacts for potential security weaknesses using defined strategies.
- **Methodology:** Employ multiple techniques. Log approach notes in `SECURITY_AUDIT.MD` under `Methodology Notes`. Examples:
    - **Keyword Search:** Search for known dangerous functions, common misconfigurations, TODOs related to security.
    - **Data Flow Analysis:** Trace handling of external inputs (HTTP requests, user input fields, API calls) through validation, processing, and storage/output.
    - **Component Review:** Examine files related to specific security areas:
        - Authentication & Authorization (Login, Roles, Permissions)
        - Session Management (Cookies, Tokens, Lifecycles)
        - Input Validation/Sanitization (API endpoints, Forms, DB queries)
        - Cryptography (Encryption methods, Key management)
        - Error Handling & Logging (Sensitive data exposure)
        - Dependencies (Check known vulnerabilities in third-party libraries using available tools like `npm audit`, `pip check`, etc.)
        - Configuration (Secrets management, Security headers, Infrastructure-as-Code files)
    - **Pattern Recognition:** Look for known anti-patterns (e.g., Hardcoded secrets, SQL injection vulnerabilities, XSS possibilities, insecure defaults) informed by OWASP Top 10.
- **Action:** As potential issues or areas needing deeper review are identified, log them immediately under `Exploratory Findings Log` in `SECURITY_AUDIT.md` including: brief description, file path(s), line number(s), initial thoughts.

## 3. Deep-Dive Analysis & Verification
- **Goal:** Investigate promising leads from the exploratory review to confirm vulnerabilities and assess potential impact.
- **Actions:**
    - Prioritize findings from the `Exploratory Findings Log` based on likely impact or ease of confirmation.
    - For each prioritized item:
        - ***Think hard***: Conduct focused code review and logical analysis to understand the potential vulnerability in detail.
        - **Use Available Tools:** Employ any configured security tools (SAST scanners, dependency checkers) to analyze the relevant code sections or dependencies.
        - **Document Analysis:** Record detailed findings, supporting evidence (code snippets, tool output), impact assessment (e.g., potential for data exposure, unauthorized access, DoS), and confidence level under `Deep Dive Analysis Log` in `SECURITY_AUDIT.MD`.
        - **Severity Estimation:** Assign a preliminary severity (Low, Medium, High) based on potential impact, noting that this requires human validation.

## 4. Create Remediation Plan
- **Goal:** Organize findings from the deep-dive analysis into a structured, actionable remediation plan.
- **Actions:**
    - Use architect to generate a comprehensive security plan based on findings:
        ```bash
        architect --instructions SECURITY_AUDIT.md --output SECURITY_PLAN.md docs/philosophy/ [relevant-security-files]
        ```
    - Review the remediation plan in `SECURITY_PLAN.MD`. Verify it includes:
        - A clear executive summary
        - Detailed findings with locations, evidence, and impact assessments
        - Severity ratings (Low/Medium/High)
        - Specific remediation steps for each finding
        - Verification procedures to confirm fixes

## 5. Finalize and Commit
- **Goal:** Save the completed audit documentation to version control.
- **Actions:**
    - Ensure both `SECURITY_AUDIT.MD` (containing the detailed logs) and `SECURITY_PLAN.MD` (containing the remediation plan) are saved with the latest information.
    - Stage both files (`git add SECURITY_AUDIT.MD SECURITY_PLAN.MD`).
    - Review the staged changes (`git diff --staged`).
    - Commit using the **Conventional Commits** format:
        - `chore(security): Conduct security audit and generate remediation plan`
        - Include a brief summary in the commit body if desired (e.g., "Audit identified X high, Y medium, Z low severity preliminary findings. See SECURITY_PLAN.md for details.").
    - Report "Security audit and plan committed successfully."
