#!/usr/bin/env python3
"""
EPOCH-AUDIT-TRAIL - Minimal v1.0
Independent Single-File Forensic Vault
Static Release - April 2026

LEGAL DISCLOSURE:
This is an independent open-source defensive safety tool.
Author: ZZZ_EPOCHE
No affiliation with xAI, Anthropic, Google, OpenAI, Mistral or any LLM provider.
Released under the MIT License for defensive and research purposes only.

WARNING: This version is explicitly not intended for use in the European Union or EEA.
It is not designed to meet EU AI Act or GDPR requirements.

© ZZZ_EPOCHE 2026 - Static Release (April 2026). No further updates.
"""

import json
import hashlib
import os
import re
import uuid
import sqlite3
import sys
import asyncio
import hmac
import shutil
from datetime import datetime, timedelta

print("EPOCH-AUDIT-TRAIL Minimal v1.0 | ZZZ_EPOCHE | MIT License | Defensive research only.")
print("Not for EU/EEA use. Static release April 2026.\n")

# ====================== KEY HANDLING ======================
KEY_FILE = "epoch_vault_key.txt"

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Error: cryptography is required.")
    print("Run: pip install cryptography")
    sys.exit(1)

if os.getenv("EPOCH_VAULT_KEY"):
    key = os.getenv("EPOCH_VAULT_KEY").strip().encode()
    print("✅ Using key from EPOCH_VAULT_KEY environment variable")
elif os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key = f.read().strip()
    print("✅ Loaded existing key from epoch_vault_key.txt")
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("🔑 New key generated and saved to epoch_vault_key.txt")
    print("⚠️  Protect this key file. Loss = permanent data loss.")

cipher = Fernet(key)
sign_key = key


