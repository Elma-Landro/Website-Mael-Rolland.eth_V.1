/**
 * Pure helper utilities extracted from graphe.html.
 * Scope: tiny, reversible, behavior-preserving helpers only.
 */
(function attachGrapheHelpers(globalObj) {
  function escHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function generateId() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let id = '';
    const arr = new Uint8Array(22);
    crypto.getRandomValues(arr);
    for (let i = 0; i < 22; i++) id += chars[arr[i] % chars.length];
    return id;
  }

  function normalizeRelationName(v) {
    return (v || '').toString().trim().toLowerCase();
  }

  function canonicalizeRelationName(v) {
    return normalizeRelationName(v).replace(/[^a-z0-9]/g, '');
  }

  globalObj.GrapheHelpers = {
    escHtml,
    generateId,
    normalizeRelationName,
    canonicalizeRelationName,
  };
})(window);
