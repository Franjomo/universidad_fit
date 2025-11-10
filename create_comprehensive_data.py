"""
Create comprehensive test data for MongoDB fitness tracking application
"""
import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universidad_fit.settings')
django.setup()

from fitness.models import Exercise, Routine, Progress, Recommendation, FollowUp
from accounts.models import User
from bson import ObjectId

def create_exercises():
    """Create 15-20 diverse exercises covering all types and difficulty levels"""
    print("\n" + "="*60)
    print("Creating Exercises...")
    print("="*60)
    
    exercises_data = [
        # Cardio - Baja
        {"name": "Caminata Rápida", "type": "cardio", "difficulty": "baja", 
         "description": "Caminata a ritmo rápido durante 30 minutos", "duration": 30.0,
         "video_url": "https://example.com/videos/caminata-rapida"},
        {"name": "Trote Suave", "type": "cardio", "difficulty": "baja",
         "description": "Trote ligero de 20 minutos", "duration": 20.0,
         "video_url": "https://example.com/videos/trote-suave"},
        {"name": "Bicicleta Estática", "type": "cardio", "difficulty": "baja",
         "description": "Pedaleo suave en bicicleta estática", "duration": 25.0,
         "video_url": "https://example.com/videos/bicicleta-estatica"},
        
        # Cardio - Media
        {"name": "Correr 5K", "type": "cardio", "difficulty": "media",
         "description": "Correr 5 kilómetros a ritmo moderado", "duration": 30.0,
         "video_url": "https://example.com/videos/correr-5k"},
        {"name": "Burpees", "type": "cardio", "difficulty": "media",
         "description": "Ejercicio completo de cuerpo que combina sentadilla, flexión y salto", "duration": 15.0,
         "video_url": "https://example.com/videos/burpees"},
        {"name": "Saltar Cuerda", "type": "cardio", "difficulty": "media",
         "description": "Saltar la cuerda durante 20 minutos", "duration": 20.0,
         "video_url": "https://example.com/videos/saltar-cuerda"},
        {"name": "HIIT Básico", "type": "cardio", "difficulty": "media",
         "description": "Entrenamiento de intervalos de alta intensidad", "duration": 20.0,
         "video_url": "https://example.com/videos/hiit-basico"},
        
        # Cardio - Alta
        {"name": "Correr 10K", "type": "cardio", "difficulty": "alta",
         "description": "Correr 10 kilómetros a ritmo sostenido", "duration": 50.0,
         "video_url": "https://example.com/videos/correr-10k"},
        {"name": "Sprint Intervals", "type": "cardio", "difficulty": "alta",
         "description": "Series de sprints de alta intensidad", "duration": 25.0,
         "video_url": "https://example.com/videos/sprint-intervals"},
        
        # Fuerza - Baja
        {"name": "Sentadillas Básicas", "type": "fuerza", "difficulty": "baja",
         "description": "Sentadillas sin peso adicional", "duration": 10.0,
         "video_url": "https://example.com/videos/sentadillas-basicas"},
        {"name": "Flexiones de Rodillas", "type": "fuerza", "difficulty": "baja",
         "description": "Flexiones modificadas apoyando las rodillas", "duration": 8.0,
         "video_url": "https://example.com/videos/flexiones-rodillas"},
        {"name": "Plancha Básica", "type": "fuerza", "difficulty": "baja",
         "description": "Mantenerse en posición de plancha", "duration": 5.0,
         "video_url": "https://example.com/videos/plancha-basica"},
        
        # Fuerza - Media
        {"name": "Sentadillas con Peso", "type": "fuerza", "difficulty": "media",
         "description": "Sentadillas con barra o mancuernas", "duration": 15.0,
         "video_url": "https://example.com/videos/sentadillas-peso"},
        {"name": "Flexiones Estándar", "type": "fuerza", "difficulty": "media",
         "description": "Flexiones tradicionales", "duration": 12.0,
         "video_url": "https://example.com/videos/flexiones-estandar"},
        {"name": "Press de Banca", "type": "fuerza", "difficulty": "media",
         "description": "Press de banca con barra", "duration": 20.0,
         "video_url": "https://example.com/videos/press-banca"},
        {"name": "Peso Muerto", "type": "fuerza", "difficulty": "media",
         "description": "Peso muerto con barra", "duration": 18.0,
         "video_url": "https://example.com/videos/peso-muerto"},
        
        # Fuerza - Alta
        {"name": "Sentadillas Profundas con Peso", "type": "fuerza", "difficulty": "alta",
         "description": "Sentadillas profundas con peso adicional", "duration": 20.0,
         "video_url": "https://example.com/videos/sentadillas-profundas"},
        {"name": "Muscle-Ups", "type": "fuerza", "difficulty": "alta",
         "description": "Ejercicio avanzado de dominadas con transición", "duration": 15.0,
         "video_url": "https://example.com/videos/muscle-ups"},
        
        # Movilidad - Baja
        {"name": "Estiramiento Básico", "type": "movilidad", "difficulty": "baja",
         "description": "Rutina básica de estiramientos", "duration": 15.0,
         "video_url": "https://example.com/videos/estiramiento-basico"},
        {"name": "Yoga Suave", "type": "movilidad", "difficulty": "baja",
         "description": "Sesión de yoga para principiantes", "duration": 30.0,
         "video_url": "https://example.com/videos/yoga-suave"},
        
        # Movilidad - Media
        {"name": "Yoga Flow", "type": "movilidad", "difficulty": "media",
         "description": "Flujo de yoga de nivel intermedio", "duration": 45.0,
         "video_url": "https://example.com/videos/yoga-flow"},
        {"name": "Pilates", "type": "movilidad", "difficulty": "media",
         "description": "Sesión de pilates para fortalecimiento y flexibilidad", "duration": 40.0,
         "video_url": "https://example.com/videos/pilates"},
        {"name": "Movilidad de Cadera", "type": "movilidad", "difficulty": "media",
         "description": "Ejercicios específicos para mejorar movilidad de cadera", "duration": 20.0,
         "video_url": "https://example.com/videos/movilidad-cadera"},
        
        # Movilidad - Alta
        {"name": "Yoga Avanzado", "type": "movilidad", "difficulty": "alta",
         "description": "Sesión de yoga avanzada con posturas complejas", "duration": 60.0,
         "video_url": "https://example.com/videos/yoga-avanzado"},
        {"name": "Estiramiento Avanzado", "type": "movilidad", "difficulty": "alta",
         "description": "Rutina avanzada de estiramientos y flexibilidad", "duration": 30.0,
         "video_url": "https://example.com/videos/estiramiento-avanzado"},
    ]
    
    created_exercises = []
    for ex_data in exercises_data:
        exercise = Exercise(
            name=ex_data["name"],
            type=ex_data["type"],
            difficulty=ex_data["difficulty"],
            description=ex_data["description"],
            duration=ex_data["duration"],
            video_url=ex_data["video_url"],
            created_by="system"
        )
        exercise.save()
        exercise_id = str(exercise.id)
        created_exercises.append(exercise_id)
        print(f"✓ Created: {ex_data['name']} ({ex_data['type']}, {ex_data['difficulty']}) - ID: {exercise_id}")
    
    print(f"\nTotal exercises created: {len(created_exercises)}")
    return created_exercises