class EpochForensicVault:
    def __init__(self):
        self.conn = sqlite3.connect("epoch_forensic_vault.db")
        self.last_hash = ""
        self._init_db()
        self._create_backup("startup")
        self._migrate_db()
        self._load_last_hash()

        print("\n📊 Database Statistics:")
        stats = self.get_stats()
        print(f"   Total entries     : {stats['total_entries']}")
        print(f"   Last entry time   : {stats['last_entry'] or 'None'}")
        print(f"   Database size     : {stats['db_size'] / 1024:.1f} KB")

        print("\n🔍 Performing initial full chain verification...")
        status = self.verify_chain()
        if status["valid"]:
            print(f"✅ Chain verified successfully — {status['entries']} entries intact")
        else:
            print(f"⚠️  CHAIN INTEGRITY WARNING: {status['message']}")

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                audit_id TEXT PRIMARY KEY,
                timestamp TEXT,
                prompt TEXT,
                grok_output TEXT,
                risk_score REAL,
                safe INTEGER,
                human_feedback TEXT,
                image_hash TEXT,
                previous_hash TEXT,
                signature TEXT,
                encrypted_entry BLOB
            )
        """)
        self.conn.commit()

    def _create_backup(self, reason: str):
        """Create timestamped backup before major operations"""
        db_file = "epoch_forensic_vault.db"
        if not os.path.exists(db_file):
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"epoch_forensic_vault_{timestamp}_{reason}.db.backup"
        try:
            shutil.copy2(db_file, backup_file)
            print(f"→ Forensic backup created: {backup_file}")
        except Exception as e:
            print(f"→ Warning: Backup failed ({reason}): {e}")

    def _migrate_db(self):
        cursor = self.conn.execute("PRAGMA table_info(audit_log)")
        existing = {row[1] for row in cursor.fetchall()}
        needed = {"prompt": "TEXT", "grok_output": "TEXT", "image_hash": "TEXT", "signature": "TEXT"}
        for col, col_type in needed.items():
            if col not in existing:
                print(f"→ Updating database: Adding missing column '{col}'...")
                try:
                    self.conn.execute(f"ALTER TABLE audit_log ADD COLUMN {col} {col_type}")
                    self.conn.commit()
                except Exception:
                    pass

    def _load_last_hash(self):
        if os.path.exists("epoch_vault_last_hash.txt"):
            with open("epoch_vault_last_hash.txt", encoding="utf-8") as f:
                self.last_hash = f.read().strip()

    def get_stats(self):
        try:
            total = self.conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
            last = self.conn.execute("SELECT timestamp FROM audit_log ORDER BY timestamp DESC LIMIT 1").fetchone()
            last_time = last[0] if last else None
            size = os.path.getsize("epoch_forensic_vault.db") if os.path.exists("epoch_forensic_vault.db") else 0
            return {"total_entries": total, "last_entry": last_time, "db_size": size}
        except Exception:
            return {"total_entries": 0, "last_entry": None, "db_size": 0}

    def _redact_pii(self, text: str) -> str:
        if not text: return ""
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]', text)
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE REDACTED]', text)
        return text

    def _compute_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode("utf-8")).hexdigest()

    def _assess_prompt(self, prompt: str, output: str, image_hash: str = None) -> dict:
        if (not prompt or prompt.strip() == "") and (not output or output.strip() == "") and image_hash:
            return {"risk_score": 0.10, "judgement": "🟢 LOW RISK - Image only (hash stored)", "safe": True}

        text = (prompt + " " + (output or "")).lower()
        dangerous = ["bomb", "explosive", "weapon", "kill", "murder", "hack", "illegal", "drugs", "terror", "child", "porn"]
        jailbreak_patterns = ["ignore previous", "dan mode", "developer mode", "jailbreak", "override all"]
        
        if any(word in text for word in dangerous):
            return {"risk_score": 0.92, "judgement": "🔴 HIGH RISK", "safe": False}
        elif any(p in text for p in jailbreak_patterns):
            return {"risk_score": 0.88, "judgement": "🔴 JAILBREAK ATTEMPT", "safe": False}
        elif len(text) > 2500 or re.search(r'base64|exec\(|eval\(|system\(', text):
            return {"risk_score": 0.65, "judgement": "🟠 SUSPICIOUS", "safe": True}
        return {"risk_score": 0.35, "judgement": "🟠 MEDIUM RISK", "safe": True}

    async def log_session(self, prompt="", grok_output="", risk_score=None, safe=None,
                          human_feedback=None, image_bytes=None):
        print("→ Redacting sensitive information (PII)...")
        prompt = self._redact_pii(prompt)
        grok_output = self._redact_pii(grok_output)
        image_hash = hashlib.sha256(image_bytes).hexdigest() if image_bytes else None

        print("→ Assessing risk level...")
        assessment = (self._assess_prompt(prompt, grok_output, image_hash) 
                      if risk_score is None 
                      else {"risk_score": float(risk_score), "judgement": "🔵 MANUAL OVERRIDE", "safe": bool(safe)})

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "audit_id": str(uuid.uuid4())[:16],
            "prompt": prompt,
            "grok_output": grok_output,
            "risk_score": assessment["risk_score"],
            "safe": assessment["safe"],
            "human_feedback": human_feedback,
            "image_hash": image_hash,
            "previous_hash": self.last_hash,
        }

        leaf_hash = self._compute_hash(entry)
        signature = hmac.new(sign_key, leaf_hash.encode(), hashlib.sha256).hexdigest()
        encrypted = cipher.encrypt(json.dumps(entry).encode("utf-8"))

        try:
            print("→ Encrypting and storing tamper-evident entry...")
            self.conn.execute("""
                INSERT INTO audit_log 
                (audit_id, timestamp, prompt, grok_output, risk_score, safe, human_feedback,
                 image_hash, previous_hash, signature, encrypted_entry)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                entry["audit_id"], entry["timestamp"], prompt, grok_output,
                entry["risk_score"], int(entry["safe"]), human_feedback,
                image_hash, self.last_hash, signature, encrypted
            ))
            self.conn.commit()

            self.last_hash = leaf_hash
            with open("epoch_vault_last_hash.txt", "w", encoding="utf-8") as f:
                f.write(leaf_hash)

            print(f"\n✅ [VAULT] Successfully logged entry {entry['audit_id']}")
            print(f"   Judgement : {assessment['judgement']}")
            print(f"   Risk      : {assessment['risk_score']:.2f}")
        except Exception as e:
            print(f"❌ [ERROR] Failed to log entry: {e}")

    def verify_chain(self) -> dict:
        """Detailed forensic chain verification"""
        try:
            rows = self.conn.execute("""
                SELECT audit_id, timestamp, previous_hash, signature, encrypted_entry 
                FROM audit_log ORDER BY timestamp ASC
            """).fetchall()

            if not rows:
                return {"valid": True, "entries": 0, "message": "Vault is empty", "details": []}

            prev_hash = ""
            valid_count = 0
            issues = []

            for row in rows:
                audit_id, ts, stored_prev, stored_sig, enc = row
                try:
                    decrypted = json.loads(cipher.decrypt(enc))
                    computed_hash = self._compute_hash({
                        k: v for k, v in decrypted.items() if k != "signature"
                    })

                    expected_sig = hmac.new(sign_key, computed_hash.encode(), hashlib.sha256).hexdigest()

                    if expected_sig != stored_sig:
                        issues.append(f"Signature mismatch at {audit_id} ({ts})")
                    if stored_prev != prev_hash:
                        issues.append(f"Chain break at {audit_id} ({ts}) - expected {prev_hash[:8]}... but got {stored_prev[:8]}...")

                    if issues:
                        return {"valid": False, "broken_at": audit_id, "message": issues[-1], "details": issues}

                    prev_hash = computed_hash
                    valid_count += 1
                except Exception as e:
                    issues.append(f"Decryption failed at {audit_id} ({ts}): {e}")
                    return {"valid": False, "broken_at": audit_id, "message": issues[-1], "details": issues}

            return {"valid": True, "entries": valid_count, 
                    "message": f"Full forensic chain verified — all {valid_count} entries intact",
                    "details": ["All hashes and signatures valid"]}
        except Exception as e:
            return {"valid": False, "message": f"Verification system error: {e}", "details": []}

    def query(self, days_back=7):
        cutoff = (datetime.utcnow() - timedelta(days=days_back)).isoformat()
        try:
            rows = self.conn.execute(
                "SELECT encrypted_entry FROM audit_log WHERE timestamp > ?", (cutoff,)
            ).fetchall()
            return [json.loads(cipher.decrypt(row[0])) for row in rows if row[0]]
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            return []


