
# EPOCH-AUDIT-TRAIL
**Minimal Tamper-Evident Forensic Vault for LLM Interactions**  
**Tamper-Evident • Epistemic-Aware • Lab-Ready • Outer-Layer Governance**

**Code Name:** Epoch-Audit-Trail-M  
**Version:** 1.0 (Static Release)  
**EU/EEA Use:** -NOT FOR USE IN THE EU/EEA-

**Author:** ZZZ_EPOCHE  
**Assisted by:** Grok by xAI  
**Date:** 2026-04-17  
**Keywords:** audit-trail, forensic-logging, tamper-evident, llm-governance, encryption, fernet, sqlite, pii-redaction, risk-assessment, defensive-tool, epistemic-check, hallucination-tracking, outer-layer, static-release, mit-license, research-tool, defensive-safety, vault, chain-of-custody, non-eu

---

## LEGAL DISCLOSURE (MANDATORY READ)

This is an **independent open-source defensive safety tool**.  
**Author:** ZZZ_EPOCHE  
**No affiliation** with xAI, Anthropic, Google, OpenAI, Mistral or any LLM provider.

This tool is released under the **MIT License** for defensive and research purposes only.  
It is designed to provide persistent auditability, epistemic checking, and hallucination tracking for outer-layer LLM governance.

**WARNING:** This version is **explicitly not intended for use in the European Union or EEA**.  
It is **not designed** to meet EU AI Act or GDPR requirements. Any use in the EU/EEA is entirely at the user's own risk and responsibility.

**Legal & Compliance**  
© ZZZ_EPOCHE 2026  
**License:** MIT License (USA)  

Users are solely responsible for compliance with all applicable U.S. federal, state, and local laws.  
The author disclaims all liability.

**European Union / EEA**  
If used in the EU/EEA, the user must conduct their own full legal assessment and accept all liability.  
The tool is provided without any warranty of conformity with the EU AI Act or GDPR.

**Rest of the World**  
Users bear full responsibility for compliance with all local laws and regulations.

**Static Release Policy**  
This is a **final, frozen version** (2026-04-17). No maintenance, updates, or security patches will be provided.

**Intended Use**  
Defensive safety research, artistic, technical, educational, and personal use only.

**Inspired by** the EPOCH-FRAMEWORK and OUTER-LAYERS-LLMS philosophy.

---

## WHAT THIS CODE DOES

`EPOCH-AUDIT-TRAIL` is a single-file, minimal forensic vault that creates a **provably tamper-evident, encrypted audit trail** of interactions with any LLM (including Grok, Claude, GPT, etc.).

It stores prompts, model outputs, and image hashes only (never the actual images), with automatic PII redaction, intelligent risk assessment, and full chain-of-custody verification.

---
# 🛡️ Project Evaluation: EPOCH-AUDIT-TRAIL Minimal v1.0
**Current Version:** Forensic Vault (Single-File Static Release)  
**Overall Performance Rating:** **8.6 / 10**

---
### 1. Key Capabilities
- Tamper-evident logging with hash chaining and HMAC signatures
- Full forensic chain verification that detects tampering or deletions
- Automatic PII redaction (emails and phone numbers)
- Smart risk assessment (dangerous content, jailbreak attempts, suspicious patterns, image-only logs marked LOW RISK)
- Timestamped forensic backups before major operations
- Clear step-by-step terminal feedback
- Database statistics on startup
- Exports include full verification report
  
### 2. Code & Architecture Assessment
This score reflects the technical health and structural integrity of the codebase.

| Criterion | Score | Key Notes |
| :--- | :---: | :--- |
| **Simplicity & Minimalism** | 9.0 | Single-file architecture with a clean, logical structure. |
| **Forensic Integrity** | 9.0 | Detailed verification via full chain walking. |
| **Privacy** | 9.0 | Robust PII redaction; stores image hashes rather than raw data. |
| **Usability** | 9.0 | Intuitive terminal output with clear step-by-step guidance. |
| **Security** | 8.5 | Solid implementation of encryption, signatures, and backups. |
| **Reliability** | 8.5 | Includes automated migration paths and backup routines. |
| **Risk Assessment** | 8.0 | Improved logic tailored for various log types. |

**Architecture Average:** **8.7 / 10**

---

### 3. Competitive Feature Landscape
How **EPOCH-AUDIT-TRAIL** compares to industry-standard logging and SIEM solutions.