def create_template_routines(exercise_ids):
    """Create 8-10 pre-designed template routines"""
    print("\n" + "="*60)
    print("Creating Template Routines...")
    print("="*60)
    
    # Group exercises by type and difficulty
    cardio_baja = [eid for i, eid in enumerate(exercise_ids) if i < 3]
    cardio_media = [eid for i, eid in enumerate(exercise_ids) if 3 <= i < 7]
    fuerza_baja = [eid for i, eid in enumerate(exercise_ids) if 10 <= i < 13]
    fuerza_media = [eid for i, eid in enumerate(exercise_ids) if 13 <= i < 17]
    movilidad_baja = [eid for i, eid in enumerate(exercise_ids) if 18 <= i < 20]
    movilidad_media = [eid for i, eid in enumerate(exercise_ids) if 20 <= i < 23]
    
    routines_data = [
        {
            "name": "Rutina Cardio para Principiantes",
            "description": "Rutina de cardio suave para empezar",
            "exercises": [
                {"exercise_id": cardio_baja[0], "sets": 1, "duration": 30.0, "rest": 0},
                {"exercise_id": cardio_baja[1], "sets": 1, "duration": 20.0, "rest": 60},
            ],
        },
        {
            "name": "Rutina de Fuerza Básica",
            "description": "Rutina completa de fuerza para principiantes",
            "exercises": [
                {"exercise_id": fuerza_baja[0], "sets": 3, "reps": 12, "rest": 60},
                {"exercise_id": fuerza_baja[1], "sets": 3, "reps": 10, "rest": 60},
                {"exercise_id": fuerza_baja[2], "sets": 3, "duration": 30.0, "rest": 60},
            ],
        },
        {
            "name": "Rutina de Movilidad Matutina",
            "description": "Rutina de estiramientos y movilidad para empezar el día",
            "exercises": [
                {"exercise_id": movilidad_baja[0], "sets": 1, "duration": 15.0, "rest": 0},
                {"exercise_id": movilidad_baja[1], "sets": 1, "duration": 30.0, "rest": 0},
            ],
        },
        {
            "name": "Rutina Cardio Intensiva",
            "description": "Rutina de cardio de nivel intermedio",
            "exercises": [
                {"exercise_id": cardio_media[0], "sets": 1, "duration": 30.0, "rest": 120},
                {"exercise_id": cardio_media[1], "sets": 3, "reps": 10, "rest": 90},
                {"exercise_id": cardio_media[2], "sets": 1, "duration": 20.0, "rest": 60},
            ],
        },
        {
            "name": "Rutina de Fuerza Intermedia",
            "description": "Rutina completa de fuerza de nivel intermedio",
            "exercises": [
                {"exercise_id": fuerza_media[0], "sets": 4, "reps": 8, "rest": 90},
                {"exercise_id": fuerza_media[1], "sets": 3, "reps": 12, "rest": 90},
                {"exercise_id": fuerza_media[2], "sets": 3, "reps": 8, "rest": 120},
                {"exercise_id": fuerza_media[3], "sets": 3, "reps": 6, "rest": 120},
            ],
        },
        {
            "name": "Rutina Full Body",
            "description": "Rutina completa que combina cardio, fuerza y movilidad",
            "exercises": [
                {"exercise_id": cardio_media[0], "sets": 1, "duration": 20.0, "rest": 60},
                {"exercise_id": fuerza_media[0], "sets": 3, "reps": 10, "rest": 90},
                {"exercise_id": fuerza_media[1], "sets": 3, "reps": 12, "rest": 90},
                {"exercise_id": movilidad_media[0], "sets": 1, "duration": 15.0, "rest": 0},
            ],
        },
        {
            "name": "Rutina de Yoga Completa",
            "description": "Sesión completa de yoga para flexibilidad y relajación",
            "exercises": [
                {"exercise_id": movilidad_media[0], "sets": 1, "duration": 45.0, "rest": 0},
                {"exercise_id": movilidad_media[1], "sets": 1, "duration": 20.0, "rest": 0},
            ],
        },
        {
            "name": "Rutina HIIT",
            "description": "Entrenamiento de intervalos de alta intensidad",
            "exercises": [
                {"exercise_id": cardio_media[3], "sets": 1, "duration": 20.0, "rest": 60},
                {"exercise_id": fuerza_media[1], "sets": 3, "reps": 15, "rest": 60},
                {"exercise_id": cardio_media[1], "sets": 3, "reps": 12, "rest": 60},
            ],
        },
        {
            "name": "Rutina de Fuerza Avanzada",
            "description": "Rutina de fuerza para usuarios avanzados",
            "exercises": [
                {"exercise_id": fuerza_media[0], "sets": 5, "reps": 5, "rest": 180},
                {"exercise_id": fuerza_media[2], "sets": 4, "reps": 6, "rest": 180},
                {"exercise_id": fuerza_media[3], "sets": 3, "reps": 5, "rest": 180},
            ],
        },
        {
            "name": "Rutina de Recuperación",
            "description": "Rutina suave de movilidad para días de recuperación",
            "exercises": [
                {"exercise_id": movilidad_baja[0], "sets": 1, "duration": 20.0, "rest": 0},
                {"exercise_id": movilidad_media[2], "sets": 1, "duration": 20.0, "rest": 0},
            ],
        },
    ]
    
    created_routines = []
    for routine_data in routines_data:
        routine = Routine(
            name=routine_data["name"],
            description=routine_data["description"],
            exercises=routine_data["exercises"],
            created_by="system",
            is_template=True
        )
        routine.save()
        routine_id = str(routine.id)
        created_routines.append(routine_id)
        print(f"✓ Created template: {routine_data['name']} - ID: {routine_id}")
    
    print(f"\nTotal template routines created: {len(created_routines)}")
    return created_routines


