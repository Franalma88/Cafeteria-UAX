# Cafetería UAX

## Objetivo del proyecto

Este proyecto simula el flujo de pedidos de una cafetería universitaria. Incluye:

- Un servidor central que recibe pedidos de estudiantes.
- Un módulo de cocina que procesa los pedidos con productos de cocina y notifica el estado a una pantalla de recogida.
- Un módulo de barra que recibe y muestra los pedidos de bebidas y productos de barra.
- Una pantalla frontend que muestra los pedidos en preparación y listos para recoger.

Está pensado como una demo de comunicación entre procesos usando sockets TCP y WebSockets, con una interfaz visual para la recogida.

## Arquitectura

- `backend/servidor.py`: servidor TCP central que recibe pedidos y retransmite los mensajes a todos los clientes conectados.
- `backend/app_estudiante.py`: simulador de la app de estudiante que envía pedidos aleatorios al servidor.
- `backend/barra.py`: cliente que recibe pedidos desde el servidor y muestra los productos que corresponden a la barra.
- `backend/cocina.py`: cliente que procesa los pedidos de cocina y publica el estado de preparación/listo mediante WebSocket.
- `frontend/`: pantalla de recogida que se conecta al servidor WebSocket de cocina y muestra los pedidos.

## Requisitos

- Python 3.8+ (o versión compatible)
- Módulo `websockets`

## Instalación de dependencias

Desde el directorio raíz del proyecto:

```powershell
pip install websockets
```

## Ejecución

1. Abrir un terminal y lanzar el servidor central:

```powershell
python backend\servidor.py
```

2. En otro terminal, iniciar el módulo de cocina:

```powershell
python backend\cocina.py
```

3. En otro terminal, iniciar el módulo de barra (opcional, para ver pedidos de barra):

```powershell
python backend\barra.py
```

4. En otro terminal, iniciar el simulador de la app de estudiante:

```powershell
python backend\app_estudiante.py
```

5. Abrir `frontend/index.html` en un navegador para ver la pantalla de recogida.

> Nota: la pantalla frontend se conecta a `ws://127.0.0.1:8765`, por lo que el script `backend/cocina.py` debe estar en ejecución.

## Cómo funciona

- `app_estudiante.py` genera pedidos aleatorios de alumnos con productos de barra y/o cocina.
- El pedido se envía al servidor central `backend/servidor.py` en el puerto `5000`.
- El servidor retransmite el pedido a todos los clientes conectados:
  - `backend/barra.py` filtra y muestra los productos de barra.
  - `backend/cocina.py` filtra los productos de cocina y calcula un tiempo estimado de preparación.
- `backend/cocina.py` publica eventos de estado al frontend mediante WebSocket:
  - `PREPARANDO`: pedido en curso.
  - `LISTO`: pedido listo para recoger.

## Puertos usados

- TCP del sistema de pedidos: `127.0.0.1:5000`
- WebSocket de cocina: `127.0.0.1:8765`

## Estructura de archivos

- `backend/servidor.py`
- `backend/app_estudiante.py`
- `backend/barra.py`
- `backend/cocina.py`
- `frontend/index.html`
- `frontend/css/styles.css`
- `frontend/js/app.js`
- `frontend/img/`

## Sugerencias de mejora

- Añadir una pantalla de pedidos para la barra con WebSocket en lugar de solo consola.
- Integrar una app de estudiante real con formulario y selección de productos.
- Añadir un servidor HTTP para servir el frontend de forma local.
- Implementar una base de datos para registrar el historial de pedidos.
