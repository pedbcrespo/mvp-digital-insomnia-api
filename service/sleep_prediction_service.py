from dataclasses import asdict
from hashlib import sha256
import hmac
import logging
import os
from pathlib import Path
import shutil
import tempfile
from urllib.error import URLError
from urllib.request import urlopen

import joblib
import pandas as pd

from model.request.sleep_request import SleepRequest


logger = logging.getLogger(__name__)


class SleepPredictionService:
    """Carrega o pipeline treinado e classifica uma solicitação de sono."""

    DEFAULT_MODEL_PATH = (
        Path(__file__).resolve().parents[1]
        / "artifacts"
        / "sleep_debt_pipeline.joblib"
    )

    def __init__(
        self,
        model_path: str | Path | None = None,
        model_url: str | None = None,
        expected_sha256: str | None = None,
    ):
        self.model_path = Path(model_path) if model_path else self.DEFAULT_MODEL_PATH
        self.model_url = model_url if model_url is not None else os.getenv("SLEEP_MODEL_URL")
        self.expected_sha256 = (
            expected_sha256
            if expected_sha256 is not None
            else os.getenv("SLEEP_MODEL_SHA256")
        )
        self._model = None

    def ensure_model_available(self) -> bool:
        """Garante o arquivo local; baixa-o quando ausente e há URL configurada."""
        if self.model_path.is_file():
            return True

        self.model_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.model_url:
            logger.warning(
                "Modelo ausente em '%s'. Defina SLEEP_MODEL_URL ou coloque o "
                "arquivo sleep_debt_pipeline.joblib em artifacts/.",
                self.model_path,
            )
            return False

        if not self.model_url.startswith("https://"):
            raise ValueError("SLEEP_MODEL_URL deve usar HTTPS.")

        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix="sleep-debt-",
                suffix=".download",
                dir=self.model_path.parent,
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                with urlopen(self.model_url, timeout=60) as response:
                    shutil.copyfileobj(response, temporary_file)

            if temporary_path.stat().st_size == 0:
                raise ValueError("O arquivo baixado está vazio.")

            if self.expected_sha256:
                digest = sha256(temporary_path.read_bytes()).hexdigest()
                if not hmac.compare_digest(
                    digest.lower(), self.expected_sha256.strip().lower()
                ):
                    raise ValueError("O SHA-256 do modelo baixado não corresponde.")

            os.replace(temporary_path, self.model_path)
            logger.info("Modelo baixado para '%s'.", self.model_path)
            return True
        except (OSError, URLError, ValueError) as error:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise RuntimeError(
                f"Não foi possível obter o modelo de SLEEP_MODEL_URL: {error}"
            ) from error

    def _load_model(self):
        if self._model is None:
            if not self.model_path.is_file():
                self.ensure_model_available()
            if not self.model_path.is_file():
                raise FileNotFoundError(
                    f"Modelo treinado não encontrado em '{self.model_path}'. "
                    "Configure SLEEP_MODEL_URL ou coloque o arquivo na pasta artifacts."
                )
            self._model = joblib.load(self.model_path)
        return self._model

    def predict(self, sleep_request: SleepRequest) -> str:
        """Retorna a classe prevista para os dados recebidos."""
        if not isinstance(sleep_request, SleepRequest):
            raise TypeError("sleep_request deve ser uma instância de SleepRequest")

        input_data = pd.DataFrame([asdict(sleep_request)])
        prediction = self._load_model().predict(input_data)[0]
        return str(prediction)