def create_user_routines(template_routine_ids, exercise_ids):
    """Create 3-5 user-specific routines adopted from templates"""
    print("\n" + "="*60)
    print("Creating User-Specific Routines...")
    print("="*60)
    
    # Get some users (or use test user IDs)
    test_user_ids = ["student", "user1", "user2", "user3", "user4"]
    
    user_routines_data = [
        {
            "name": "Mi Rutina Personalizada",
            "description": "Rutina adaptada de template para usuario",
            "template_id": template_routine_ids[0],
            "user_id": test_user_ids[0],
            "exercises": [
                {"exercise_id": exercise_ids[0], "sets": 2, "duration": 25.0, "rest": 60},
                {"exercise_id": exercise_ids[10], "sets": 3, "reps": 15, "rest": 60},
            ],
        },
        {
            "name": "Rutina Adaptada Cardio",
            "description": "Versión personalizada de rutina cardio",
            "template_id": template_routine_ids[3],
            "user_id": test_user_ids[1],
            "exercises": [
                {"exercise_id": exercise_ids[3], "sets": 1, "duration": 25.0, "rest": 90},
                {"exercise_id": exercise_ids[4], "sets": 2, "reps": 8, "rest": 90},
            ],
        },
        {
            "name": "Mi Rutina de Fuerza",
            "description": "Rutina de fuerza personalizada",
            "template_id": template_routine_ids[1],
            "user_id": test_user_ids[2],
            "exercises": [
                {"exercise_id": exercise_ids[13], "sets": 3, "reps": 10, "rest": 90},
                {"exercise_id": exercise_ids[14], "sets": 3, "reps": 12, "rest": 90},
            ],
        },
        {
            "name": "Rutina Matutina Personal",
            "description": "Adaptación de rutina matutina",
            "template_id": template_routine_ids[2],
            "user_id": test_user_ids[0],
            "exercises": [
                {"exercise_id": exercise_ids[18], "sets": 1, "duration": 20.0, "rest": 0},
            ],
        },
        {
            "name": "Full Body Personalizado",
            "description": "Versión personalizada de rutina full body",
            "template_id": template_routine_ids[5],
            "user_id": test_user_ids[3],
            "exercises": [
                {"exercise_id": exercise_ids[3], "sets": 1, "duration": 15.0, "rest": 60},
                {"exercise_id": exercise_ids[13], "sets": 2, "reps": 10, "rest": 90},
                {"exercise_id": exercise_ids[20], "sets": 1, "duration": 10.0, "rest": 0},
            ],
        },
    ]
    
    created_user_routines = []
    for routine_data in user_routines_data:
        routine = Routine(
            name=routine_data["name"],
            description=routine_data["description"],
            exercises=routine_data["exercises"],
            created_by=routine_data["user_id"],
            is_template=False,
            adopted_from=routine_data["template_id"],
            user_id=routine_data["user_id"]
        )
        routine.save()
        routine_id = str(routine.id)
        created_user_routines.append(routine_id)
        print(f"✓ Created user routine: {routine_data['name']} (user: {routine_data['user_id']}) - ID: {routine_id}")
    
    print(f"\nTotal user routines created: {len(created_user_routines)}")
    return created_user_routines


