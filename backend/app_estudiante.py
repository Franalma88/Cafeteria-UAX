import socket
import json
import time
import random
from menu_loader import load_menu

HOST = "127.0.0.1"
PORT = 5000

MENU = load_menu()

alumnos = [
    "Laura", "Mario", "Sofía", "Carlos", "Lucía",
    "Hugo", "Paula", "Daniel", "Elena", "Adrián"
]

facultades = [
    "Informática", "Matemáticas", "Derecho",
    "Educación", "Enfermería", "ADE"
]


def generar_pedido(id_pedido):
    nombres = list(MENU.keys())
    seleccionados = random.sample(nombres, random.randint(1, 3))

    total, kcal, prot, carb, grasas = 0, 0, 0, 0, 0
    necesita_cocina = False

    for n in seleccionados:
        p = MENU[n]
        total += p["precio"]
        kcal += p["kcal"]
        prot += p["prot"]
        carb += p["carb"]
        grasas += p["grasas"]
        if p["tipo"] != "barra":
            necesita_cocina = True

    return {
        "id": id_pedido,
        "alumno": random.choice(alumnos),
        "facultad": random.choice(facultades),
        "productos": seleccionados,
        "destino": "cocina" if necesita_cocina else "barra",
        "nutricion": {
            "calorias": kcal, "proteinas": round(prot, 1), 
            "carbohidratos": round(carb, 1), "grasas": round(grasas, 1)
        },
        "total": round(total, 2)
    }

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    print("[APP ESTUDIANTE] Conectada al sistema de la cafetería")

    id_pedido = 1

    while True:
        pedido = generar_pedido(id_pedido)
        mensaje = json.dumps(pedido, ensure_ascii=False)

        cliente.sendall(mensaje.encode("utf-8"))

        print(f"[APP ESTUDIANTE] Pedido enviado: {pedido}")

        id_pedido += 1
        time.sleep(4)

# main
if __name__ == "__main__":
    main()
