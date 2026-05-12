import os

MENU_FILE = os.path.join(os.path.dirname(__file__), "menu.txt")


def load_menu():
    menu = {}
    with open(MENU_FILE, encoding="utf-8") as archivo:
        lineas = archivo.read().strip().splitlines()

    if not lineas:
        return menu

    header = [campo.strip() for campo in lineas[0].split("|")]
    for linea in lineas[1:]:
        if not linea.strip():
            continue
        partes = [parte.strip() for parte in linea.split("|")]
        if len(partes) != len(header):
            continue
        item = dict(zip(header, partes))
        nombre = item["nombre"]
        menu[nombre] = {
            "tipo": item["tipo"],
            "precio": float(item["precio"]),
            "kcal": float(item["kcal"]),
            "prot": float(item["prot"]),
            "carb": float(item["carb"]),
            "grasas": float(item["grasas"])
        }
    return menu