def create_progress_entries(exercise_ids, routine_ids, user_routine_ids):
    """Create 20-30 progress entries"""
    print("\n" + "="*60)
    print("Creating Progress Entries...")
    print("="*60)
    
    test_user_ids = ["student", "user1", "user2", "user3", "user4"]
    all_routine_ids = routine_ids + user_routine_ids
    
    # Create progress entries over the last 30 days
    base_date = datetime.utcnow()
    created_progress = []
    
    for i in range(25):
        user_id = random.choice(test_user_ids)
        date = base_date - timedelta(days=random.randint(0, 30))
        
        # Mix of routine-based and exercise-based progress
        if random.random() > 0.4:  # 60% routine-based
            routine_id = random.choice(all_routine_ids)
            exercise_id = None
            # Get an exercise from the routine
            try:
                routine = Routine.objects.get(id=ObjectId(routine_id))
                if routine.exercises and len(routine.exercises) > 0:
                    exercise_id = routine.exercises[0].get("exercise_id")
            except:
                exercise_id = random.choice(exercise_ids)
        else:  # 40% exercise-based
            exercise_id = random.choice(exercise_ids)
            routine_id = None
        
        progress = Progress(
            user_id=user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
            date=date,
            repetitions=random.randint(5, 20) if exercise_id else None,
            duration=random.uniform(10.0, 60.0) if random.random() > 0.5 else None,
            effort_level=random.randint(4, 10),
            notes=random.choice([
                "Great workout!",
                "Felt strong today",
                "It was tough but I finished",
                "Really enjoyed this session",
                "Need to improve form",
                "Felt tired but pushed through",
                "Excellent progress",
                None,
                None,  # More None for variety
            ])
        )
        progress.save()
        progress_id = str(progress.id)
        created_progress.append(progress_id)
        print(f"✓ Created progress entry for user {user_id} - ID: {progress_id}")
    
    print(f"\nTotal progress entries created: {len(created_progress)}")
    return created_progress


