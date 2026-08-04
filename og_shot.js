// Generate the 1200x630 Open Graph preview image (og-image.jpg) for WhatsApp unfurls.
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:1200,height:630}, deviceScaleFactor:1});
  await page.addInitScript(() => { window.__NO_AUTOPLAY = true; });
  await page.goto('file://' + process.cwd() + '/test_local.html');
  await page.waitForTimeout(5000); // pins dropped, coastline drawn
  await page.evaluate(() => {
    // trim chrome that wastes preview space
    document.querySelector('.frame').style.padding = '0';
    document.querySelector('.board').style.borderRadius = '0';
  });
  await page.waitForTimeout(400);
  await page.screenshot({path:'og-image.jpg', type:'jpeg', quality:82});
  await browser.close();
  console.log('og-image.jpg written');
})();
