import json
from datetime import datetime

def scan():
    opportunities = [
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": "New Tsukuba Reconfigurable Hardware Position",
            "deadline": "2026-11-30",
            "match": "High"
        },
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": "MEXT 2027 Embassy Track",
            "deadline": "2026-05-01",
            "match": "High"
        }
    ]
    
    with open('opportunities.json', 'w') as f:
        json.dump(opportunities, f, indent=2)

if __name__ == "__main__":
    scan()
