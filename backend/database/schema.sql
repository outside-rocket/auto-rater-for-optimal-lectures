CREATE TABLE teachers (
    faculty_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    photo TEXT,
    subjects TEXT
);

CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    group_name TEXT,
    timestamp TEXT,
    user_hash TEXT,
    message TEXT,
    reply_to TEXT
);

CREATE TABLE teacher_mentions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT,
    faculty_id TEXT,
    confidence REAL
);

CREATE TABLE teacher_insights (
    faculty_id TEXT PRIMARY KEY,
    attendance_strictness TEXT,
    general_strictness TEXT,
    assignment_load TEXT,
    teaching_clarity TEXT,
    marking_leniency TEXT,
    exam_difficulty TEXT,
    lab_difficulty TEXT,
    doubt_support TEXT,
    confidence REAL,
    summary TEXT,
    last_updated TEXT
);