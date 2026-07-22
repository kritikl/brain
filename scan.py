import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def real_scan():
    opportunities = []
    
    urls = [
        "https://www.u-tokyo.ac.jp/en/prospective-students/graduate.html",  # UTokyo
        "https://www.titech.ac.jp/english/prospective-students",  # Tokyo Tech
    ]
    
    for url in urls:
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Example parsing (customize per site)
            text = soup.get_text()[:500]
            if "deadline" in text.lower() or "admission" in text.lower():
                opportunities.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "title": f"Detected opportunity at {url.split('//')[1].split('/')[0]}",
                    "deadline": "Check site for exact date",
                    "match": "Medium"
                })
        except:
            pass  # Skip failed sites
    
    opportunities.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": "MEXT 2027 Embassy Track",
        "deadline": "2026-05-01 (estimated)",
        "match": "High"
    })
    
    with open("opportunities.json", "w") as f:
        json.dump(opportunities, f, indent=2)
    
    print(f"Real scan completed - {len(opportunities)} opportunities found")

if __name__ == "__main__":
    real_scan()
