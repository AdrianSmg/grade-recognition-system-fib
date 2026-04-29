from escala.models import ValorEscala


def grade_converter(escala, origen):

    val_esc = ValorEscala.objects.get(id_escala=escala, valor_origen=origen)
    result = val_esc.valor_upc
    return result
