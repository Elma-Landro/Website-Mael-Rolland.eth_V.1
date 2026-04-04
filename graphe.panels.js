/**
 * Panel controller extracted from graphe.html.
 * Keeps existing API and behavior for panel orchestration.
 */
(function attachPanelControllerFactory(globalObj) {
  function createGraphePanelController({ document, window, State }) {
    let panel, launcher, titleEl, metaEl, dragHandle, grip;
    let dragging = null;
    let resizing = null;
    const clamp = (v, min, max) => Math.max(min, Math.min(v, max));

    function setLauncherLabel() {
      if (!launcher) return;
      const hasSelection = Boolean(State.selectedId && State.maps.entities[State.selectedId]);
      launcher.classList.toggle('hidden', !hasSelection);
      launcher.title = panel.classList.contains('is-closed') ? 'Ouvrir le panneau d’information' : 'Ramener le panneau';
      launcher.textContent = panel.classList.contains('is-closed') ? 'ⓘ' : '◫';
    }

    function applyBounds(left, top, width, height) {
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const minW = window.matchMedia('(max-width: 900px)').matches ? 220 : 230;
      const minH = 170;
      const maxW = Math.min(window.matchMedia('(max-width: 900px)').matches ? 360 : 380, vw - 20);
      const maxH = Math.max(220, vh - 92);
      const w = clamp(width, minW, maxW);
      const h = clamp(height, minH, maxH);
      panel.style.width = `${w}px`;
      panel.style.height = `${h}px`;
      panel.style.left = `${clamp(left, 8, vw - w - 8)}px`;
      panel.style.top = `${clamp(top, 66, vh - h - 8)}px`;
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
    }

    function open() {
      panel.classList.remove('is-closed');
      panel.setAttribute('aria-hidden', 'false');
      setLauncherLabel();
    }
    function close() {
      panel.classList.add('is-closed');
      panel.classList.remove('is-minimized');
      panel.setAttribute('aria-hidden', 'true');
      setLauncherLabel();
    }
    function minimize() {
      panel.classList.toggle('is-minimized');
    }
    function focusPanel() { panel.style.zIndex = String(Date.now()); }

    function setMeta(title, subtitle) {
      if (titleEl) titleEl.textContent = title || 'Informations du nœud';
      if (metaEl) metaEl.textContent = subtitle || '';
    }

    function init() {
      panel = document.getElementById('detail-panel');
      launcher = document.getElementById('btn-info-launcher');
      titleEl = document.getElementById('detail-panel-title');
      metaEl = document.getElementById('detail-panel-meta');
      dragHandle = document.getElementById('btn-panel-drag');
      grip = document.getElementById('panel-resize-grip');
      if (!panel || !dragHandle || !grip) return;
      applyBounds(window.innerWidth - 330, 84, 300, 470);
      setLauncherLabel();
      document.getElementById('btn-panel-close')?.addEventListener('click', close);
      document.getElementById('btn-panel-minimize')?.addEventListener('click', minimize);
      launcher?.addEventListener('click', () => {
        open();
        panel.classList.remove('is-minimized');
        focusPanel();
      });
      panel.addEventListener('pointerdown', focusPanel);

      dragHandle.addEventListener('pointerdown', (e) => {
        e.preventDefault();
        dragging = { id: e.pointerId, x: e.clientX, y: e.clientY, rect: panel.getBoundingClientRect() };
        dragHandle.setPointerCapture(e.pointerId);
      });
      dragHandle.addEventListener('pointermove', (e) => {
        if (!dragging || dragging.id !== e.pointerId) return;
        applyBounds(
          dragging.rect.left + (e.clientX - dragging.x),
          dragging.rect.top + (e.clientY - dragging.y),
          dragging.rect.width,
          dragging.rect.height
        );
      });
      dragHandle.addEventListener('pointerup', (e) => { if (dragging?.id === e.pointerId) dragging = null; });
      dragHandle.addEventListener('pointercancel', (e) => { if (dragging?.id === e.pointerId) dragging = null; });

      grip.addEventListener('pointerdown', (e) => {
        e.preventDefault();
        resizing = { id: e.pointerId, x: e.clientX, y: e.clientY, rect: panel.getBoundingClientRect() };
        grip.setPointerCapture(e.pointerId);
      });
      grip.addEventListener('pointermove', (e) => {
        if (!resizing || resizing.id !== e.pointerId) return;
        applyBounds(
          resizing.rect.left,
          resizing.rect.top,
          resizing.rect.width + (e.clientX - resizing.x),
          resizing.rect.height + (e.clientY - resizing.y)
        );
      });
      grip.addEventListener('pointerup', (e) => { if (resizing?.id === e.pointerId) resizing = null; });
      grip.addEventListener('pointercancel', (e) => { if (resizing?.id === e.pointerId) resizing = null; });
      window.addEventListener('resize', () => {
        const rect = panel.getBoundingClientRect();
        applyBounds(rect.left, rect.top, rect.width, rect.height);
      });
    }

    return { init, open, close, minimize, setMeta, setLauncherLabel };
  }

  globalObj.createGraphePanelController = createGraphePanelController;
})(window);
