# fitness/forms.py
from django import forms

class ExerciseForm(forms.Form):
    name = forms.CharField(max_length=100)
    type = forms.ChoiceField(choices=[
        ('cardio', 'Cardio'),
        ('fuerza', 'Fuerza'),
        ('movilidad', 'Movilidad'),
    ])
    description = forms.CharField(required=False, widget=forms.Textarea)
    duration = forms.FloatField(required=False)
    difficulty = forms.ChoiceField(required=False, choices=[
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ])
    video_url = forms.URLField(required=False)

# fitness/forms.py
from django import forms

class RoutineForm(forms.Form):
    name = forms.CharField(max_length=120, required=True, label="Nombre",)

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}), label="Descripción",)

    # Este campo no se usará directamente: lo reconstruimos en clean_exercises()
    exercises = forms.CharField(required=False,widget=forms.HiddenInput(),)

    is_template = forms.BooleanField(required=False, initial=False, label="¿Es plantilla?",)

    def clean_exercises(self):
        """
        Reconstruye la lista de ejercicios enviada desde inputs como:
        exercises[1][exercise_id]
        exercises[1][sets]
        exercises[1][reps]
        exercises[1][rest]
        """

        raw = self.data  # request.POST original
        prefix = "exercises["

        parsed = {}  # {"1": {"exercise_id": "...", "sets": "..."}}

        for key in raw:
            if key.startswith(prefix):
                # "exercises[3][reps]" -> row="3", field="reps"
                row = key.split("[")[1].split("]")[0]
                field = key.split("[")[2].split("]")[0]

                if row not in parsed:
                    parsed[row] = {}

                parsed[row][field] = raw.get(key)

        result = []

        for row_id, fields in parsed.items():
            exercise_id = fields.get("exercise_id")

            if not exercise_id:
                continue  # ignorar filas vacías

            entry = {
                "exercise_id": exercise_id,
                "sets": int(fields["sets"]) if fields.get("sets") else None,
                "reps": int(fields["reps"]) if fields.get("reps") else None,
                "rest": int(fields["rest"]) if fields.get("rest") else None,
            }

            result.append(entry)

        if not result:
            raise forms.ValidationError(
                "Debe agregar al menos un ejercicio a la rutina."
            )

        return result
