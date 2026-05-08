from escales.models import ValorEscala

def grade_converter(escala, origen):
    try:
        val_esc = ValorEscala.objects.get(
            escala=escala,
            valor_origen=origen,
        )
        return val_esc.valor_upc
    except ValorEscala.DoesNotExist:
        return None