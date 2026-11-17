from dataclasses import dataclass


@dataclass
class SleepRequest:
    """Dados de entrada esperados pelo modelo de classificação do sono."""

    age: int
    gender: str
    chronotype: str
    occupation: str
    bedtime_hour: float
    screen_time_before_bed_min: int
    primary_app_category: str
    screen_brightness_pct: int
    blue_light_filter_on: bool
    caffeine_intake_mg: int
    caffeine_last_hour: float
    physical_activity_min: int
    room_temperature_f: float
    ambient_noise_db: float

    @staticmethod
    def from_dict(data: dict) -> 'SleepRequest':
        return SleepRequest(
            age=data['age'],
            gender=data['gender'],
            chronotype=data['chronotype'],
            occupation=data['occupation'],
            bedtime_hour=data['bedtime_hour'],
            screen_time_before_bed_min=data['screen_time_before_bed_min'],
            primary_app_category=data['primary_app_category'],
            screen_brightness_pct=data['screen_brightness_pct'],
            blue_light_filter_on=data['blue_light_filter_on'],
            caffeine_intake_mg=data['caffeine_intake_mg'],
            caffeine_last_hour=data['caffeine_last_hour'],
            physical_activity_min=data['physical_activity_min'],
            room_temperature_f=data['room_temperature_f'],
            ambient_noise_db=data['ambient_noise_db'],
        )


    @staticmethod
    def is_valid(data: dict) -> bool:
        """Valida se os dados fornecidos contêm todos os campos necessários."""
        required_fields = {
            "age",
            "gender",
            "chronotype",
            "occupation",
            "bedtime_hour",
            "screen_time_before_bed_min",
            "primary_app_category",
            "screen_brightness_pct",
            "blue_light_filter_on",
            "caffeine_intake_mg",
            "caffeine_last_hour",
            "physical_activity_min",
            "room_temperature_f",
            "ambient_noise_db",
        }
        return required_fields.issubset(data.keys())