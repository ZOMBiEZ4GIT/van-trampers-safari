const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:1400,height:1000}});
  await page.goto('file://' + process.cwd() + '/test_local.html');
  await page.waitForTimeout(2000);
  await page.click('#playBtn');
  await page.click('#speedBtn'); await page.click('#speedBtn'); // 4x
  await page.waitForTimeout(30000); // run to completion
  await page.keyboard.press('Escape');
  await page.evaluate(()=>{ document.querySelector('.leaflet-popup-close-button')?.dispatchEvent(new MouseEvent('click',{bubbles:true})); });
  await page.waitForTimeout(800);
  await page.screenshot({path:'tour_end.png', clip:{x:0,y:150,width:980,height:850}});
  await browser.close();
})();
