// Mobile-viewport tour check: play → reset mid-tour → replay from scratch → run to end.
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:390,height:844}});
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + process.cwd() + '/test_local.html');
  await page.waitForTimeout(2000);

  await page.click('#playBtn');
  await page.waitForTimeout(2500);
  await page.click('#resetBtn');                       // reset mid-tour
  const afterReset = await page.textContent('#playBtn');
  const speedVisible = await page.isVisible('#speedBtn');
  const tickerVisible = await page.isVisible('#ticker');
  const vans = await page.locator('.vanicon').count();

  await page.click('#playBtn');                        // replay from scratch
  await page.click('#speedBtn'); await page.click('#speedBtn'); // 4x
  await page.waitForTimeout(32000);
  const ticker = await page.textContent('#ticker');
  const playTxt = await page.textContent('#playBtn');
  await page.screenshot({path:'shot_mobile_tour.png', fullPage:false});

  console.log('AFTER RESET btn:', afterReset, '| speed visible:', speedVisible, '| ticker visible:', tickerVisible, '| vans:', vans);
  console.log('END TICKER:', ticker);
  console.log('END PLAYBTN:', playTxt);
  console.log('PAGE ERRORS:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})();
