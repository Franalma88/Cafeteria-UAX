const preparandoList = document.getElementById("preparando-list");
const listosList = document.getElementById("listos-list");

const fechaElemento = document.getElementById("fecha");
const horaElemento = document.getElementById("hora");

let pedidosPreparando = [];
let pedidosListos = [];


function actualizarReloj() {
  const ahora = new Date();

  const fecha = ahora.toLocaleDateString("es-ES", {
    weekday: "long",
    day: "numeric",
    month: "long"
  });

  const hora = ahora.toLocaleTimeString("es-ES", {
    hour: "2-digit",
    minute: "2-digit"
  });

  fechaElemento.textContent = fecha.charAt(0).toUpperCase() + fecha.slice(1);
  horaElemento.textContent = hora;
}

function crearPedidoHTML(pedido, tipo) {
  const esPreparando = tipo === "preparando";

  return `
    <article class="order-card ${esPreparando ? "preparing" : "ready"}">
      <div class="order-number">
        <small>Pedido</small>
        <strong>#${pedido.id}</strong>
      </div>

      <div class="divider"></div>

      <div class="order-info">
        <h3>${pedido.alumno}</h3>
        <p>${pedido.productos}</p>
      </div>

      <div class="badge ${esPreparando ? "badge-time" : "badge-ready"}">
        ${esPreparando ? "◷ " + pedido.tiempo : "✓ Listo"}
      </div>
    </article>
  `;
}

function renderizarPedidos() {
  preparandoList.innerHTML = pedidosPreparando
    .map(pedido => crearPedidoHTML(pedido, "preparando"))
    .join("");

  listosList.innerHTML = pedidosListos
    .map(pedido => crearPedidoHTML(pedido, "listo"))
    .join("");
    reproducir();
}

function convertirProductosATexto(productos) {
  if (Array.isArray(productos)) {
    return productos.join(" y ");
  }

  return productos;
}

function procesarEventoCocina(evento) {
  const pedido = {
    id: evento.id,
    alumno: evento.alumno || "Alumno",
    productos: convertirProductosATexto(evento.productos || ""),
    tiempo: evento.tiempo || "En 10–15 min"
  };

  const estado = evento.estado;

  console.log("[PANTALLA] Evento recibido desde cocina:", evento);

  if (estado === "PREPARANDO") {
    pedidosPreparando = pedidosPreparando.filter(p => p.id !== pedido.id);
    pedidosListos = pedidosListos.filter(p => p.id !== pedido.id);

    pedidosPreparando.push(pedido);
  }

  if (estado === "LISTO") {
    pedidosPreparando = pedidosPreparando.filter(p => p.id !== pedido.id);
    pedidosListos = pedidosListos.filter(p => p.id !== pedido.id);

    pedidosListos.unshift(pedido);
  }

  if (estado === "ENTREGADO") {
    pedidosPreparando = pedidosPreparando.filter(p => p.id !== pedido.id);
    pedidosListos = pedidosListos.filter(p => p.id !== pedido.id);
  }

  renderizarPedidos();
}

function conectarConCocina() {
  const socket = new WebSocket("ws://127.0.0.1:8765");

  socket.onopen = () => {
    console.log("[PANTALLA] Conectada a cocina por WebSocket");
  };

  socket.onmessage = (event) => {
    const datos = JSON.parse(event.data);
    procesarEventoCocina(datos);
  };

  socket.onclose = () => {
    console.log("[PANTALLA] Conexión con cocina cerrada. Reintentando...");

    setTimeout(() => {
      conectarConCocina();
    }, 3000);
  };

  socket.onerror = () => {
    console.log("[PANTALLA] Error de conexión con cocina");
  };
}

actualizarReloj();
renderizarPedidos();
conectarConCocina();


setInterval(actualizarReloj, 1000);