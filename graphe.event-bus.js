/**
 * Minimal event bus spike for Graph extraction.
 * Scope intentionally limited to tiny pub/sub.
 */
(function attachEventBusFactory(globalObj) {
  function createGrapheEventBus() {
    const listeners = new Map();

    function on(eventName, handler) {
      if (!listeners.has(eventName)) listeners.set(eventName, new Set());
      listeners.get(eventName).add(handler);
      return () => off(eventName, handler);
    }

    function off(eventName, handler) {
      const set = listeners.get(eventName);
      if (!set) return;
      set.delete(handler);
      if (!set.size) listeners.delete(eventName);
    }

    function emit(eventName, payload) {
      const set = listeners.get(eventName);
      if (!set) return;
      for (const handler of set) handler(payload);
    }

    return { on, off, emit };
  }

  function getGrapheEventBus() {
    if (!globalObj.__grapheEventBus) globalObj.__grapheEventBus = createGrapheEventBus();
    return globalObj.__grapheEventBus;
  }

  globalObj.createGrapheEventBus = createGrapheEventBus;
  globalObj.getGrapheEventBus = getGrapheEventBus;
})(window);
