from django import forms

ALGORITMOS = [
    ('aprofundamento', 'Aprofundamento Progressivo'),
    ('custo_uniforme', 'Custo Uniforme'),
    ('a_estrela', 'A* (A Estrela)'),
    ('sofrega', 'Procura Sôfrega'),
]

class AlgoritmoForm(forms.Form):
    algoritmo = forms.ChoiceField(choices=ALGORITMOS, label="Escolha o algoritmo")
    origem = forms.CharField(label="Cidade de origem")
    destino = forms.CharField(label="Cidade de destino")
