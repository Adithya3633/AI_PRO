from django.core.management.base import BaseCommand

from dashboard.models import Role
from mcq.models import MCQQuestion


class Command(BaseCommand):
    help = "Seed beginner-friendly demo roles and MCQ questions."

    def handle(self, *args, **options):
        data = {
            "Python Developer": [
                ("Which keyword defines a function in Python?", ["func", "def", "function", "lambda"], "def"),
                ("Which data type is immutable?", ["list", "dict", "set", "tuple"], "tuple"),
                ("What does PEP 8 describe?", ["Testing", "Style guide", "Database design", "Deployment"], "Style guide"),
            ],
            "Java Developer": [
                ("Which keyword creates a subclass?", ["extends", "inherits", "super", "implements"], "extends"),
                ("Which method starts a Java program?", ["start", "run", "main", "init"], "main"),
                ("What is JVM?", ["Compiler", "Virtual machine", "Framework", "Package manager"], "Virtual machine"),
            ],
            "Frontend Developer": [
                ("Which language styles web pages?", ["HTML", "CSS", "SQL", "Python"], "CSS"),
                ("What does DOM stand for?", ["Document Object Model", "Data Object Map", "Digital Output Mode", "Design Object Model"], "Document Object Model"),
                ("Which API stores data in the browser?", ["fetch", "localStorage", "Promise", "querySelector"], "localStorage"),
            ],
            "SQL Developer": [
                ("Which command reads data?", ["INSERT", "SELECT", "UPDATE", "DELETE"], "SELECT"),
                ("Which clause filters rows?", ["WHERE", "ORDER BY", "GROUP BY", "JOIN"], "WHERE"),
                ("What does a primary key enforce?", ["Duplication", "Uniqueness", "Sorting", "Null values"], "Uniqueness"),
            ],
        }

        created_questions = 0
        for role_name, questions in data.items():
            role, _ = Role.objects.get_or_create(role_name=role_name)
            for question, options, answer in questions:
                _, created = MCQQuestion.objects.get_or_create(
                    role=role,
                    question=question,
                    defaults={
                        "option1": options[0],
                        "option2": options[1],
                        "option3": options[2],
                        "option4": options[3],
                        "correct_answer": answer,
                        "difficulty": "easy",
                    },
                )
                created_questions += int(created)

        self.stdout.write(self.style.SUCCESS(f"Seeded demo data. New questions: {created_questions}"))
