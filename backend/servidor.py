import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clientes = []


def manejar_cliente(conn, addr):
    print(f"[SERVIDOR] Nueva conexión desde {addr}")

    try:
        while True:
            mensaje = conn.recv(4096).decode("utf-8")

            if not mensaje:
                break

            print(f"[SERVIDOR] Pedido recibido: {mensaje}")

            for cliente in clientes:
                if cliente != conn:
                    try:
                        cliente.sendall(mensaje.encode("utf-8"))
                    except:
                        clientes.remove(cliente)

    except ConnectionResetError:
        print(f"[SERVIDOR] Cliente desconectado: {addr}")

    finally:
        if conn in clientes:
            clientes.remove(conn)
        conn.close()
        print(f"[SERVIDOR] Conexión cerrada con {addr}")


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"[SERVIDOR] Cafetería universitaria escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = servidor.accept()
        clientes.append(conn)

        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()


if __name__ == "__main__":
    iniciar_servidor()