def create_recommendations(progress_ids, routine_ids, user_routine_ids):
    """Create 10-15 trainer recommendations"""
    print("\n" + "="*60)
    print("Creating Recommendations...")
    print("="*60)
    
    trainer_ids = ["trainer1", "trainer2", "employee"]
    test_user_ids = ["student", "user1", "user2", "user3", "user4"]
    all_routine_ids = routine_ids + user_routine_ids
    
    messages = [
        "Great progress! Keep up the excellent work.",
        "I noticed you're improving. Try increasing the weight slightly next time.",
        "Your form is getting better. Focus on maintaining consistency.",
        "Consider adding more rest time between sets for better recovery.",
        "Excellent effort level! You're ready to move to the next difficulty.",
        "Try to focus on breathing during the exercise for better performance.",
        "I recommend increasing repetitions gradually over the next week.",
        "Your progress is steady. Keep maintaining this pace.",
        "Consider trying a different exercise variation to avoid plateau.",
        "Great job completing the routine! Try to maintain this frequency.",
        "I suggest adding more cardio to your routine for better results.",
        "Your consistency is paying off. Keep it up!",
        "Try to focus on the negative part of the movement for better gains.",
        "Excellent work! You're ready for more challenging exercises.",
        "I recommend tracking your progress more consistently.",
    ]
    
    created_recommendations = []
    for i in range(12):
        trainer_id = random.choice(trainer_ids)
        user_id = random.choice(test_user_ids)
        
        # Link to progress or routine
        related_progress_id = random.choice(progress_ids) if random.random() > 0.3 else None
        related_routine_id = random.choice(all_routine_ids) if random.random() > 0.5 else None
        
        recommendation = Recommendation(
            trainer_id=trainer_id,
            user_id=user_id,
            message=random.choice(messages),
            related_progress_id=related_progress_id,
            related_routine_id=related_routine_id
        )
        recommendation.save()
        recommendation_id = str(recommendation.id)
        created_recommendations.append(recommendation_id)
        print(f"✓ Created recommendation from {trainer_id} to {user_id} - ID: {recommendation_id}")
    
    print(f"\nTotal recommendations created: {len(created_recommendations)}")
    return created_recommendations


