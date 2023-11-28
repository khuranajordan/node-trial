const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

async function captureWebpage(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(url, { waitUntil: "domcontentloaded" });

  // Get the total height of the page
  const bodyHandle = await page.$("body");
  const { height } = await bodyHandle.boundingBox();
  await bodyHandle.dispose();

  // Set the viewport size to 1920x1024
  await page.setViewport({ width: 1920, height: 1024 });

  // Create a directory to save screenshots if it doesn't exist
  const screenshotDirectory = path.join(__dirname, "screenshots");
  if (!fs.existsSync(screenshotDirectory)) {
    fs.mkdirSync(screenshotDirectory);
  }

  // Capture each fold and save it with a unique name
  const scrollStep = 500; // Adjust as needed
  let foldNumber = 1;
  for (let scrollTop = 0; scrollTop < height; scrollTop += scrollStep) {
    await page.evaluate((scrollTop) => {
      window.scrollTo(0, scrollTop);
    }, scrollTop);
    // Capture screenshot here

    // Capture the fold
    const screenshotPath = path.join(
      screenshotDirectory,
      `Fold_${foldNumber}.png`
    );
    await page.screenshot({ path: screenshotPath });

    console.log(`Captured Fold ${foldNumber}: ${screenshotPath}`);
    foldNumber++;
  }

  await browser.close();
}

captureWebpage("https://www.promptsmith.co");
// captureWebpage("https://pythontutor.com/visualize.html#mode=edit");
