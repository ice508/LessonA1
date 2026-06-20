-- 1. Create the students table if it doesn't exist yet
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);

-- 2. Insert some prerequisite starter data
-- 'INSERT OR IGNORE' prevents crashes if you run this script multiple times
INSERT OR IGNORE INTO students (student_id, name, age) VALUES ('STU101', 'Alice Smith', 15);
INSERT OR IGNORE INTO students (student_id, name, age) VALUES ('STU102', 'Bob Jones', 16);
INSERT OR IGNORE INTO students (student_id, name, age) VALUES ('STU103', 'Charlie Brown', 15);
INSERT OR IGNORE INTO students (student_id, name, age) VALUES ('STU104', 'Diana Prince', 17);