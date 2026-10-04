const launch = require('./pw_launch');
(async () => {
  const browser = await launch();
  const page = await browser.newPage({viewport:{width:1400,height:1000}});
  await page.goto('file://' + process.cwd() + '/test_local.html');
  await page.waitForTimeout(2500);
  // click Arthur's Pass 2 row (combined pin) 
  await page.locator('.row').nth(7).click();
  await page.waitForTimeout(1800);
  await page.screenshot({path:'shot_popup_ap.png'});
  // click Reefton row
  await page.locator('.row').nth(0).click();
  await page.waitForTimeout(1800);
  await page.screenshot({path:'shot_popup_reefton.png'});
  await browser.close();
})();
