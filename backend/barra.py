import socket
import json

HOST = "127.0.0.1"
PORT = 5000


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    print("[BARRA] Conectada al sistema de pedidos")

    while True:
        mensaje = cliente.recv(4096).decode("utf-8")

        if mensaje:
            pedido = json.loads(mensaje)

            productos_barra = [
                "Café solo",
                "Café con leche",
                "Colacao",
                "Zumo de naranja",
                "Agua",
                "Refresco"
            ]

            productos_para_barra = [
                producto for producto in pedido["productos"]
                if producto in productos_barra
            ]

            if productos_para_barra:
                print("\n[BARRA] Nuevo pedido para preparar")
                print(f"Pedido #{pedido['id']}")
                print(f"Alumno: {pedido['alumno']}")
                print(f"Facultad: {pedido['facultad']}")
                print(f"Preparar: {', '.join(productos_para_barra)}")
            else:
                print(f"[BARRA] Pedido #{pedido['id']} no tiene productos de barra")


if __name__ == "__main__":
    main()