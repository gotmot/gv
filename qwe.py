import sqlite3

conn = sqlite3.connect('University.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    StudentID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INTEGER PRIMARY KEY,
    CourseName TEXT,
    Credits INTEGER
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Enrollments (
    StudentID INTEGER,
    CourseID INTEGER,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
)''')

students = [(1, 'Иван', 'Иванов'), (2, 'Анна', 'Петрова')]
courses = [(101, 'Python', 4), (102, 'Базы данных', 3)]
enrollments = [(1, 101), (1, 102), (2, 101)]

cursor.executemany('INSERT OR IGNORE INTO Students VALUES (?, ?, ?)', students)
cursor.executemany('INSERT OR IGNORE INTO Courses VALUES (?, ?, ?)', courses)
cursor.executemany('INSERT OR IGNORE INTO Enrollments VALUES (?, ?)', enrollments)
conn.commit()

print("Список студентов и их курсов:")
query = '''
SELECT s.FirstName, s.LastName, c.CourseName
FROM Students s
JOIN Enrollments e ON s.StudentID = e.StudentID
JOIN Courses c ON e.CourseID = c.CourseID
'''
cursor.execute(query)
for row in cursor.fetchall():
    print(f"Студент: {row[0]} {row[1]} | Курс: {row[2]}")

cursor.execute('DELETE FROM Enrollments')
cursor.execute('DELETE FROM Students')
cursor.execute('DELETE FROM Courses')
conn.commit()

print("\nТаблицы успешно очищены.")
conn.close()
