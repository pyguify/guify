const fs = require('fs')
const cheerio = require('cheerio')

const html = fs.readFileSync('build/index.html', 'utf8')
const $ = cheerio.load(html)
$('#eel-script').attr('src', '/eel.js')
fs.writeFileSync('build/index.html', $.html())
