"""Script to create test data for the fitness app"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universidad_fit.settings')
django.setup()

from fitness.models_sql import ExerciseSQL, RoutineSQL, ProgressSQL, RecommendationSQL

def create_test_data():
    print("Creating test exercises...")

    # Create exercises
    exercise1 = ExerciseSQL.objects.create(
        name="Push-ups",
        type="fuerza",
        description="Standard push-ups for upper body strength",
        duration=5.0,
        difficulty="media",
        video_url="https://example.com/pushups",
        created_by="system"
    )
    print(f"Created exercise: {exercise1.name} (ID: {exercise1.id})")

    exercise2 = ExerciseSQL.objects.create(
        name="Running",
        type="cardio",
        description="Outdoor or treadmill running",
        duration=30.0,
        difficulty="baja",
        video_url="https://example.com/running",
        created_by="system"
    )
    print(f"Created exercise: {exercise2.name} (ID: {exercise2.id})")

    exercise3 = ExerciseSQL.objects.create(
        name="Squats",
        type="fuerza",
        description="Bodyweight squats for leg strength",
        duration=10.0,
        difficulty="media",
        video_url="https://example.com/squats",
        created_by="system"
    )
    print(f"Created exercise: {exercise3.name} (ID: {exercise3.id})")

    exercise4 = ExerciseSQL.objects.create(
        name="Yoga Stretching",
        type="movilidad",
        description="Full body stretching routine",
        duration=15.0,
        difficulty="baja",
        video_url="https://example.com/yoga",
        created_by="system"
    )
    print(f"Created exercise: {exercise4.name} (ID: {exercise4.id})")

    exercise5 = ExerciseSQL.objects.create(
        name="Burpees",
        type="cardio",
        description="High-intensity full body exercise",
        duration=8.0,
        difficulty="alta",
        video_url="https://example.com/burpees",
        created_by="system"
    )
    print(f"Created exercise: {exercise5.name} (ID: {exercise5.id})")

    print("\nCreating test routines...")

    # Create routines
    routine1 = RoutineSQL.objects.create(
        name="Beginner Full Body",
        description="A complete beginner workout routine",
        exercises_data={
            "exercises": [
                {"exercise_id": exercise1.id, "sets": 3, "reps": 10, "rest": 60},
                {"exercise_id": exercise3.id, "sets": 3, "reps": 15, "rest": 60},
                {"exercise_id": exercise4.id, "duration": 900}  # 15 min
            ]
        },
        created_by="system",
        is_pre_designed=True
    )
    print(f"Created routine: {routine1.name} (ID: {routine1.id})")

    routine2 = RoutineSQL.objects.create(
        name="Cardio Blast",
        description="High-intensity cardio workout",
        exercises_data={
            "exercises": [
                {"exercise_id": exercise2.id, "duration": 1800},  # 30 min
                {"exercise_id": exercise5.id, "sets": 5, "reps": 10, "rest": 45}
            ]
        },
        created_by="system",
        is_pre_designed=True
    )
    print(f"Created routine: {routine2.name} (ID: {routine2.id})")

    routine3 = RoutineSQL.objects.create(
        name="Strength Builder",
        description="Build muscle and strength",
        exercises_data={
            "exercises": [
                {"exercise_id": exercise1.id, "sets": 4, "reps": 12, "rest": 90},
                {"exercise_id": exercise3.id, "sets": 4, "reps": 20, "rest": 90}
            ]
        },
        created_by="system",
        is_pre_designed=True
    )
    print(f"Created routine: {routine3.name} (ID: {routine3.id})")

    print("\nTest data created successfully!")
    print(f"\nTotal exercises: {ExerciseSQL.objects.count()}")
    print(f"Total routines: {RoutineSQL.objects.count()}")
    print(f"Total progress entries: {ProgressSQL.objects.count()}")
    print(f"Total recommendations: {RecommendationSQL.objects.count()}")

if __name__ == "__main__":
    # Clear existing data
    print("Clearing existing data...")
    ExerciseSQL.objects.all().delete()
    RoutineSQL.objects.all().delete()
    ProgressSQL.objects.all().delete()
    RecommendationSQL.objects.all().delete()
    print("Existing data cleared.\n")

    create_test_data()
