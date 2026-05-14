function renderSidebar() {
  const html = `
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="brand">BodegaOS</div>
      <div class="sub">v2.0.0</div>
    </div>
    <nav>
      <a href="dashboard.html"><span class="icon">📊</span><span>Dashboard</span></a>
      <a href="productos.html"><span class="icon">📦</span><span>Productos</span></a>
      <a href="clientes.html"><span class="icon">👥</span><span>Clientes</span></a>
      <a href="pedidos.html"><span class="icon">🛒</span><span>Pedidos</span></a>
      <a href="chat.html"><span class="icon">💬</span><span>Chat</span></a>
      <a href="reporte_utilidad.html"><span class="icon">📈</span><span>Utilidad</span></a>
    </nav>
    <div class="sidebar-footer">BodegaOS &copy; 2025</div>
  </aside>`;
  document.body.insertAdjacentHTML("afterbegin", html);
  markActiveNav();
}
