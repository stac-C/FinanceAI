from django.shortcuts import render
from .forms import PredictionForm
from .utils import FEATURE_ORDER, load_artifacts, make_prediction, load_metadata


def home(request):
    metadata = load_metadata()
    accuracy = metadata.get("accuracy")
    default_rate = metadata.get("default_rate")
    top_features = metadata.get("feature_names", [])[:5]

    context = {
        "accuracy": accuracy * 100 if accuracy is not None else None,
        "default_rate": default_rate * 100 if default_rate is not None else None,
        "top_features": top_features,
    }
    return render(request, "prediction/home.html", context)


def predict(request):
    form = PredictionForm(request.POST or None)
    result = None
    probability = None
    risk_label = None
    model = None
    preprocess = None
    metadata = load_metadata()
    feature_importances = metadata.get("feature_importances", [])
    feature_names = metadata.get("feature_names", FEATURE_ORDER)
    feature_importance_pairs = list(zip(feature_names, feature_importances))

    if request.method == "POST" and form.is_valid():
        model, preprocess, _ = load_artifacts()
        input_data = [
            form.cleaned_data["revenus"],
            form.cleaned_data["ccavg"],
            form.cleaned_data["experience"],
            form.cleaned_data["education"],
            form.cleaned_data["famille"],
            form.cleaned_data["pret_immobilier"],
            form.cleaned_data["compte_cd"],
            form.cleaned_data["compte_de_titres"],
            form.cleaned_data["age"],
            form.cleaned_data["en_ligne"],
            form.cleaned_data["carte_de_credit"],
        ]

        result, probability = make_prediction(input_data, model, preprocess)
        probability = probability * 100
        risk_label = "Client à risque" if result == 1 else "Client fiable"

    context = {
        "form": form,
        "prediction": result,
        "probability": probability,
        "risk_label": risk_label,
        "feature_names": feature_names,
        "feature_importances": feature_importances,
        "feature_importance_pairs": feature_importance_pairs,
        "accuracy": metadata.get("accuracy"),
        "default_rate": metadata.get("default_rate"),
    }

    return render(request, "prediction/prediction.html", context)


def dashboard(request):
    metadata = load_metadata()
    feature_names = metadata.get("feature_names", [])
    feature_importances = metadata.get("feature_importances", [])
    feature_importance_pairs = list(zip(feature_names, feature_importances))
    confusion_matrix = metadata.get("confusion_matrix", [[0, 0], [0, 0]])
    target_counts = metadata.get("target_counts", {})
    target_rates = metadata.get("target_rates", {})
    classification_report = metadata.get("classification_report", {})
    confusion_plot_html = metadata.get("confusion_plot_html", "")
    feature_plot_html = metadata.get("feature_plot_html", "")
    target_dist_plot_html = metadata.get("target_dist_plot_html", "")

    accuracy = metadata.get("accuracy")
    default_rate = metadata.get("default_rate")
    context = {
        "accuracy": accuracy * 100 if accuracy is not None else None,
        "default_rate": default_rate * 100 if default_rate is not None else None,
        "feature_names": feature_names,
        "feature_importances": feature_importances,
        "feature_importance_pairs": feature_importance_pairs,
        "model_type": metadata.get("model_type", "RandomForest"),
        "confusion_matrix": confusion_matrix,
        "target_counts": target_counts,
        "target_rates": target_rates,
        "classification_report": classification_report,
        "confusion_plot_html": confusion_plot_html,
        "feature_plot_html": feature_plot_html,
        "target_dist_plot_html": target_dist_plot_html,
    }
    return render(request, "prediction/dashboard.html", context)
