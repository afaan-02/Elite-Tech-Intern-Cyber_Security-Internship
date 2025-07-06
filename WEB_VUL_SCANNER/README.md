# 🌐 Web Vulnerability Scanner

This is a lightweight Python-based Web Vulnerability Scanner that checks for common vulnerabilities in web applications, including:

- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Open Redirects

> ✅ Developed as part of the ELite Tech Cybersecurity Internship — Project 2.

---

## 🔍 What It Does

- Crawls web pages recursively to find forms and URLs
- Detects vulnerable input fields using test payloads
- Prints out possible injection points for manual verification

---

## 🛠️ Features

- Detects:
  - 🔎 SQL Injection
  - 💉 Reflected XSS
  - 🔀 Open Redirect
- Crawls websites using links and forms
- Simple payload injection with response comparison

---

## 📦 Requirements

- Python 3.x  
- `requests`, `beautifulsoup4` libraries

Install with:

```bash
pip install -r requirements.txt
