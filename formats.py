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

def format_stringdate(string_date):
    month = {
        "ene": "01",
        "feb": "02",
        "mar": "03",
        "abr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dic": "12"
    }

    string_date = string_date[5::].replace(".", "")
    m = string_date[0:3]
    string_date = string_date.replace(m, month[m])

    object_date = datetime.strptime(string_date, '%m %d %Y')
    formatted_date = object_date.strftime("%Y-%m-%d")

    return formatted_date
