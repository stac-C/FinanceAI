import joblib
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def main():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "Bank_Personal_Loan_Modelling.xlsx"
    model_dir = base_dir / "model"
    static_dir = base_dir / "prediction" / "static" / "prediction"
    static_dir.mkdir(exist_ok=True, parents=True)
    model_dir.mkdir(exist_ok=True)

    df = pd.read_excel(data_path)
    feature_columns = [
        "Age",  # "Age" indique l'âge du client en années
        "Expérience",  # "Expérience" indique l'expérience professionnelle du client en années
        "Revenus",  # "Revenus" indique les revenus annuels du client en milliers d'euros
        "Famille",  # "Famille" indique la taille de la famille du client (1, 2, 3, 4+)
        "CCAvg",  # CCAvg est une abréviation pour "Credit Card Average" (Dépenses mensuelles moyennes sur carte de crédit)
        "Education",  # "Education" indique le niveau d'éducation du client (1: Undergrad, 2: Graduate, 3: Advance/Professional, 4: Doctorate)
        "Pret Immobilier",  # "Pret Immobilier" indique si le client possède un prêt immobilier
        "Compte de titres",  # "Compte de titres" indique si le client possède un compte de titres (investissement)
        "Compte CD",  # CD est une abréviation pour "Certificate of Deposit" (Compte à terme)
        "En ligne",  # "En ligne" indique si le client utilise les services bancaires en ligne
        "Carte de credit",  # "Carte de credit" indique si le client possède une carte de crédit
    ]
    X = df[feature_columns]
    y = df["Prêt Personnel"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    default_rate = float((y == 1).mean())
    confusion = confusion_matrix(y_test, y_pred).tolist()
    target_counts = y.value_counts().to_dict()
    target_rates = y.value_counts(normalize=True).mul(100).round(2).to_dict()
    class_report = classification_report(y_test, y_pred, output_dict=True)

    # Générer les graphiques interactifs avec Plotly
    confusion_html = generate_confusion_matrix_plotly(confusion)
    feature_html = generate_feature_importance_plotly(
        feature_columns, model.feature_importances_
    )
    target_dist_html = generate_target_distribution_plotly(target_counts, target_rates)

    metadata = {
        "feature_names": feature_columns,
        "feature_importances": model.feature_importances_.tolist(),
        "accuracy": float(accuracy),
        "default_rate": default_rate,
        "model_type": "RandomForest",
        "confusion_matrix": confusion,
        "target_counts": target_counts,
        "target_rates": target_rates,
        "classification_report": class_report,
        "confusion_plot_html": confusion_html,
        "feature_plot_html": feature_html,
        "target_dist_plot_html": target_dist_html,
    }

    joblib.dump(model, model_dir / "model.pkl")
    joblib.dump(scaler, model_dir / "preprocess.pkl")
    joblib.dump(metadata, model_dir / "metadata.pkl")

    print("Modèle entraîné et exporté dans le dossier model/")
    print(f"Accuracy test: {accuracy:.4f}")
    print(f"Taux de défaut global: {default_rate:.4f}")


def generate_confusion_matrix_plotly(confusion_matrix):
    """Génère un graphique de matrice de confusion interactif avec Plotly"""
    fig = go.Figure(
        data=go.Heatmap(
            z=confusion_matrix,
            x=["Prédit 0", "Prédit 1"],
            y=["Réel 0", "Réel 1"],
            colorscale="Blues",
            text=confusion_matrix,
            texttemplate="%{text}",
            textfont={"size": 16},
            hoverongaps=False,
        )
    )

    fig.update_layout(
        title="Matrice de Confusion - Random Forest",
        xaxis_title="Valeurs Prédites",
        yaxis_title="Valeurs Réelles",
        width=600,
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )

    # Configuration du thème sombre
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)")

    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")


def generate_feature_importance_plotly(feature_names, importances):
    """Génère un graphique d'importance des variables avec Plotly"""
    # Trier par importance
    sorted_idx = importances.argsort()
    sorted_features = [feature_names[i] for i in sorted_idx]
    sorted_importances = importances[sorted_idx]

    fig = go.Figure(
        data=[
            go.Bar(
                x=sorted_importances,
                y=sorted_features,
                orientation="h",
                marker_color="rgba(61, 111, 255, 0.7)",
                marker_line_color="rgba(61, 111, 255, 1)",
                marker_line_width=1,
            )
        ]
    )

    fig.update_layout(
        title="Importance des Variables - Random Forest",
        xaxis_title="Importance",
        yaxis_title="Variables",
        width=700,
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )

    fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)")

    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")


def generate_target_distribution_plotly(target_counts, target_rates):
    """Génère un graphique de distribution de la cible avec Plotly"""
    labels = ["Client Fiable (0)", "Client à Risque (1)"]
    values = [target_counts.get(0, 0), target_counts.get(1, 0)]
    percentages = [target_rates.get(0, 0), target_rates.get(1, 0)]

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "xy"}]])

    # Pie chart
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            name="Distribution",
            marker_colors=["#4CAF50", "#F44336"],
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>",
        ),
        1,
        1,
    )

    # Bar chart
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            name="Nombre",
            marker_color=["#4CAF50", "#F44336"],
            text=values,
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
        ),
        1,
        2,
    )

    fig.update_layout(
        title_text="Distribution de la Variable Cible",
        width=800,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )

    fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)", row=1, col=2)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)", row=1, col=2)

    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")


def generate_confusion_matrix_plot(confusion_matrix, static_dir):
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        confusion_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Prédit 0", "Prédit 1"],
        yticklabels=["Réel 0", "Réel 1"],
    )
    plt.title("Matrice de Confusion - Random Forest")
    plt.ylabel("Valeurs Réelles")
    plt.xlabel("Valeurs Prédites")
    plt.tight_layout()
    plt.savefig(static_dir / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()


def generate_feature_importance_plot(feature_names, importances, static_dir):
    plt.figure(figsize=(10, 6))
    sorted_idx = importances.argsort()
    plt.barh(range(len(sorted_idx)), importances[sorted_idx], align="center")
    plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
    plt.xlabel("Importance")
    plt.title("Importance des Variables - Random Forest")
    plt.tight_layout()
    plt.savefig(static_dir / "feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
