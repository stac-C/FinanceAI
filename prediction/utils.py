import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"
MODEL_FILE = MODEL_DIR / "model.pkl"
PREPROCESS_FILE = MODEL_DIR / "preprocess.pkl"
METADATA_FILE = MODEL_DIR / "metadata.pkl"

FEATURE_ORDER = [
    "Age",
    "Expérience",
    "Revenus",
    "Famille",
    "CCAvg",
    "Education",
    "Pret Immobilier",
    "Compte de titres",
    "Compte CD",
    "En ligne",
    "Carte de credit",
]


def load_artifacts():
    model = None
    preprocess = None
    try:
        model = joblib.load(MODEL_FILE)
        preprocess = joblib.load(PREPROCESS_FILE)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Les fichiers model.pkl et preprocess.pkl doivent être créés avec train_model.py."
        )
    return model, preprocess, FEATURE_ORDER


def load_metadata():
    try:
        return joblib.load(METADATA_FILE)
    except FileNotFoundError:
        return {}


def make_prediction(input_data, model, preprocess):
    if len(input_data) != len(FEATURE_ORDER):
        raise ValueError("Le nombre de caractéristiques est incorrect.")

    X = [input_data]
    X_processed = preprocess.transform(X)
    prediction = int(model.predict(X_processed)[0])
    probability = float(model.predict_proba(X_processed)[0][1])
    return prediction, probability
