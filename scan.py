import json
from datetime import datetime

opportunities = [
    {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": "Test Opportunity",
        "deadline": "2026-12-15",
        "match": "High"
    }
]

with open("opportunities.json", "w") as f:
    json.dump(opportunities, f, indent=2)

print("Created opportunities.json")
