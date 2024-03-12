from django.db import migrations


def add_muscle_group_exercise_data(apps, schema_editor):
    MuscleGroup = apps.get_model('core', 'MuscleGroup')
    Exercise = apps.get_model('core', 'Exercise')

    # Defining muscle groups
    muscle_groups_data = [
        {"name": "Chest", "description": "All chest muscles"},
        {"name": "Back", "description": "All back muscles"},
        {"name": "Shoulders", "description": "All shoulder muscles"},
        {"name": "Biceps", "description": "Front part of the upper arm"},
        {"name": "Legs", "description": "Includes thigh and calf muscles"},
        {"name": "Core", "description": "Abdominal and lower back muscles"},
        {"name": "Glutes", "description": "Buttock muscles"},
        {"name": "Forearms", "description": "Lower arm muscles"},
        {"name": "Traps", "description": "Upper back muscles"},
        {"name": "Lats", "description": "Lower back muscles"},

    ]

    muscle_groups = {mg_data['name']: MuscleGroup.objects.get_or_create(**mg_data)[0] for mg_data in muscle_groups_data}

    # Defining exercises
    exercises_data = [
        {"name": "Flat Bench Press", "description": "Chest exercise",
         "instructions": "Lay on bench, press barbell from chest", "target_muscles": ["Chest"]},
        {"name": "Incline Bench Press", "description": "Upper chest exercise",
         "instructions": "Lay on an incline bench, press barbell upwards", "target_muscles": ["Chest"]},
        {"name": "Deadlift", "description": "Back exercise", "instructions": "Lift barbell from ground to hip level",
         "target_muscles": ["Back"]},
        {"name": "Bent Over Row", "description": "Back exercise",
         "instructions": "Bend over, row barbell towards your stomach", "target_muscles": ["Back"]},
        {"name": "Military Press", "description": "Shoulder exercise",
         "instructions": "Press barbell from shoulders overhead", "target_muscles": ["Shoulders"]},
        {"name": "Lateral Raise", "description": "Shoulder exercise",
         "instructions": "Lift dumbbells out to sides to shoulder height", "target_muscles": ["Shoulders"]},
        {"name": "Barbell Curl", "description": "Bicep exercise", "instructions": "Curl barbell towards your chest",
         "target_muscles": ["Biceps"]},
        {"name": "Hammer Curl", "description": "Bicep exercise",
         "instructions": "Curl dumbbells with palms facing each other", "target_muscles": ["Biceps"]},
        {"name": "Squats", "description": "Leg exercise",
         "instructions": "Lower body until thighs are parallel to the floor", "target_muscles": ["Legs"]},
        {"name": "Lunges", "description": "Leg exercise",
         "instructions": "Step forward and lower until both knees are bent", "target_muscles": ["Legs"]},
        {"name": "Plank", "description": "Core exercise",
         "instructions": "Hold a pushup position with your body straight", "target_muscles": ["Core"]},
        {"name": "Russian Twist", "description": "Core exercise",
         "instructions": "Sit on the floor, lean back, twist side to side", "target_muscles": ["Core"]},
        {"name": "Glute Bridge", "description": "Glute exercise",
         "instructions": "Lay on back, lift hips towards the ceiling", "target_muscles": ["Glutes"]},
        {"name": "Hip Thrust", "description": "Glute exercise",
         "instructions": "Rest upper back on bench, thrust hips upwards", "target_muscles": ["Glutes"]},
        {"name": "Wrist Curl", "description": "Forearm exercise",
         "instructions": "Curl wrist upwards holding a dumbbell", "target_muscles": ["Forearms"]},
        {"name": "Reverse Wrist Curl", "description": "Forearm exercise",
         "instructions": "Curl wrist downwards holding a dumbbell", "target_muscles": ["Forearms"]},
        {"name": "Shrugs", "description": "Trap exercise", "instructions": "Lift shoulders up towards your ears",
         "target_muscles": ["Traps"]},
        {"name": "Upright Row", "description": "Trap and shoulder exercise",
         "instructions": "Lift barbell straight up to chin", "target_muscles": ["Traps", "Shoulders"]},
        {"name": "Pull-up", "description": "Lat exercise", "instructions": "Hang from bar and pull body up",
         "target_muscles": ["Lats"]},
        {"name": "Lat Pulldown", "description": "Lat exercise", "instructions": "Pull down bar towards chest",
         "target_muscles": ["Lats"]},
    ]

    for ex_data in exercises_data:
        target_muscles_names = ex_data.pop('target_muscles', [])
        exercise, created = Exercise.objects.get_or_create(**ex_data)
        exercise.target_muscles.set([muscle_groups[name] for name in target_muscles_names])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_musclegroup_exercise'),
    ]

    operations = [
        migrations.RunPython(add_muscle_group_exercise_data),
    ]
