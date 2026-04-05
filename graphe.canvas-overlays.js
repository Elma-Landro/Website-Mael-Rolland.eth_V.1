/**
 * Canvas overlays helper extracted from graphe.html.
 * Scope intentionally limited to halo overlay lifecycle and drawing.
 */
(function attachCanvasOverlaysFactory(globalObj) {
  function createGrapheCanvasOverlays({
    document,
    windowObj,
    requestAnimationFrame,
    cancelAnimationFrame,
    getCy,
    canvasId,
    getCanvasHost,
  }) {
    let haloActive = false;
    let haloRAF = null;
    let haloConfig = null;

    function haloCanvas() {
      let c = document.getElementById(canvasId);
      if (!c) {
        c = document.createElement('canvas');
        c.id = canvasId;
        const host = getCanvasHost();
        if (!host) {
          console.warn('[graphe.canvas-overlays] Missing canvas host (.grc-canvas-wrap); halo overlay draw skipped.');
          return null;
        }
        host.appendChild(c);
      }
      return c;
    }

    function drawHalos() {
      const cy = getCy();
      if (!haloActive || !haloConfig || !cy) return;
      const canvas = haloCanvas();
      if (!canvas || !canvas.parentElement) return;
      const wrap = canvas.parentElement;
      canvas.width = wrap.clientWidth;
      canvas.height = wrap.clientHeight;
      const ctx = canvas.getContext('2d');
      const pan = cy.pan();
      const zoom = cy.zoom();

      function rgb(hex) {
        return [parseInt(hex.slice(1, 3), 16), parseInt(hex.slice(3, 5), 16), parseInt(hex.slice(5, 7), 16)];
      }

      if (haloConfig.cells) {
        // ── Mode matrice : radial gradient per cell (chapter × col intersection) ──
        // CSS mix-blend-mode:screen handles additive compositing → nebula glow.
        const { cells, cellW, cellH } = haloConfig;
        cells.forEach(({ modelX, modelY, color }) => {
          const sx = modelX * zoom + pan.x;
          const sy = modelY * zoom + pan.y;
          const sw = cellW * zoom;
          const sh = cellH * zoom;
          const [r, g, b] = rgb(color);
          const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
          grad.addColorStop(0, `rgba(${r},${g},${b},0.32)`);
          grad.addColorStop(0.35, `rgba(${r},${g},${b},0.18)`);
          grad.addColorStop(0.75, `rgba(${r},${g},${b},0.07)`);
          grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
          ctx.save();
          ctx.translate(sx, sy);
          ctx.scale(sw / 2, sh / 2);
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(0, 0, 1, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        });
      } else {
        // ── Mode linéaire : bandes horizontales + verticales (monétisation, arbre) ──
        const { rows, cols, modelH, modelColW } = haloConfig;
        const W = canvas.width;
        const H = canvas.height;
        rows.forEach(({ modelY, color }) => {
          const sy = modelY * zoom + pan.y;
          const sh = modelH * zoom;
          const [r, g, b] = rgb(color);
          const grad = ctx.createLinearGradient(0, sy - sh * 0.6, 0, sy + sh * 0.6);
          grad.addColorStop(0, `rgba(${r},${g},${b},0)`);
          grad.addColorStop(0.25, `rgba(${r},${g},${b},0.03)`);
          grad.addColorStop(0.5, `rgba(${r},${g},${b},0.08)`);
          grad.addColorStop(0.75, `rgba(${r},${g},${b},0.03)`);
          grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
          ctx.fillStyle = grad;
          ctx.fillRect(0, sy - sh * 0.6, W, sh * 1.2);
        });
        (cols || []).forEach(({ modelX, color }) => {
          const sx = modelX * zoom + pan.x;
          const sw = (modelColW || 0) * zoom;
          const [r, g, b] = rgb(color);
          const grad = ctx.createLinearGradient(sx - sw * 0.6, 0, sx + sw * 0.6, 0);
          grad.addColorStop(0, `rgba(${r},${g},${b},0)`);
          grad.addColorStop(0.25, `rgba(${r},${g},${b},0.02)`);
          grad.addColorStop(0.5, `rgba(${r},${g},${b},0.04)`);
          grad.addColorStop(0.75, `rgba(${r},${g},${b},0.02)`);
          grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
          ctx.fillStyle = grad;
          ctx.fillRect(sx - sw * 0.6, 0, sw * 1.2, H);
        });
      }
    }

    function scheduleHaloDraw() {
      if (haloRAF) return;
      haloRAF = requestAnimationFrame(() => {
        haloRAF = null;
        drawHalos();
      });
    }

    function startHaloOverlay(config) {
      const cy = getCy();
      haloConfig = config;
      haloActive = true;
      if (cy) cy.on('viewport', scheduleHaloDraw);
      windowObj.addEventListener('resize', scheduleHaloDraw);
      drawHalos(); // immediate draw after layout fit
    }

    function stopHaloOverlay() {
      const cy = getCy();
      haloActive = false;
      haloConfig = null;
      if (cy) cy.off('viewport', scheduleHaloDraw);
      windowObj.removeEventListener('resize', scheduleHaloDraw);
      if (haloRAF) {
        cancelAnimationFrame(haloRAF);
        haloRAF = null;
      }
      const c = document.getElementById(canvasId);
      if (c) c.getContext('2d').clearRect(0, 0, c.width, c.height);
    }

    return {
      drawHalos,
      startHaloOverlay,
      stopHaloOverlay,
    };
  }

  globalObj.createGrapheCanvasOverlays = createGrapheCanvasOverlays;
})(window);
