// Generate the 1200x630 Open Graph preview image (og-image.jpg) for WhatsApp unfurls.
// Run `python3 gen_og.py` first — it builds og.html (vector map, no network needed).
const launch = require('./pw_launch');
(async () => {
  const browser = await launch();
  const page = await browser.newPage({viewport:{width:1200,height:630}, deviceScaleFactor:1});
  await page.goto('file://' + process.cwd() + '/og.html');
  await page.waitForTimeout(1200);
  await page.screenshot({path:'og-image.jpg', type:'jpeg', quality:85});
  await browser.close();
  console.log('og-image.jpg written');
})();
