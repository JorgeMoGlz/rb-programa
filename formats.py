from datetime import date, datetime, timedelta

def format_fecha_hoy(objeto_fecha):
    month = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre"
    }

    m = objeto_fecha.month

    fecha_formateada = objeto_fecha.strftime("%d de {} del %Y".format(month[m]))

    return fecha_formateada
