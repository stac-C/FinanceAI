from django import forms


class PredictionForm(forms.Form):
    revenus = forms.FloatField(label="Revenus (k€)", min_value=0, initial=60.0)
    ccavg = forms.FloatField(
        label="Dépenses mensuelles CCAvg", min_value=0.0, initial=1.0
    )
    education = forms.ChoiceField(
        label="Niveau d'éducation",
        choices=[
            (1, "Undergrad"),
            (2, "Graduate"),
            (3, "Advance/Professional"),
            (4, "Doctorate"),
        ],
        initial=2,
    )
    famille = forms.ChoiceField(
        label="Taille de la famille",
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4+")],
        initial=1,
    )
    pret_immobilier = forms.TypedChoiceField(
        label="Possède un prêt immobilier ?",
        choices=[(0, "Non"), (1, "Oui")],
        coerce=int,
        widget=forms.RadioSelect,
        initial=0,
    )
    compte_cd = forms.TypedChoiceField(
        label="Compte à terme (CD) ?",
        choices=[(0, "Non"), (1, "Oui")],
        coerce=int,
        widget=forms.RadioSelect,
        initial=0,
    )

    compte_de_titres = forms.TypedChoiceField(
        label="Compte de titres ?",
        choices=[(0, "Non"), (1, "Oui")],
        coerce=int,
        widget=forms.RadioSelect,
        initial=0,
    )
    age = forms.IntegerField(label="Age", min_value=18, max_value=100, initial=30)
    experience = forms.IntegerField(
        label="Expérience (années)", min_value=0, max_value=50, initial=5
    )
    en_ligne = forms.TypedChoiceField(
        label="Utilise les services en ligne ?",
        choices=[(0, "Non"), (1, "Oui")],
        coerce=int,
        widget=forms.RadioSelect,
        initial=1,
    )
    carte_de_credit = forms.TypedChoiceField(
        label="Possède une carte de crédit ?",
        choices=[(0, "Non"), (1, "Oui")],
        coerce=int,
        widget=forms.RadioSelect,
        initial=1,
    )
