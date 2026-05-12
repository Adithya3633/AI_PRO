from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MCQQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.TextField()),
                ("option1", models.CharField(max_length=255)),
                ("option2", models.CharField(max_length=255)),
                ("option3", models.CharField(max_length=255)),
                ("option4", models.CharField(max_length=255)),
                ("correct_answer", models.CharField(max_length=255)),
                ("difficulty", models.CharField(choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], default="easy", max_length=20)),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="mcq_questions", to="dashboard.role")),
            ],
            options={"ordering": ["role", "difficulty", "id"]},
        ),
        migrations.CreateModel(
            name="MCQResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveIntegerField()),
                ("total_questions", models.PositiveIntegerField(default=0)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("time_taken", models.PositiveIntegerField(help_text="Time taken in seconds")),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="dashboard.role")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-date"]},
        ),
    ]
