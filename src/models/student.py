from datetime import datetime
import uuid


class Student:
    def __init__(self, student_id, name, email, course, year_level, gpa=0.0):
        self.student_id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.course = course
        self.year_level = year_level
        self.gpa = gpa
        self.created_at = datetime.now().isoformat(timespec="seconds")
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "year_level": self.year_level,
            "gpa": self.gpa,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(
            data.get("student_id", ""),
            data.get("name", ""),
            data.get("email", ""),
            data.get("course", ""),
            data.get("year_level", ""),
            data.get("gpa", 0.0),
        )

        student.created_at = data.get(
            "created_at", student.created_at
        )
        student.updated_at = data.get(
            "updated_at", student.updated_at
        )

        return student