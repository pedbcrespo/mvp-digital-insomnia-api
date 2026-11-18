from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from config.const_config import BASE_URL
from config.db_config import init_db
from controller.sleep_prediction_controller import (
    service as sleep_prediction_service,
    sleep_prediction_ns,
)


def create_app(config_override=None):
    app = Flask(__name__)
    if config_override:
        app.config.update(config_override)

    CORS(app)
    # init_db(app)

    model_available = sleep_prediction_service.ensure_model_available()
    app.extensions["sleep_prediction_service"] = sleep_prediction_service
    app.extensions["sleep_model_available"] = model_available

    api = Api(
        app,
        title="Digital Insomnia API",
        version="1.0",
        description="API de classificação de dívida de sono",
        doc=f"/{BASE_URL}/docs",
    )
    api.add_namespace(sleep_prediction_ns, path=f"/{BASE_URL}")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
