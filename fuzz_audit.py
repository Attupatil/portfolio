import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

PAYLOADS = [
    "/portfolio.db",
    "/.env",
    "/static/portfolio.db",
    "/static/.env",
    "/templates/portfolio.db",
    "/../../portfolio.db",
    "/%2e%2e/%2e%2e/portfolio.db",
    "/view_db.py",
    "/app.py",
    "/models.py"
]

def run_audit():
    print(f"--- Starting Security Fuzzing Audit on {BASE_URL} ---")
    vulnerabilities_found = 0
    
    for path in PAYLOADS:
        url = BASE_URL + path
        try:
            response = requests.get(url, timeout=5)
            # A 200 OK for these paths is a CRITICAL vulnerability
            if response.status_code == 200:
                print(f"[CRITICAL] Exposed Sensitive File: {path} (Status: 200 OK)")
                vulnerabilities_found += 1
            elif response.status_code == 403:
                print(f"[SAFE] Access Forbidden: {path} (Status: 403)")
            elif response.status_code == 404:
                print(f"[SAFE] File Not Found/Blocked: {path} (Status: 404)")
            else:
                print(f"[INFO] Path {path} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Could not connect to the local server. Is it running?")
            sys.exit(1)
            
    if vulnerabilities_found == 0:
        print("\n--- Audit Complete: NO sensitive files exposed to web traffic! ---")
    else:
        print(f"\n--- Audit Complete: {vulnerabilities_found} vulnerabilities detected! ---")

if __name__ == "__main__":
    run_audit()
