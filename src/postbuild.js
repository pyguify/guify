const fs = require('fs')
const cheerio = require('cheerio')

const html = fs.readFileSync('build/index.html', 'utf8')
const $ = cheerio.load(html)
$('#eel-script').attr('src', '/eel.js')
fs.writeFileSync('build/index.html', $.html())

var oldPath = 'build'
var newPath = 'src/guify/web'

fs.rmSync(newPath, { recursive: true, force: true })

fs.rename(oldPath, newPath, function (err) {
  if (err) throw err
  console.log('Successfully renamed - AKA moved!')
})