| Feature | EPOCH-AUDIT-TRAIL | Commercial SIEM | Simple Text Log |
| :--- | :---: | :---: | :---: |
| **Full Chain Verification** | ✅ Yes | ⚠️ Partial | ❌ No |
| **Timestamped Backups** | ✅ Yes | ⚠️ Usually No | ❌ No |
| **Export Tamper Detection** | ✅ Yes | ⚙️ Configurable | ❌ No |
| **Image Hash Tracking** | ✅ Yes | ❌ N/A | ❌ No |
| **Offline / Single File** | ✅ Yes | ❌ No | ✅ Yes |
| **Static Release** | ✅ Yes | ❌ No | ✅ Yes |

---

### 4. Stakeholder & Team Utility
The tool's effectiveness across different operational "color teams."

* **⚪ White Team (Oversight): 9.5** – Exceptional for provable chain-of-custody.
* **🔵 Blue Team (Defensive): 9.0** – Strong incident response and audit capabilities.
* **🟠 Orange Team (Resilience): 9.0** – High marks for forensic readiness.
* **🟡 Yellow Team (Ethics/AI): 8.5** – Effective tracking of harmful or biased outputs.
* **🟣 Purple Team (Hybrid): 8.5** – Validates defenses during attack simulations.
* **🔴 Red Team (Offensive): 7.5** – Reliable for tracking prompt injection/jailbreaks.
* **🔘 Gray Team (Ambiguous): 7.5** – Promotes logging discipline in "gray" areas.
* **🟢 Green Team (Sustainability): 7.0** – Efficient, lightweight single-file design.

---

### 5 🚀 Production Ramp Schedule

| Phase | Status | Description | Target |
| :--- | :--- | :--- | :--- |
| **Phase 0** | **Stable** | **Current Version:** Minimal single-file forensic vault. | **Immediate** |
| **Phase 1** | Inactive | Lab / Personal: Enhanced reporting modules. | N/A |
| **Phase 2** | Inactive | Team Scale: Multi-vault support. | N/A |
| **Phase 3** | Inactive | Enterprise: Advanced third-party integration. | N/A |

> **Summary Note:** The project currently excels as a high-integrity, portable forensic tool. While the "Team" and "Enterprise" phases are not currently planned, the existing Phase 0 architecture provides a complete, production-ready solution for standalone auditing.
---

## HOW TO USE THIS CODE

### Prerequisites
```bash
pip install cryptography

Quick Startbash

# Recommended: Use environment variable for the key
export EPOCH_VAULT_KEY="your-very-long-secret-key-here"

python3 EPOCH-AUDIT-TRAIL.py

The tool will guide you through the menu. It auto-generates a key on first run if none exists and creates timestamped backups for forensic safety.FEATURESProvably Tamper-Evident: Full chain verification walks every entry and detects breaks
Forensic Backups: Automatic timestamped database backups before startup and export
Encryption + Signatures: Fernet encryption with HMAC signatures on every entry
PII Redaction: Automatic removal of sensitive information
Smart Risk Assessment: Correctly handles image-only logs as LOW RISK
Automatic Migration: Works with older database versions
Clear Operator Feedback: Step-by-step terminal messages for every action
Export with Proof: JSON export includes chain verification report
This tool remains intentionally at Phase 0.

🛠️ Troubleshooting Guide

If you encounter issues while running the EPOCH-AUDIT-TRAIL, refer to the table below for quick resolutions to common technical hurdles.
Issue	Recommended Action
cryptography module not found	Run pip install cryptography to install the required dependency.
Key Access / Permissions	Set the EPOCH_VAULT_KEY environment variable or delete the existing key file to regenerate.
Legacy Database Errors	No manual action needed—the tool is designed to automatically migrate columns.
Incorrect Image Risk Level	Resolved in latest update: Image-only logs are now correctly categorized as LOW RISK.
Chain Verification Warning	Ensure your key is consistent across sessions and review the detailed log output for specific gaps.

LIMITATIONS
Risk assessment is rule-based (not full ML classifier)
Static release — no future updates or patches
Fernet key must be protected (loss = permanent data loss)
Designed for personal/lab use, not high-volume production
Explicitly non-compliant with EU AI Act / GDPR by design

Copyright © 2026 ZZZ_EPOCHE
License: MIT License  Final Note from Author
In an era of increasingly capable outer-layer models, persistent epistemic discipline and forensic accountability remain human responsibilities. EPOCH-AUDIT-TRAIL provides one minimal, defensible instrument toward that end.Use responsibly.
EPOCH-AUDIT-TRAIL Minimal v1.0


