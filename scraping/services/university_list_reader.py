import pandas as pd
from escales.models import Universitat, Pais

FILE_NAME = "/home/adriansanmiguel/Escritorio/grade_recognition_system_fib/scraping/services/universities.csv"
universities = pd.read_csv(FILE_NAME)


def clear_models():
    Universitat.objects.all().delete()


def find_pais(nom_csv):
    variants = [
        nom_csv.strip(),
        nom_csv.strip().upper(),
        nom_csv.strip().capitalize(),
    ]
    for variant in variants:
        pais = Pais.objects.filter(nom_pais=variant).first()
        if pais:
            return pais

    return None


def load_universities():
    clear_models()
    for _, row in universities.iterrows():
        nom_complet = row["University name"]
        if " - " in nom_complet:
            nom_universitat, facultat = nom_complet.split(" - ", maxsplit=1)
        else:
            nom_universitat = nom_complet
            facultat = ""

        pais = find_pais(row["Country"])

        Universitat.objects.get_or_create(
            codi_universitat=row["University code"],
            defaults={
                "nom_universitat": nom_universitat.strip(),
                "facultat": facultat.strip(),
                "programa": row["Program"],
                "pais": pais,
            },
        )
