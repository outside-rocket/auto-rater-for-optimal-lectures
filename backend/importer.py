import json

with open("../data/raw/sample_export.json","r",encoding="utf-8") as f:
    raw = json.load(f)

processed = []

for i,msg in enumerate(raw):
    processed.append({
        "message_id":f"msg_{i}",
        "timestamp":msg["timestamp"],
        "user_hash":"anon",
        "message":msg["message"],
        "reply_to":None
    })

with open("../data/processed/messages.json","w",encoding="utf-8") as f:
    json.dump(processed,f,indent=2)

print(f"Processed {len(processed)}")