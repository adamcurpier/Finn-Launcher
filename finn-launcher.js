/* TCL Flip 4 minimalist launcher v5 */
(function () {
  'use strict';

  var items = [
    { label: 'Applications', app: null },
    { label: 'Messages', app: 'sms' },
    { label: 'Calendar', app: 'calendar' },
    { label: 'Notes', app: 'notes' }
  ];
  var selected = 0;
  var panel = null;
  var captured = {};

  function isHome() {
    try {
      var service = window.TCLLauncherServices;
      var sheet = service && service.query('lastSheet');
      return !sheet || sheet === 'mainView';
    } catch (e) { return true; }
  }

  function dialerShown() {
    try {
      return !!(window.TCLLauncherServices &&
        window.TCLLauncherServices.query('Dialer.isShown'));
    } catch (e) { return false; }
  }

  function status(message) {
    var element = document.getElementById('finn-launcher-status');
    if (element) element.textContent = message;
  }

  function render() {
    if (!panel) return;
    panel.textContent = '';
    items.forEach(function (item, index) {
      var line = document.createElement('div');
      line.textContent = (index === selected ? '› ' : '  ') + item.label;
      panel.appendChild(line);
    });
    var small = document.createElement('small');
    small.id = 'finn-launcher-status';
    small.textContent = '';
    panel.appendChild(small);
  }

  function openApp(name) {
    try {
      if (!window.AppOrigin) throw new Error('AppOrigin unavailable');
      var manifest = window.AppOrigin.getManifestURL(name);
      if (!manifest) throw new Error('App not found');
      window.open(manifest, '_blank', 'kind=app,noopener=yes');
    } catch (e) {
      status('Unable to open app');
    }
  }

  function activate() {
    var item = items[selected];
    if (item.app) return openApp(item.app);
    if (!window.TCLLauncherServices) {
      status('Applications unavailable');
      return;
    }
    window.TCLLauncherServices.request('openSheet', 'appList')
      .then(function () { sync(); })
      .catch(function () { status('Applications unavailable'); });
  }

  function sync() {
    if (panel) panel.style.setProperty('display', (isHome() && !dialerShown()) ? 'block' : 'none', 'important');
  }

  function keydown(e) {
    if (!panel || document.hidden || !isHome() || dialerShown()) return;
    var key = e.key;
    if (['ArrowDown', 'Enter'].indexOf(key) < 0) return;
    captured[key] = true;
    e.preventDefault();
    e.stopImmediatePropagation();
    if (e.repeat && (key === 'Enter' || key === 'SoftRight')) return;
    if (key === 'ArrowDown') selected = (selected + 1) % 4;
    if (key === 'Enter') activate();
    render();
  }

  function keyup(e) {
    if (!captured[e.key]) return;
    delete captured[e.key];
    e.preventDefault();
    e.stopImmediatePropagation();
  }

  function init() {
    if (!document.body || panel) return;
    panel = document.createElement('div');
    panel.id = 'finn-launcher-menu';
    document.body.appendChild(panel);
    render();
    sync();
  }

  window.addEventListener('keydown', keydown, true);
  window.addEventListener('keyup', keyup, true);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
  window.setTimeout(init, 2000);
  window.addEventListener('panelChange', sync);
  window.setInterval(sync, 500);
})();
