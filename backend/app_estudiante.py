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

productos = [
    ("Café solo", "barra", 1.20),
    ("Café con leche", "barra", 1.50),
    ("Colacao", "barra", 1.60),
    ("Zumo de naranja", "barra", 2.00),
    ("Tostada", "cocina", 1.80),
    ("Bocadillo de tortilla", "cocina", 3.50),
    ("Bocadillo de jamón", "cocina", 3.80),
    ("Menú del día", "cocina", 7.50),
    ("Agua", "barra", 1.00),
    ("Refresco", "barra", 1.80)
]


def generar_pedido(id_pedido):
    num_productos = random.randint(1, 3)
    seleccionados = random.sample(productos, num_productos)

    lista_productos = [p[0] for p in seleccionados]
    total = sum(p[2] for p in seleccionados)

    necesita_cocina = any(p[1] == "cocina" for p in seleccionados)
    destino = "cocina" if necesita_cocina else "barra"

    pedido = {
        "id": id_pedido,
        "alumno": random.choice(alumnos),
        "facultad": random.choice(facultades),
        "productos": lista_productos,
        "destino": destino,
        "total": round(total, 2)
    }

    return pedido


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
