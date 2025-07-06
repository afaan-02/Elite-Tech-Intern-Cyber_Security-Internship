import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Test payloads
XSS_PAYLOAD = "<script>alert('XSS')</script>"
SQL_PAYLOADS = ["' OR '1'='1", '" OR "1"="1', "';--", 'admin" --']

# Functions
def log(msg):
    output_text.insert(tk.END, msg + "\n")
    output_text.see(tk.END)

def get_forms(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        log(f"[ERROR] Failed to load URL: {e}")
        return []

def get_form_details(form):
    action = form.attrs.get("action", "")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        name = input_tag.attrs.get("name")
        input_type = input_tag.attrs.get("type", "text")
        if name:
            inputs.append({"name": name, "type": input_type})
    return {"action": action, "method": method, "inputs": inputs}

def submit_form(form, url, payload):
    target_url = urljoin(url, form["action"])
    data = {}
    for input_field in form["inputs"]:
        if input_field["type"] == "text":
            data[input_field["name"]] = payload
    try:
        if form["method"] == "post":
            return requests.post(target_url, data=data)
        else:
            return requests.get(target_url, params=data)
    except Exception as e:
        log(f"[ERROR] Request failed: {e}")
        return None

def scan_xss():
    url = url_entry.get().strip()
    if not url.startswith("http"):
        url = "http://" + url
    forms = get_forms(url)
    log(f"[+] Found {len(forms)} form(s) on {url}")

    for form in forms:
        details = get_form_details(form)
        response = submit_form(details, url, XSS_PAYLOAD)
        if response and XSS_PAYLOAD in response.text:
            log(f"[!!] XSS Vulnerability Found! Payload echoed in response.\nForm Details: {details}")
        else:
            log("[OK] No XSS vulnerability detected.")

def scan_sql_injection():
    url = url_entry.get().strip()
    if not url.startswith("http"):
        url = "http://" + url

    for payload in SQL_PAYLOADS:
        test_url = f"{url}?id={payload}"
        try:
            res = requests.get(test_url)
            if any(error in res.text.lower() for error in ["sql", "syntax", "mysql", "error", "oracle"]):
                log(f"[!!] SQL Injection Detected! Payload: {payload}")
                return
        except Exception as e:
            log(f"[ERROR] SQLi test failed: {e}")
    log("[OK] No SQL Injection detected.")

# ---------------- GUI ----------------

app = tk.Tk()
app.title("🛡 Web Vulnerability Scanner")
app.geometry("750x500")

tk.Label(app, text="Enter URL to Scan:", font=("Arial", 12)).pack(pady=10)

url_entry = tk.Entry(app, width=90)
url_entry.pack()

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Scan for XSS", command=scan_xss, width=20).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Scan for SQL Injection", command=scan_sql_injection, width=20).grid(row=0, column=1, padx=10)

output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=90, height=20)
output_text.pack(padx=10, pady=10)

app.mainloop()
