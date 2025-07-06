# 🧾 File Integrity Checker

This Python-based File Integrity Checker monitors files for unauthorized changes by comparing their current cryptographic hash (SHA-256) to a previously stored value.

> ✅ Developed as part of the ELite Tech Cybersecurity Internship — Project 1.

---

## 🔍 What It Does

- Scans specified files or directories
- Computes SHA-256 hashes for integrity verification
- Alerts when files have been modified, added, or deleted
- Maintains a reference hash file for future comparisons

---

## 🛠️ How It Works

1. **Initial Run**:
   - Calculates and stores hashes for all target files
2. **Subsequent Runs**:
   - Compares current file hashes with stored ones
   - Reports **modified**, **new**, or **missing** files

---

## 📦 Requirements

- Python 3.x  
- No external libraries required

---

## 🚀 Usage

```bash
python integrity_checker.py --init /path/to/folder
python integrity_checker.py --check /path/to/folder
