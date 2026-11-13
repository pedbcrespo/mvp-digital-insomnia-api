from dataclasses import asdict
from pathlib import Path

import joblib
import pandas as pd

from model.request.sleep_request import SleepRequest


class SleepPredictionService:
    """Carrega o pipeline treinado e classifica uma solicitação de sono."""

    DEFAULT_MODEL_PATH = (
        Path(__file__).resolve().parents[1]
        / "artifacts"
        / "sleep_debt_pipeline.joblib"
    )

    def __init__(self, model_path: str | Path | None = None):
        self.model_path = Path(model_path) if model_path else self.DEFAULT_MODEL_PATH
        self._model = None

    def _load_model(self):
        if self._model is None:
            if not self.model_path.is_file():
                raise FileNotFoundError(
                    f"Modelo treinado não encontrado em '{self.model_path}'. "
                    "Coloque o arquivo sleep_debt_pipeline.joblib na pasta artifacts."
                )
            self._model = joblib.load(self.model_path)
        return self._model

    def predict(self, sleep_request: SleepRequest) -> str:
        """Retorna a classe prevista para os dados recebidos."""
        if not isinstance(sleep_request, SleepRequest):
            raise TypeError("sleep_request deve ser uma instância de SleepRequest")

        # Mantém os nomes das colunas usados no treinamento do pipeline no Colab.
        input_data = pd.DataFrame([asdict(sleep_request)])
        prediction = self._load_model().predict(input_data)[0]
        return str(prediction)