def create_followups(progress_ids):
    """Create 5-8 follow-up comments from trainers"""
    print("\n" + "="*60)
    print("Creating Follow-ups...")
    print("="*60)
    
    trainer_ids = ["trainer1", "trainer2", "employee"]
    test_user_ids = ["student", "user1", "user2", "user3", "user4"]
    
    comments = [
        "Keep focusing on form, you're doing great!",
        "I see improvement in your consistency. Well done!",
        "Try to increase the intensity slightly next session.",
        "Your recovery time is good. Keep maintaining this pace.",
        "Excellent progress! You're on the right track.",
        "Consider adding more variety to avoid boredom.",
        "Your effort level is consistent. Great job!",
        "I noticed you're pushing yourself. Keep it up!",
    ]
    
    created_followups = []
    for i in range(6):
        trainer_id = random.choice(trainer_ids)
        user_id = random.choice(test_user_ids)
        progress_id = random.choice(progress_ids)
        
        followup = FollowUp(
            trainer_id=trainer_id,
            user_id=user_id,
            progress_id=progress_id,
            comment=random.choice(comments)
        )
        followup.save()
        followup_id = str(followup.id)
        created_followups.append(followup_id)
        print(f"✓ Created follow-up from {trainer_id} to {user_id} - ID: {followup_id}")
    
    print(f"\nTotal follow-ups created: {len(created_followups)}")
    return created_followups


def main():
    """Main function to create all test data"""
    print("\n" + "="*60)
    print("CREATING COMPREHENSIVE TEST DATA FOR MONGODB")
    print("="*60)
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("\nClearing existing MongoDB data...")
    Exercise.objects.all().delete()
    Routine.objects.all().delete()
    Progress.objects.all().delete()
    Recommendation.objects.all().delete()
    FollowUp.objects.all().delete()
    print("✓ Cleared existing data")
    
    # Create all data
    exercise_ids = create_exercises()
    template_routine_ids = create_template_routines(exercise_ids)
    user_routine_ids = create_user_routines(template_routine_ids, exercise_ids)
    all_routine_ids = template_routine_ids + user_routine_ids
    progress_ids = create_progress_entries(exercise_ids, template_routine_ids, user_routine_ids)
    recommendation_ids = create_recommendations(progress_ids, template_routine_ids, user_routine_ids)
    followup_ids = create_followups(progress_ids)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Exercises created: {len(exercise_ids)}")
    print(f"Template routines created: {len(template_routine_ids)}")
    print(f"User routines created: {len(user_routine_ids)}")
    print(f"Progress entries created: {len(progress_ids)}")
    print(f"Recommendations created: {len(recommendation_ids)}")
    print(f"Follow-ups created: {len(followup_ids)}")
    print("\n" + "="*60)
    print("✓ All test data created successfully!")
    print("="*60)
    
    # Return IDs for validation
    return {
        "exercises": exercise_ids,
        "template_routines": template_routine_ids,
        "user_routines": user_routine_ids,
        "progress": progress_ids,
        "recommendations": recommendation_ids,
        "followups": followup_ids,
    }


if __name__ == "__main__":
    main()

