import json

with open("unclean.json","r",encoding="utf-8") as f:
    data=json.load(f)

cleaned=[]
print("Original:", len(data))
print("Cleaned :", len(cleaned))
for item in data:

    cleaned.append({
        "message": item.get("message",""),
        "context": item.get("caption",""),
        "id": item.get("messageId","")
    })

with open("clean.json","w",encoding="utf-8") as f:
    json.dump(cleaned,f,indent=2,ensure_ascii=False)

print(f"processed messages {len(cleaned)}")
