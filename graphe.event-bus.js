/**
 * Minimal shared event bus for graphe runtime seams.
 * Small, reversible, and intentionally generic.
 */
(function attachGrapheEventBus(globalObj) {
  if (globalObj.GrapheEventBus) return;

  const listeners = {};

  function on(event, cb) {
    if (!listeners[event]) listeners[event] = [];
    listeners[event].push(cb);
  }

  function emit(event, payload) {
    const active = listeners[event] || [];
    active.forEach((cb) => cb(payload));
    return active.length > 0;
  }

  globalObj.GrapheEventBus = { on, emit };
})(window);
