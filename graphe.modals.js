/**
 * Modals utility extracted from graphe.html.
 * Keeps existing API: open, close, closeAll.
 */
(function attachGrapheModalsFactory(globalObj) {
  function createGrapheModals({ document }) {
    function open(id) {
      document.getElementById(id).classList.remove('hidden');
    }

    function close(id) {
      document.getElementById(id).classList.add('hidden');
    }

    function closeAll() {
      document.querySelectorAll('.modal-backdrop').forEach((m) => m.classList.add('hidden'));
    }

    // Close on backdrop click
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal-backdrop')) closeAll();
    });

    return { open, close, closeAll };
  }

  globalObj.createGrapheModals = createGrapheModals;
})(window);
