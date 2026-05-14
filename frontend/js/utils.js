// BodegaOS — utilidades compartidas

const API = "http://127.0.0.1:8000/api";

// ── Fetch helper ──────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Error en la solicitud");
  }
  if (res.status === 204) return null;
  return res.json();
}

// ── Toast ─────────────────────────────────────────────────
function toast(msg, type = "ok") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }
  const t = document.createElement("div");
  t.className = "toast" + (type === "error" ? " error" : type === "warn" ? " warn" : "");
  t.textContent = msg;
  container.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ── Modal helpers ─────────────────────────────────────────
function openModal(id) {
  document.getElementById(id).classList.add("open");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("open");
}

// ── Formatters ────────────────────────────────────────────
function fmtMoney(n) {
  return "S/ " + parseFloat(n || 0).toFixed(2);
}

function fmtDate(d) {
  if (!d) return "—";
  return new Date(d).toLocaleString("es-PE", { dateStyle: "short", timeStyle: "short" });
}

function fmtDateShort(d) {
  if (!d) return "—";
  return new Date(d).toLocaleDateString("es-PE");
}

// ── Estado badge ──────────────────────────────────────────
function estadoBadge(estado) {
  const map = {
    pendiente:   "tag-warn",
    en_proceso:  "tag-blue",
    confirmado:  "tag-green",
    entregado:   "tag-green",
    cancelado:   "tag-danger",
    activo:      "tag-green",
    inactivo:    "tag-gray",
    minorista:   "tag-blue",
    mayorista:   "tag-warn",
  };
  const cls = map[estado] || "tag-gray";
  return `<span class="tag ${cls}">${estado}</span>`;
}

// ── Mark active nav link ───────────────────────────────────
function markActiveNav() {
  const page = location.pathname.split("/").pop();
  document.querySelectorAll(".sidebar nav a").forEach(a => {
    if (a.getAttribute("href") === page) a.classList.add("active");
  });
}

document.addEventListener("DOMContentLoaded", markActiveNav);
