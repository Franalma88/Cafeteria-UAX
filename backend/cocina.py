import socket
import json
import asyncio
import threading
import time
import websockets

HOST_SERVIDOR = "127.0.0.1"
PUERTO_SERVIDOR = 5000

HOST_WEBSOCKET = "127.0.0.1"
PUERTO_WEBSOCKET = 8765

clientes_web = set()
loop_websocket = None


# Productos que realmente pertenecen a cocina
PRODUCTOS_COCINA = {
    "Tostada con tomate": 4,
    "Tostada": 4,
    "Bocadillo de tortilla": 7,
    "Bocadillo de jamón": 6,
    "Bocadillo vegetal": 6,
    "Menú del día": 12,
    "Pasta": 10,
    "Ensalada": 5,
    "Croissant mixto": 4
}


def calcular_tiempo_preparacion(productos_cocina):
    """
    Calcula el tiempo estimado de preparación.

    Se toma el producto que más tarda y se añade 1 minuto extra
    por cada producto adicional.
    """

    if not productos_cocina:
        return 0

    tiempos = [
        PRODUCTOS_COCINA.get(producto, 5)
        for producto in productos_cocina
    ]

    tiempo_base = max(tiempos)
    extra = max(0, len(productos_cocina) - 1)

    return tiempo_base + extra


async def enviar_a_websockets(mensaje):
    if not clientes_web:
        return

    mensaje_json = json.dumps(mensaje, ensure_ascii=False)
    clientes_desconectados = set()

    for cliente in clientes_web:
        try:
            await cliente.send(mensaje_json)
        except:
            clientes_desconectados.add(cliente)

    for cliente in clientes_desconectados:
        clientes_web.remove(cliente)


def publicar_evento_web(mensaje):
    if loop_websocket:
        asyncio.run_coroutine_threadsafe(
            enviar_a_websockets(mensaje),
            loop_websocket
        )


async def manejar_cliente_websocket(websocket):
    print("[COCINA] Pantalla de recogida conectada")
    clientes_web.add(websocket)

    try:
        await websocket.wait_closed()
    finally:
        clientes_web.remove(websocket)
        print("[COCINA] Pantalla de recogida desconectada")


async def iniciar_servidor_websocket():
    global loop_websocket

    loop_websocket = asyncio.get_running_loop()

    print(f"[COCINA] WebSocket activo en ws://{HOST_WEBSOCKET}:{PUERTO_WEBSOCKET}")

    async with websockets.serve(
        manejar_cliente_websocket,
        HOST_WEBSOCKET,
        PUERTO_WEBSOCKET
    ):
        await asyncio.Future()


def iniciar_websocket_en_hilo():
    asyncio.run(iniciar_servidor_websocket())


def obtener_productos_cocina(productos):
    """
    Recibe todos los productos del pedido y devuelve solo los que son de cocina.
    """

    productos_filtrados = []

    for producto in productos:
        if producto in PRODUCTOS_COCINA:
            productos_filtrados.append(producto)

    return productos_filtrados


def procesar_pedido(pedido):
    id_pedido = pedido.get("id")
    alumno = pedido.get("alumno", "Alumno")
    facultad = pedido.get("facultad", "Sin facultad")
    productos = pedido.get("productos", [])

    productos_cocina = obtener_productos_cocina(productos)

    if not productos_cocina:
        print(f"[COCINA] Pedido #{id_pedido} ignorado. No tiene productos de cocina.")
        return

    tiempo_estimado = calcular_tiempo_preparacion(productos_cocina)

    print("\n[COCINA] Pedido de cocina recibido")
    print(f"ID: #{id_pedido}")
    print(f"Alumno: {alumno}")
    print(f"Facultad: {facultad}")
    print(f"Productos cocina: {productos_cocina}")
    print(f"Tiempo estimado: {tiempo_estimado} minutos")

    evento_preparando = {
        "id": id_pedido,
        "alumno": alumno,
        "facultad": facultad,
        "productos": productos_cocina,
        "estado": "PREPARANDO",
        "tiempo": f"En {tiempo_estimado} min"
    }

    publicar_evento_web(evento_preparando)

    print(f"[COCINA] Pedido #{id_pedido} enviado a pantalla como PREPARANDO")

    # Simulación acelerada:
    # 1 minuto real de cocina = 1 segundo en la demo
    time.sleep(tiempo_estimado)

    evento_listo = {
        "id": id_pedido,
        "alumno": alumno,
        "facultad": facultad,
        "productos": productos_cocina,
        "estado": "LISTO",
        "tiempo_respuesta": f"{tiempo_estimado} min"
    }

    publicar_evento_web(evento_listo)

    print(f"[COCINA] Pedido #{id_pedido} enviado a pantalla como LISTO")
    print(f"[COCINA] Tiempo de respuesta del pedido #{id_pedido}: {tiempo_estimado} minutos")


def escuchar_servidor_tcp():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST_SERVIDOR, PUERTO_SERVIDOR))

    print("[COCINA] Conectada al servidor principal")
    print("[COCINA] Esperando pedidos de cocina...")

    buffer = ""

    while True:
        datos = cliente.recv(4096).decode("utf-8")

        if not datos:
            break

        buffer += datos

        if "\n" in buffer:
            partes = buffer.split("\n")
            buffer = partes[-1]

            for parte in partes[:-1]:
                if parte.strip():
                    pedido = json.loads(parte.strip())

                    hilo = threading.Thread(
                        target=procesar_pedido,
                        args=(pedido,),
                        daemon=True
                    )
                    hilo.start()

        else:
            try:
                pedido = json.loads(buffer)
                buffer = ""

                hilo = threading.Thread(
                    target=procesar_pedido,
                    args=(pedido,),
                    daemon=True
                )
                hilo.start()

            except json.JSONDecodeError:
                pass


if __name__ == "__main__":
    hilo_websocket = threading.Thread(
        target=iniciar_websocket_en_hilo,
        daemon=True
    )
    hilo_websocket.start()

    time.sleep(1)

    escuchar_servidor_tcp()