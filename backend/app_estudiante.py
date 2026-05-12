import socket
import json
import time
import random

HOST = "127.0.0.1"
PORT = 5000

alumnos = [
    "Laura", "Mario", "Sofía", "Carlos", "Lucía",
    "Hugo", "Paula", "Daniel", "Elena", "Adrián"
]

facultades = [
    "Informática", "Matemáticas", "Derecho",
    "Educación", "Enfermería", "ADE"
]


productos = {
    "Café solo": {"tipo": "barra", "precio": 1.20, "kcal": 2, "prot": 0.1, "carb": 0, "grasas": 0},
    "Café con leche": {"tipo": "barra", "precio": 1.50, "kcal": 65, "prot": 3.4, "carb": 4.8, "grasas": 3.6},
    "Colacao": {"tipo": "barra", "precio": 1.60, "kcal": 150, "prot": 5, "carb": 25, "grasas": 2.5},
    "Zumo de naranja": {"tipo": "barra", "precio": 2.00, "kcal": 90, "prot": 1.4, "carb": 20, "grasas": 0.2},
    "Tostada": {"tipo": "cocina", "precio": 1.80, "kcal": 210, "prot": 6, "carb": 32, "grasas": 5},
    "Bocadillo de tortilla": {"tipo": "cocina", "precio": 3.50, "kcal": 550, "prot": 18, "carb": 45, "grasas": 30},
    "Bocadillo de jamón": {"tipo": "cocina", "precio": 3.80, "kcal": 420, "prot": 28, "carb": 38, "grasas": 12},
    "Menú del día": {"tipo": "cocina", "precio": 7.50, "kcal": 950, "prot": 45, "carb": 85, "grasas": 35},
    "Agua": {"tipo": "barra", "precio": 1.00, "kcal": 0, "prot": 0, "carb": 0, "grasas": 0},
    "Refresco": {"tipo": "barra", "precio": 1.80, "kcal": 140, "prot": 0, "carb": 35, "grasas": 0}
}


def generar_pedido(id_pedido):
    nombres = list(productos.keys())
    seleccionados = random.sample(nombres, random.randint(1, 3))

    total, kcal, prot, carb, grasas = 0, 0, 0, 0, 0
    necesita_cocina = False

    for n in seleccionados:
        p = productos[n]
        total += p["precio"]
        kcal += p["kcal"]
        prot += p["prot"]
        carb += p["carb"]
        grasas += p["grasas"]
        if p["tipo"] == "cocina": necesita_cocina = True

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
