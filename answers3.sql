CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    fullName TEXT(100),
    age INTEGER
);
INSERT INTO student (id, fullName, age) VALUES
(1, 'John Smith', 18),
(2, 'Emily Johnson', 19),
(3, 'Michael Brown', 20),
(4, 'Sarah Davis', 17);
UPDATE student 
SET age = 20 
WHERE id = 2;