const puppeteer = require('puppeteer');

(async () => {
  // Launch browser
  const browser = await puppeteer.launch({ headless: true });
