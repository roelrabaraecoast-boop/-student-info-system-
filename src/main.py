import logging


from services.student_service import StudentService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


class StudentInformationSystem:

    def __init__(self):
        self.student_service = StudentService()
        self.logger = logging.getLogger(__name__)

    def display_menu(self):
        print("\n=== Student Information System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

    def add_student(self):
        print("\n--- Add New Student ---")

        name = input("Name: ").strip()
        email = input("Email: ").strip()
        course = input("Course: ").strip()
        year_level = input("Year Level: ").strip()

        if not all((name, email, course, year_level)):
            print("All fields are required.")
            return

        student_data = {
            "name": name,
            "email": email,
            "course": course,
            "year_level": year_level,
        }

        try:
            student = self.student_service.add_student(student_data)

            self.logger.info(
                "Added student ID: %s",
                student["student_id"],
            )

            print(
                "Student added successfully! "
                f"ID: {student['student_id']}"
            )

        except Exception as error:
            self.logger.exception("Error adding student")
            print(f"Error adding student: {error}")

    def view_all_students(self):
        print("\n--- All Students ---")

        students = self.student_service.get_all_students()

        if not students:
            print("No students found.")
            return

        for student in students:
            print(
                f"ID: {student['student_id']}, "
                f"Name: {student['name']}, "
                f"Email: {student['email']}, "
                f"Course: {student['course']}, "
                f"Year Level: {student['year_level']}"
            )

    def view_student(self):
        student_id = input("Enter Student ID: ").strip()

        student = self.student_service.get_student(student_id)

        if student:
            print("\n--- Student Details ---")

            for key, value in student.items():
                print(
                    f"{key.replace('_', ' ').title()}: {value}"
                )
        else:
            print("Student not found.")

    def update_student(self):
        student_id = input(
            "Enter Student ID to update: "
        ).strip()

        current_student = self.student_service.get_student(
            student_id
        )

        if not current_student:
            print("Student not found.")
            return

        print("Leave a field blank to keep its current value.")

        update_data = {}

        for field in ("name", "email", "course", "year_level"):
            current_value = current_student.get(field, "")
            new_value = input(
                f"{field.replace('_', ' ').title()} "
                f"[{current_value}]: "
            ).strip()

            if new_value:
                update_data[field] = new_value

        if not update_data:
            print("No changes made.")
            return

        student = self.student_service.update_student(
            student_id,
            update_data,
        )

        if student:
            print("Student updated successfully.")
        else:
            print("Update failed.")

    def delete_student(self):
        student_id = input(
            "Enter Student ID to delete: "
        ).strip()

        confirm = input(
            "Are you sure you want to delete this student? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("Delete cancelled.")
            return

        if self.student_service.delete_student(student_id):
            print("Student deleted successfully.")
            self.logger.info("Deleted student ID: %s", student_id)
        else:
            print("Student not found.")

    def run(self):
        while True:
            self.display_menu()

            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_all_students()

            elif choice == "3":
                self.view_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = StudentInformationSystem()
    app.run()