const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/fridge.html');
  await page.waitForTimeout(1200);
  await page.pdf({path:'South_Island_Safari_Fridge_Map.pdf', width:'297mm', height:'210mm', printBackground:true, pageRanges:'1'});
  await browser.close();
})();
