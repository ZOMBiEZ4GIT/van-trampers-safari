const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  for (const [name, w, h] of [['desktop',1400,1000],['mobile',390,844]]) {
    const page = await browser.newPage({viewport:{width:w,height:h}});
    page.on('console', m => { if(m.type()==='error') console.log('CONSOLE ERR:', m.text().slice(0,200)); });
    page.on('requestfailed', r => console.log('REQ FAIL:', r.url().slice(0,90)));
    await page.addInitScript(() => { window.__NO_AUTOPLAY = true; });
  await page.goto('file://' + process.cwd() + '/test_local.html');
    await page.waitForTimeout(6000);
    await page.screenshot({path:`shot_${name}.png`, fullPage:true});
    await page.close();
  }
  await browser.close();
})();
