// "Add to my calendar" UI: both entry points open the dialog, the three links point at the
// calendar feed, the mini Feb/Mar calendar shades all 40 nights, and it closes cleanly —
// on desktop and on a phone-sized viewport, with no page errors or sideways scroll.
// Usage: node cal_ui_test.js   (needs `python build.py` first; exits non-zero on failure)
const launch = require('./pw_launch');
const FEED = 'zombiez4git.github.io/van-trampers-safari/South_Island_Safari_2027.ics';

(async () => {
  const browser = await launch();
  let fails = 0;
  const check = (ok, msg) => { if (!ok) { fails++; console.log('FAIL:', msg); } };

  for (const [name, w, h] of [['desktop', 1400, 1000], ['mobile', 390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.addInitScript(() => { window.__NO_AUTOPLAY = true; });
    await page.goto('file://' + process.cwd() + '/test_local.html');
    await page.waitForTimeout(1500);
    const isOpen = () => page.evaluate(() => !!document.getElementById('calDlg')?.open);

    // entry point 1: itinerary header
    const btn = page.locator('aside #calBtn');
    check(await btn.count() === 1 && await btn.isVisible(), `${name}: calendar button in the itinerary header`);
    if (await btn.count()) await btn.click();
    await page.waitForTimeout(400);
    check(await isOpen(), `${name}: header button opens the calendar dialog`);

    const href = async sel => (await page.locator(sel).count()) ? page.getAttribute(sel, 'href') : null;
    check(await href('#calApple') === 'webcal://' + FEED, `${name}: Apple link subscribes via webcal`);
    check(await href('#calGoogle') === 'https://calendar.google.com/calendar/r?cid=' + encodeURIComponent('webcal://' + FEED),
      `${name}: Google link opens add-by-URL`);
    check(await href('#calFile') === 'South_Island_Safari_2027.ics' &&
      (await page.locator('#calFile[download]').count()) === 1, `${name}: plain .ics download link`);

    // mini calendar: 40 shaded nights, Reefton on Feb 1-3, Geraldine to Mar 12, home on Mar 13
    const nights = await page.locator('#calDlg .cal-night').count();
    check(nights === 40, `${name}: mini calendar shades 40 nights (got ${nights})`);
    const hubOf = d => page.evaluate(d => document.querySelector(`#calDlg [data-date="${d}"]`)?.dataset.hub || null, d);
    check(await hubOf('2027-02-01') === '1' && await hubOf('2027-02-03') === '1' && await hubOf('2027-02-04') === '2',
      `${name}: Reefton shaded Feb 1–3, Denniston from Feb 4`);
    check(await hubOf('2027-03-12') === '15', `${name}: Geraldine shaded to Mar 12`);
    check(await page.locator('#calDlg [data-date="2027-03-13"].cal-home').count() === 1, `${name}: Mar 13 marked as home day`);

    // fits the screen
    const box = (await page.locator('#calDlg').count()) ? await page.locator('#calDlg').boundingBox() : null;
    check(box && box.x >= 0 && box.x + box.width <= w && box.height <= h, `${name}: dialog fits the viewport (${JSON.stringify(box)})`);
    await page.screenshot({ path: `shot_cal_${name}.png` });

    // closes with Escape and with the close button
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    check(!(await isOpen()), `${name}: Escape closes the dialog`);

    // entry point 2: footer, next to the fridge-map PDF
    const foot = page.locator('footer #calBtn2');
    check(await foot.count() === 1, `${name}: second calendar button in the footer`);
    if (await foot.count()) { await foot.scrollIntoViewIfNeeded(); await foot.click(); }
    await page.waitForTimeout(400);
    check(await isOpen(), `${name}: footer button opens the dialog`);
    if (await page.locator('#calClose').count()) await page.click('#calClose');
    await page.waitForTimeout(300);
    check(!(await isOpen()), `${name}: close button closes the dialog`);

    const sideways = await page.evaluate(() => document.scrollingElement.scrollWidth > innerWidth);
    check(!sideways, `${name}: no sideways scroll`);
    check(errs.length === 0, `${name}: no page errors (${errs.join(' | ')})`);
    await page.close();
  }
  await browser.close();
  console.log(fails ? `${fails} check(s) failed` : 'Calendar UI OK — desktop + mobile');
  process.exit(fails ? 1 : 0);
})();