# ====================== VAULT ======================
vault = EpochForensicVault()


# ====================== MAIN MENU ======================
async def main():
    print("\n🚀 EPOCH-AUDIT-TRAIL Minimal v1.0 is ready.\n")

    while True:
        print("\n" + "="*80)
        print("EPOCH-AUDIT-TRAIL Minimal v1.0 - MAIN MENU")
        print("="*80)
        print("1. Log text prompt + model output")
        print("2. Log image (stores hash only for privacy)")
        print("3. View recent logs")
        print("4. Export all logs to JSON")
        print("5. Help")
        print("6. Exit")
        print("7. Verify audit chain integrity")
        print("="*80)

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            print("\n→ Logging text prompt + model output")
            prompt = input("Enter prompt: ").strip()
            output = input("Enter model output: ").strip()
            risk_str = input("Risk score (0.0-1.0 or empty for auto): ").strip()
            risk = float(risk_str) if risk_str else None
            feedback = input("Human feedback (optional): ").strip() or None
            await vault.log_session(prompt, output, risk, risk is None or risk < 0.7, feedback)

        elif choice == "2":
            print("\n→ Logging image (stores hash only for privacy)")
            path = input("Enter full path to image file (or press Enter to skip): ").strip()
            image_bytes = None
            if path and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        image_bytes = f.read()
                    print("✅ Image loaded and hashed.")
                except Exception as e:
                    print(f"Failed to read image: {e}")
            await vault.log_session(image_bytes=image_bytes)

        elif choice == "3":
            print("\n→ Retrieving recent logs...")
            results = vault.query()
            if results:
                print(f"\nRecent logs (last 5 of {len(results)} entries):")
                print(json.dumps(results[-5:], indent=2))
            else:
                print("No logs recorded yet.")

        elif choice == "4":
            print("\n→ Creating forensic backup before export...")
            vault._create_backup("pre_export")

            print("\n→ Verifying full chain before export...")
            verify_status = vault.verify_chain()
            print(f"   Chain status: {'✅ VALID' if verify_status['valid'] else '❌ INVALID'}")
            if not verify_status["valid"]:
                print(f"   WARNING: {verify_status['message']}")

            print("\n→ Exporting all logs to JSON with verification report...")
            data = vault.query(9999)
            export_data = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_entries": len(data),
                "chain_verification": verify_status,
                "logs": data
            }
            with open("audit_export.json", "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2)
            print(f"✅ Exported {len(data)} entries to audit_export.json")
            print("   Full verification report included in the export.")

        elif choice == "5":
            print("\nHelp:")
            print("1 - Log a text interaction with any model")
            print("2 - Log an image (only the hash is stored)")
            print("3 - Show recent logged entries")
            print("4 - Export everything to JSON file (with chain verification + backup)")
            print("5 - Show this help message")
            print("6 - Exit the program")
            print("7 - Verify the full tamper-evident chain")

        elif choice == "6":
            print("\nThank you for using EPOCH-AUDIT-TRAIL Minimal v1.0.")
            print("Your logs have been saved securely with enhanced forensic protection.")
            break

        elif choice == "7":
            print("\n🔍 Running detailed forensic chain verification...")
            status = vault.verify_chain()
            print(f"Status : {'✅ VALID' if status['valid'] else '❌ INVALID'}")
            print(f"Details: {status['message']}")
            if "details" in status and status["details"]:
                for detail in status["details"]:
                    print(f"   → {detail}")

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

        if choice != "6":
            again = input("\nDo another action? (y/n): ").strip().lower()
            if again != "y":
                print("\nThank you for using EPOCH-AUDIT-TRAIL v1.0.")
                break


if __name__ == "__main__":
    asyncio.run(main())