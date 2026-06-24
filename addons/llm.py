import json
import sqlite3
import ollama
from datetime import datetime
from rapidfuzz import process,fuzz
from pathlib import Path

CHUNK_SIZE=10

image_folder=Path("../images")

faculty=[]

for file in image_folder.iterdir():
    if file.is_file():
        faculty.append(file.stem)

def match_faculty(name,faculty):
    if not name:
        return None

    result=process.extractOne(
        name,
        faculty,
        scorer=fuzz.token_sort_ratio
    )

    if result and result[1]>=85:
        return result[0]

    return None

with open("clean2_1.json","r",encoding="utf-8") as f:
    data=json.load(f)

total_chunks=(len(data)+CHUNK_SIZE-1)//CHUNK_SIZE

conn=sqlite3.connect("teachers.db")
cur=conn.cursor()

for chunk_no,start in enumerate(range(0,len(data),CHUNK_SIZE),1):

    print(f"\nProcessing chunk {chunk_no}/{total_chunks}")

    chunk=data[start:start+CHUNK_SIZE]

    prompt=f"""
You are an information extraction system.

Extract structured teacher feedback from WhatsApp messages.

Return ONLY valid JSON array.

JSON FORMAT:
[
  {{
"teacher": "FULL NAME OR NULL",
"teaching_clarity": 1-10 or null,
"assignment_load": 1-10 or null,
"marking_leniency": 1-10 or null,
"strictness": 1-10 or null,
"comments": ["short factual point"]
}}
]

Rules:
- Extract only explicit information
- Do not guess missing values
- Use null if unknown
- Skip if no teacher mentioned
- comments must be short factual points

Messages:
        {json.dumps(chunk,ensure_ascii=False,separators=(",",":"))}
        """

    try:
        response=ollama.chat(
            model="llama3.1:8b-instruct-q4_K_M",
            messages=[
                {"role":"user","content":prompt}
            ],
            options={
                "temperature":0,
                "num_ctx":4096,
                "num_predict":512
            }
        )

        content=response["message"]["content"].strip()

        if "```json" in content:
            content=content.split("```json",1)[1].split("```",1)[0]
        elif "```" in content:
            content=content.split("```",1)[1].rsplit("```",1)[0]

        teachers=json.loads(content)

        if isinstance(teachers,dict):
            teachers=[teachers]

        if not isinstance(teachers,list):
            continue

    except:
        continue

    print(f"Teachers found: {len(teachers)}")
    print(teachers)
    for t in teachers:

        if not isinstance(t,dict):
            continue

        name=match_faculty(
            (t.get("teacher") or "").strip(),
            faculty
        )

        if not name:
            continue

        cur.execute(
            "SELECT * FROM teachers WHERE name=?",
            (name,)
        )

        row=cur.fetchone()

        comments_list=t.get("comments",[])
        comments="\n".join(comments_list) if isinstance(comments_list,list) else ""

        if row is None:

            cur.execute("""
INSERT INTO teachers
VALUES(?,?,?,?,?,?,?,?,?,?,?)
                """,(
                    name,
                    t.get("teaching_clarity") or 0,
                    1 if t.get("teaching_clarity") is not None else 0,
                    t.get("assignment_load") or 0,
                    1 if t.get("assignment_load") is not None else 0,
                    t.get("marking_leniency") or 0,
                    1 if t.get("marking_leniency") is not None else 0,
                    t.get("strictness") or 0,
                    1 if t.get("strictness") is not None else 0,
                    comments,
                    datetime.now().isoformat()
                ))

        else:

            old_comments=set(row[9].split("\n") if row[9] else [])

            for c in comments_list:
                if isinstance(c,str) and c.strip():
                    old_comments.add(c.strip())

            merged_comments="\n".join(sorted(old_comments))

            clarity_sum=row[1]
            clarity_count=row[2]

            assignment_sum=row[3]
            assignment_count=row[4]

            leniency_sum=row[5]
            leniency_count=row[6]

            strictness_sum=row[7]
            strictness_count=row[8]

            if t.get("teaching_clarity") is not None:
                clarity_sum+=t["teaching_clarity"]
                clarity_count+=1

            if t.get("assignment_load") is not None:
                assignment_sum+=t["assignment_load"]
                assignment_count+=1

            if t.get("marking_leniency") is not None:
                leniency_sum+=t["marking_leniency"]
                leniency_count+=1

            if t.get("strictness") is not None:
                strictness_sum+=t["strictness"]
                strictness_count+=1

            cur.execute("""
UPDATE teachers
SET
clarity_sum=?,
clarity_count=?,
assignment_sum=?,
assignment_count=?,
leniency_sum=?,
leniency_count=?,
strictness_sum=?,
strictness_count=?,
comments=?,
last_updated=?
WHERE name=?
                """,(
                    clarity_sum,
                    clarity_count,
                    assignment_sum,
                    assignment_count,
                    leniency_sum,
                    leniency_count,
                    strictness_sum,
                    strictness_count,
                    merged_comments,
                    datetime.now().isoformat(),
                    name
                ))

    conn.commit()

conn.close()

print("\nCompleted")