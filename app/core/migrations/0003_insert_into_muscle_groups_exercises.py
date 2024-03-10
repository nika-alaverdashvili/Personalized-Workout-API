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
        # Add more muscle group data
    ]

    muscle_groups = {mg_data['name']: MuscleGroup.objects.get_or_create(**mg_data)[0] for mg_data in muscle_groups_data}

    # Defining exercises
    exercises_data = [
        {"name": "Bench Press", "description": "Chest exercise", "instructions": "Lay on bench, press barbell from chest", "target_muscles": ["Chest"]},
        {"name": "Deadlift", "description": "Back and leg exercise", "instructions": "Lift barbell from ground to hip level", "target_muscles": ["Back"]},
        {"name": "Shoulder Press", "description": "Shoulder exercise", "instructions": "Press dumbbells from shoulders overhead", "target_muscles": ["Shoulders"]},
        # Add more exercise data
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
