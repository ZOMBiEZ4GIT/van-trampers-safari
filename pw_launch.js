// Shared Playwright launcher for the screenshot/test/PDF scripts.
// Uses Playwright's bundled Chromium when it exists; otherwise falls back to a
// preinstalled browser (CHROMIUM_PATH env var, or the usual sandbox/system paths)
// so the scripts still run where browser downloads are blocked.
const { chromium } = require('playwright');
const fs = require('fs');
module.exports = function launch(opts = {}) {
  let bundled = false;
  try { bundled = fs.existsSync(chromium.executablePath()); } catch (e) {}
  if (!bundled) {
    const cands = [process.env.CHROMIUM_PATH, '/opt/pw-browsers/chromium',
      '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome'].filter(Boolean);
    const p = cands.find(c => fs.existsSync(c));
    if (p) opts = { executablePath: p, ...opts };
  }
  return chromium.launch(opts);
};
