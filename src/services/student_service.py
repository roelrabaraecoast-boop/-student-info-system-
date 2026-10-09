import json
from pathlib import Path
from datetime import datetime


from models.student import Student

class StudentService:
    def __init__(self, data_file="data/students.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(
            parents=True, exist_ok=True
        )

        if not self.data_file.exists():
            self._save_students([])

    def _load_students(self):
        try:
            with self.data_file.open(
                "r", encoding="utf-8"
            ) as file:
                data = json.load(file)
                return [
                    Student.from_dict(item).to_dict()
                    for item in data
                ]

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_students(self, students):
        with self.data_file.open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(students, file, indent=2)

    def add_student(self, student_data):
        students = self._load_students()

        student = Student(
            "",
            student_data["name"],
            student_data["email"],
            student_data["course"],
            student_data["year_level"],
            student_data.get("gpa", 0.0),
        )

        students.append(student.to_dict())
        self._save_students(students)

        return student.to_dict()

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        students = self._load_students()

        for student in students:
            if student["student_id"] == student_id:
                return student

        return None

    def update_student(self, student_id, update_data):
        students = self._load_students()

        for student in students:
            if student["student_id"] == student_id:

                for key in (
                    "name",
                    "email",
                    "course",
                    "year_level",
                    "gpa",
                ):
                    if (
                        key in update_data
                        and update_data[key] != ""
                    ):
                        student[key] = update_data[key]

                student["updated_at"] = (
                    datetime.now().isoformat(
                        timespec="seconds"
                    )
                )

                self._save_students(students)
                return student

        return None

    def delete_student(self, student_id):
        students = self._load_students()

        remaining = [
            student
            for student in students
            if student["student_id"] != student_id
        ]

        if len(remaining) == len(students):
            return False

        self._save_students(remaining)
        return True