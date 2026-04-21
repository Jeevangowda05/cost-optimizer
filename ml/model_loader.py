from functools import lru_cache
from pathlib import Path
import pickle

from django.conf import settings

try:
    import joblib
except ImportError:  # pragma: no cover - fallback path
    joblib = None


def get_model_path(kind):
    if kind == 'prediction':
        return Path(settings.ML_MODEL_PATH)
    if kind == 'anomaly':
        return Path(settings.ANOMALY_MODEL_PATH)
    raise ValueError('Unsupported model kind.')


@lru_cache(maxsize=2)
def load_model(kind):
    model_path = get_model_path(kind)
    if not model_path.exists():
        raise FileNotFoundError(f'Model file not found: {model_path}')

    if joblib is not None:
        return joblib.load(model_path)

    with model_path.open('rb') as model_file:
        return pickle.load(model_file)
