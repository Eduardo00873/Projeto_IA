from django import forms

ALGORITMOS = [
    ('aprofundamento', 'Aprofundamento Progressivo'),
    ('custo_uniforme', 'Custo Uniforme'),
    ('a_estrela', 'A* (A Estrela)'),
    ('sofrega', 'Procura Sôfrega'),
]

CIDADES = [
    ('Aveiro', 'Aveiro'),
    ('Braga', 'Braga'),
    ('Bragança', 'Bragança'),
    ('Beja', 'Beja'),
    ('Castelo Branco', 'Castelo Branco'),
    ('Coimbra', 'Coimbra'),
    ('Évora', 'Évora'),
    ('Faro', 'Faro'),
    ('Guarda', 'Guarda'),
    ('Leiria', 'Leiria'),
    ('Lisboa', 'Lisboa'),
    ('Porto', 'Porto'),
    ('Vila Real', 'Vila Real'),
]

class AlgoritmoForm(forms.Form):
    algoritmo = forms.ChoiceField(choices=ALGORITMOS, label="Escolha o algoritmo")
    origem = forms.ChoiceField(choices=CIDADES, label="Cidade de origem")
    destino = forms.ChoiceField(choices=CIDADES, label="Cidade de destino", required=False)

    def clean(self):
        cleaned_data = super().clean()
        algoritmo = cleaned_data.get('algoritmo')
        destino = cleaned_data.get('destino')

        if algoritmo not in ['a_estrela', 'sofrega'] and not destino:
            raise forms.ValidationError("A cidade de destino é obrigatória para este algoritmo.")
