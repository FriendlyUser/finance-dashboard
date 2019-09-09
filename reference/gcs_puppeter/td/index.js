/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
const puppeteer = require('puppeteer');
let page;

async function getBrowserPage() {
  // Launch headless Chrome. Turn off sandbox so Chrome can run under root.
  const browser = await puppeteer.launch({args: ['--no-sandbox']});
  return browser.newPage();
}


exports.screenshot = async (req, res) => {
  // const url = req.query.url;
  const url = "https://www.td.com/ca/en/asset-management/funds/solutions/mutual-funds/"

  if (!url) {
    return res.send('Please provide URL as GET parameter, for example: <a href="?url=https://example.com">?url=https://example.com</a>');
  }
  if (!page) {
    page = await getBrowserPage();
  }

  await page.goto(url);
  await page.waitFor(10000)
  const content = await page.content()
  res.set('Content-Type', 'application/json');
  res.send({"td_html": content});
};
