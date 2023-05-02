const fs = require('fs')
const cheerio = require('cheerio')


// we need to open the built index.html and change the 
// src of #eel-script to /eel.js instead of http://localhost:3001/eel.js
// which will be eel's python development server
// this is necessary because the python server will be running
// on a different port than the react development server
// after building the package we will be serving the react app
// from the python server
const html = fs.readFileSync('build/index.html', 'utf8')
const $ = cheerio.load(html)

// change the src of #eel-script to /eel.js
$('#eel-script').attr('src', '/eel.js')
fs.writeFileSync('build/index.html', $.html())


// replace the build folder with the src/guify/web folder
// it is necessary when building the package, because the
// built react app must be contained within the library.
var oldPath = 'build'
var newPath = 'src/guify/web'

// remove the old folder
fs.rmSync(newPath, { recursive: true, force: true })

// rename the build folder to src/guify/web
fs.rename(oldPath, newPath, function (err) {
  if (err) throw err
  console.log('Successfully moved!')
})
