import controller.sleep_prediction_controller as prediction_controller
import app as app_module
from model.request.sleep_request import SleepRequest


def test_predict_endpoint_passes_sleep_request_to_service(monkeypatch):
    payload = {
        "age": 28,
        "gender": "Female",
        "chronotype": "Night Owl",
        "occupation": "Professional",
        "bedtime_hour": 23.5,
        "screen_time_before_bed_min": 90,
        "primary_app_category": "Social Media",
        "screen_brightness_pct": 65,
        "blue_light_filter_on": True,
        "caffeine_intake_mg": 120,
        "caffeine_last_hour": 16.0,
        "physical_activity_min": 30,
        "room_temperature_f": 69.5,
        "ambient_noise_db": 32.0,
    }
    received = {}

    def fake_predict(sleep_request):
        received["sleep_request"] = sleep_request
        return "Mild"

    monkeypatch.setattr(prediction_controller.service, "predict", fake_predict)
    monkeypatch.setattr(app_module, "init_db", lambda app: None)

    app = app_module.create_app({"TESTING": True})
    response = app.test_client().post("/digital-insomnia/predict", json=payload)

    assert response.status_code == 200
    assert response.get_json() == {"prediction": "Mild"}
    assert isinstance(received["sleep_request"], SleepRequest)
    assert received["sleep_request"] == SleepRequest.from_dict(payload)
