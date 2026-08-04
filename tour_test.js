const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:1400,height:1000}});
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + process.cwd() + '/test_local.html');
  await page.waitForTimeout(2000);
  await page.click('#playBtn');
  await page.waitForTimeout(4000);
  await page.screenshot({path:'tour_1.png', clip:{x:0,y:150,width:1400,height:850}});
  await page.click('#speedBtn'); await page.click('#speedBtn'); // 4x
  await page.waitForTimeout(16000);
  await page.screenshot({path:'tour_2.png', clip:{x:0,y:150,width:1400,height:850}});
  await page.waitForTimeout(14000);
  const ticker = await page.textContent('#ticker');
  const playTxt = await page.textContent('#playBtn');
  await page.screenshot({path:'tour_3.png', clip:{x:0,y:150,width:1400,height:850}});
  console.log('TICKER:', ticker); console.log('PLAYBTN:', playTxt);
  console.log('PAGE ERRORS:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})();
