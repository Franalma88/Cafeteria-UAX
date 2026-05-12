import json
import random
import socket
import time
from menu_loader import load_menu

HOST = "127.0.0.1"
PORT = 5000

MENU = load_menu()
PEDIDO_ID = 1

SUGERENCIAS = {
    "rápido": ["Café solo", "Bocadillo vegetal", "Croissant mixto"],
    "saludable": ["Ensalada César", "Fruta fresca", "Zumo de naranja"],
    "dulce": ["Colacao", "Brownie", "Yogur con granola"],
    "ligero": ["Ensalada César", "Agua con gas", "Fruta fresca"],
    "energético": ["Café con leche", "Bocadillo de tortilla", "Tostada con tomate"],
    "snack": ["Croissant mixto", "Bocadillo vegetal", "Yogur con granola"]
}

NOMBRE_A_CLAVE = {nombre.lower(): nombre for nombre in MENU}


def imprimir_titulo():
    print("\n=== CAFETERÍA UAX - PEDIDOS INTERACTIVOS ===\n")


def mostrar_menu():
    categorias = {
        "barra": "Bebidas y barra",
        "cocina": "Platos calientes",
        "postre": "Postres"
    }
    print("Menú disponible:")
    por_tipo = {}
    for nombre, info in MENU.items():
        por_tipo.setdefault(info["tipo"], []).append(nombre)

    for tipo, nombres in por_tipo.items():
        etiqueta = categorias.get(tipo, tipo.title())
        print(f"\n{etiqueta}:")
        for nombre in sorted(nombres):
            precio = MENU[nombre]["precio"]
            print(f"  - {nombre} · {precio:.2f} €")
    print("")


def obtener_nombre_producto(entrada):
    return NOMBRE_A_CLAVE.get(entrada.strip().lower())


def recomendar_por_preferencia(preferencia):
    clave = preferencia.strip().lower()
    if clave in SUGERENCIAS:
        return SUGERENCIAS[clave]

    for palabra, recomendaciones in SUGERENCIAS.items():
        if palabra in clave:
            return recomendaciones

    return random.choice(list(SUGERENCIAS.values()))


def asistente_recomendaciones():
    print("\nAsistente: Cuéntame qué te apetece. Puedo recomendar cosas según tu hambre.")
    preguntas = [
        "¿Te apetece algo rápido, saludable, dulce, ligero o energético?",
        "¿Prefieres bebida, desayuno o comida?",
        "¿Quieres algo para comer ahora o algo para más tarde?"
    ]
    respuestas = []
    for pregunta in preguntas:
        respuesta = input(f"{pregunta}\n> ").strip().lower()
        if respuesta:
            respuestas.append(respuesta)
    preferencia = " " .join(respuestas)
    recomendaciones = recomendar_por_preferencia(preferencia)
    print("\nTe recomiendo probar:")
    for item in recomendaciones[:3]:
        tipo = MENU[item]["tipo"] if item in MENU else "desconocido"
        print(f"  • {item} ({tipo})")
    print("\nSi quieres, escribe uno de esos nombres para añadirlo al pedido.")


def crear_pedido(nombre, facultad, productos):
    global PEDIDO_ID
    necesita_cocina = any(MENU[item]["tipo"] != "barra" for item in productos)
    nutricion = {
        "calorias": round(sum(MENU[item].get("kcal", 0) for item in productos), 1),
        "proteinas": round(sum(MENU[item].get("prot", 0) for item in productos), 1),
        "carbohidratos": round(sum(MENU[item].get("carb", 0) for item in productos), 1),
        "grasas": round(sum(MENU[item].get("grasas", 0) for item in productos), 1)
    }
    pedido = {
        "id": PEDIDO_ID,
        "alumno": nombre,
        "facultad": facultad,
        "productos": productos,
        "destino": "cocina" if necesita_cocina else "barra",
        "nutricion": nutricion,
        "total": round(sum(MENU[item]["precio"] for item in productos), 2)
    }
    PEDIDO_ID += 1
    return pedido


def enviar_pedido(pedido):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))
            cliente.sendall(json.dumps(pedido, ensure_ascii=False).encode("utf-8"))
        print("\n✅ Pedido enviado al servidor de la cafetería.")
    except ConnectionRefusedError:
        print("\n⚠️ No se pudo conectar con el servidor. Asegúrate de que el backend esté en marcha.")


def capturar_pedido():
    productos = []
    print("Escribe los nombres de los productos uno por uno. Escribe 'fin' para terminar.")
    print("Escribe 'menu' para ver el menú otra vez o 'sugerir' para que el asistente te ayude.")

    while True:
        entrada = input("> ").strip()
        if not entrada:
            continue
        comando = entrada.lower()
        if comando == "fin":
            break
        if comando == "menu":
            mostrar_menu()
            continue
        if comando == "sugerir":
            asistente_recomendaciones()
            continue

        nombre = obtener_nombre_producto(entrada)
        if nombre:
            productos.append(nombre)
            print(f"Añadido: {nombre}")
        else:
            print("No reconozco ese producto. Prueba de nuevo o escribe 'menu' para ver la lista.")

    return productos


def main():
    imprimir_titulo()
    nombre = input("Tu nombre: ").strip() or "Cliente"
    facultad = input("Tu facultad o grupo: ").strip() or "Sin facultad"

    mostrar_menu()
    if input("¿Quieres ayuda del asistente para elegir? (s/n): ").strip().lower() in {"s", "si"}:
        asistente_recomendaciones()

    productos = capturar_pedido()
    if not productos:
        print("No se creó ningún pedido.")
        return

    pedido = crear_pedido(nombre, facultad, productos)
    print("\nResumen del pedido:")
    for item in pedido["productos"]:
        print(f"  - {item} · {MENU[item]['precio']:.2f} €")
    print(f"Total: {pedido['total']:.2f} €")
    print("Macronutrientes totales:")
    print(f"  - Calorías: {pedido['nutricion']['calorias']} kcal")
    print(f"  - Proteínas: {pedido['nutricion']['proteinas']} g")
    print(f"  - Carbohidratos: {pedido['nutricion']['carbohidratos']} g")
    print(f"  - Grasas: {pedido['nutricion']['grasas']} g")

    if input("Enviar pedido ahora? (s/n): ").strip().lower() in {"s", "si"}:
        enviar_pedido(pedido)
    else:
        print("Pedido cancelado.")


if __name__ == "__main__":
    main()
