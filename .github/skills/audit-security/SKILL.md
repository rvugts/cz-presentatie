---
name: audit-security
description: Perform a comprehensive security audit of the current codebase, identifying vulnerabilities and providing remediation strategies based on OWASP Top 10 2025 standards.
---

# Security Audit Skill

## Role
Act as an Expert Lead Application Security Engineer and Penetration Tester. Your goal is to audit the provided code for vulnerabilities, strictly adhering to **OWASP Top 10 2025** standards while performing deep-dive analyses on Authentication, Input Validation, and Dependencies.

## Constraints
1. **NO FIXES:** Do not alter the code. Do not suggest code rewrite blocks unless necessary for a brief example.
2. **IDENTIFY ONLY:** Flag issues, explain the risk, and provide a remediation strategy.
3. **OUTPUT FORMAT:** Write the report to a single file: `SECURITY_AUDIT_REPORT.md` at the project root (create it; do not only output a code block).
4. **EVIDENCE:** For each finding, cite file path and line number(s) and include a short code snippet or quote where relevant.
5. **SEVERITY:** Use consistent severity levels—define them once in the report and apply consistently (e.g. Critical = exploitable for RCE/auth bypass/data breach; High = likely exploitable with moderate effort; Medium = weak control or best-practice gap; Low = hardening/recommendation).

## Comprehensive Audit Checklist

### 1. OWASP Top 10 2025 & General Security
*   **A01: Broken Access Control:** Check for IDOR, missing role checks, bypassed authorization, and SSRF.
*   **A02: Security Misconfiguration:** Default accounts, verbose error messages, open cloud storage, missing security headers (CSP, HSTS).
*   **A03: Software Supply Chain Failures (Expanded):**
    *   Scan `package.json`, `requirements.txt`, `go.mod` for outdated packages.
    *   Check for strict version pinning (avoid `^` or `*` or `latest`).
    *   Identify unnecessary dependencies or "bloat".
    *   Flag lack of lock files (`package-lock.json`, `yarn.lock`, etc.).
*   **A04: Cryptographic Failures:** Weak hashing (MD5/SHA1), hardcoded keys, transmission of sensitive data over HTTP.
*   **A05: Injection:** SQLi (verify parameterization), NoSQLi, Command Injection, LDAP injection.
*   **A06: Insecure Design:** Lack of rate limiting, lack of captcha, business logic flaws.
*   **A07: Identification and Authentication Failures (Deep Dive):**
    *   **Password Handling:** Check for complexity enforcement, secure hashing (Argon2/Bcrypt).
    *   **Sessions:** Verify secure cookies (HttpOnly, Secure, SameSite), session timeouts, and fixation protections.
    *   **Tokens:** Check JWT signature verification, secret strength, and algorithm enforcement (None algo attacks).
    *   **Features:** Check for MFA support gaps and secure password reset flows (no enum/timing attacks).
*   **A08: Software or Data Integrity Failures:** Unsafe deserialization, unverified CI/CD artifacts.
*   **A09: Logging & Alerting Failures:** Missing audit logs for critical actions (login/payment).
*   **A10: Mishandling of Exceptional Conditions:** Empty catch blocks, silent failures, leaking stack traces.

### 2. Deep Input Validation Audit
*   **Sanitization:** Verify all user inputs (headers, query params, body) are sanitized to prevent XSS (Reflected/Stored).
*   **Type Enforcement:** Ensure strict type checking is used on API endpoints.
*   **Constraints:** Check for defined length limits, range checks, and regex patterns on string inputs.
*   **Allow-listing:** Verify validation uses allow-lists (positive validation) rather than block-lists.

### 3. Infrastructure & Secrets
*   **Secrets Detection:** Scan for hardcoded API keys, tokens, passwords, DB credentials, or private keys.
*   **Environment:** Verify usage of `.env` variables vs hardcoded strings.
*   **Access Controls:** Check for hardcoded IP whitelists or insecure CORS configurations (`Access-Control-Allow-Origin: *`).

### 4. Scope and Prioritization
*   **In scope:** Application source (routes, auth, APIs, server config, env handling). Include dependency manifests and lockfiles; do not deeply scan binary/vendor blobs unless relevant.
*   **Exclude from file paths:** `node_modules/`, `vendor/`, `.git/`, build artifacts, and third-party SDKs unless auditing their usage.
*   **Stack-aware:** Adapt emphasis to the stack (e.g. SQL/ORM usage for backends, client-side sanitization and CSP for frontends, OAuth/JWT for auth). When citing OWASP or standards, use current OWASP Top 10 and link or name the category (e.g. A01 Broken Access Control). For dependency CVEs, prefer CVE IDs and severity where available.

## Output Structure (SECURITY_AUDIT_REPORT.md)

Generate a markdown file with the following exact structure:

# Security Audit Report
**Date:** [Current Date]
**Auditor:** GitHub Copilot Security Agent
**Target Scope:** [Project Root/Files Analyzed]

## 1. Executive Summary
*   **Overall Security Score:** [1-10] (10 being most secure)
*   **Critical Issues:** [Count]
*   **High Issues:** [Count]
*   **Medium/Low Issues:** [Count]
*   **Summary:** [Brief paragraph summary of the security posture]

**Severity definitions (use consistently):**
*   **Critical:** Directly exploitable for RCE, auth bypass, or significant data breach.
*   **High:** Likely exploitable with moderate effort; missing critical controls.
*   **Medium:** Weak control or best-practice gap; lower likelihood or impact.
*   **Low:** Hardening or recommendation; defense in depth.

## 2. Critical Vulnerabilities (Immediate Action Required)
*(List issues that allow RCE, SQLi, Auth Bypass, or Data Leaks)*

| ID | Category | File | Line | Description |
|----|----------|------|------|-------------|
| 1  | SQL Injection | `db.js` | 42 | Raw query concatenation used... |

## 3. Detailed Analysis

### A. Authentication & Session Security
*   [Findings regarding passwords, tokens, MFA, sessions]

### B. Input Validation & Data Integrity
*   [Findings regarding sanitization, type checking, XSS prevention]

### C. Dependency & Supply Chain
*   [Findings regarding outdated packages, version pinning, CVEs]

### D. Infrastructure & Configuration
*   [Findings regarding secrets, headers, error handling]

## 4. Positive Security Controls Observed
*(Optional but recommended: note existing good practices—e.g. parameterized queries, secure headers, dependency pinning—to give a balanced view and support compliance narratives)*

## 5. Remediation Plan
*(Prioritized list of recommendations with target timeframes)*
1.  **Immediate:** [Fix X]
2.  **Short-term:** [Update Y]
3.  **Long-term:** [Implement Z]

---

## Execution Instruction
Read the provided codebase context. Analyze the files deeply—prioritizing authentication logic, API controllers, database interaction layers, and configuration files. Write the report to `SECURITY_AUDIT_REPORT.md` at the project root.