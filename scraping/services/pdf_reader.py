import pdfplumber
from escales.models import Escala, ValorEscala, Pagina, Pais

HEADER_CROP = 27
END_CROP = 7426
FILE_NAME = "/home/adriansanmiguel/Escritorio/grade_recognition_system_fib/scraping/services/taulesministeri.pdf"


def clear_models():
    ValorEscala.objects.all().delete()
    Pagina.objects.all().delete()
    Escala.objects.all().delete()
    Pais.objects.all().delete()


def parse_decimal(value):
    if value is None:
        return None

    try:
        return float(value.strip().replace(",", "."))
    except ValueError:
        return None


def parse_valor_escala_row(row):
    return {
        "valor_origen": row[0].strip(),
        "valor_upc": parse_decimal(row[1]),
        "equiv_literal": row[3].strip(),
    }


def save_escala(data):

    if not data["pais"] or not data["escala"]:
        return None, None
    new_pais, pais_created = Pais.objects.get_or_create(
        nom_pais=data["pais"],
    )
    new_escala, escala_created = Escala.objects.get_or_create(
        nom_pais=new_pais,
        id_escala=data["escala"],
    )
    if len(data["taules"]) >= 3:
        last_table = data["taules"][-1]
        for row in last_table:
            if not row:
                continue

            parsed_row = parse_valor_escala_row(row)
            if parsed_row["valor_upc"] is None:
                continue
            mh = parsed_row["equiv_literal"] == "MATRICULA"
            ValorEscala.objects.update_or_create(
                escala=new_escala,
                valor_origen=parsed_row["valor_origen"],
                defaults={
                    "valor_upc": parsed_row["valor_upc"],
                    "matricula": mh,
                },
            )

    new_pagina, pagina_created = Pagina.objects.update_or_create(
        num_pagina=data["pagina"], escala=new_escala
    )
    return new_escala, new_pagina


def extract_pais(text):
    lines = text.splitlines()
    if lines:
        return lines[0].strip()
    return None


def extract_escala(text):
    for line in text.splitlines():
        if "Escala:" in line:
            return line.replace("Escala:", "").strip()
    return None


def read_pdf(file_name, header_crop, end_crop, clear):

    if clear:
        clear_models()
    result = []
    with pdfplumber.open(file_name) as pdf:
        for page_number, page in enumerate(
            pdf.pages[header_crop:end_crop], start=header_crop + 1
        ):
            bounding_box = (0, 90, page.width, page.height)
            area = page.crop(bounding_box)

            page_text = area.extract_text_simple() or ""
            page_tables = area.extract_tables()

            parsed_data = {
                "pagina": page_number,
                "pais": extract_pais(page_text),
                "escala": extract_escala(page_text),
                "taules": page_tables,
            }

            print(
                f"""
                --------------------------------------------------
                Pagina: {parsed_data["pagina"]}
                Pais: {parsed_data["pais"]}
                Escala: {parsed_data["escala"]}
                Taules detectades: {len(parsed_data["taules"])}
                --------------------------------------------------
                """
            )

            for index, table in enumerate(page_tables):
                print(f"Taula {index}: {len(table)} files")

            save_escala(parsed_data)
    return result
