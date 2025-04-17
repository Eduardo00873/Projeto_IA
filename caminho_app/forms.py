from django import forms
import os

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
    algoritmo = forms.ChoiceField(
        choices=[('', 'Selecione...')] + ALGORITMOS,
        label="Escolha o algoritmo"
    )
    origem = forms.ChoiceField(
        choices=[('', 'Selecione...')] + CIDADES,
        label="Cidade de origem"
    )
    destino = forms.ChoiceField(
        choices=[('', 'Selecione...')] + CIDADES,
        label="Cidade de destino",
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        algoritmo = cleaned_data.get('algoritmo')
        destino = cleaned_data.get('destino')

        if algoritmo not in ['a_estrela', 'sofrega'] and not destino:
            raise forms.ValidationError("A cidade de destino é obrigatória para este algoritmo.")


class EscolherImagemForm(forms.Form):
    def get_opcoes_imagens():
        pasta = 'caminho_app/static/imagens'
        opcoes = []
        for nome_arquivo in os.listdir(pasta):
            if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                caminho = os.path.join(pasta, nome_arquivo)
                opcoes.append((caminho, nome_arquivo))
        return opcoes

    imagem = forms.ChoiceField(
        choices=get_opcoes_imagens(),
        label="Escolha uma imagem",
        widget=forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'})
    )