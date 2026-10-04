// Render the T-shirt mock-up (3 × A4 landscape) and the print-ready back artwork (300 × 400 mm) to PDF,
// plus PNG previews of the mock-up pages. Run `python3 gen_tshirt.py` first.
const launch = require('./pw_launch');
const path = require('path');
(async () => {
  const browser = await launch();
  const dir = path.join(process.cwd(), 'tshirt');
  const page = await browser.newPage({viewport:{width:1123,height:794}, deviceScaleFactor:1.5});
  await page.goto('file://' + path.join(dir, 'mockup.html'));
  await page.waitForTimeout(1200);
  await page.pdf({path: path.join(dir, 'South_Island_Safari_Tshirt_Mockup.pdf'), width:'297mm', height:'210mm', printBackground:true});
  const pages = await page.locator('.page').all();
  const names = ['mockup_navy_tee.png', 'mockup_sand_tee.png', 'mockup_print_spec.png'];
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({path: path.join(dir, names[i])});
  for (const key of ['navy_tee', 'sand_tee']) {
    await page.goto('file://' + path.join(dir, `back_artwork_${key}.html`));
    await page.waitForTimeout(800);
    await page.pdf({path: path.join(dir, `back_artwork_${key}.pdf`), width:'300mm', height:'400mm', printBackground:true, pageRanges:'1'});
  }
  await browser.close();
  console.log('tshirt/ PDFs + PNG previews written');
})();
