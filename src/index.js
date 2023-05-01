import React from 'react'
import './guify/web/style/index.css'
import App from './guify/web/App'
import * as serviceWorker from './guify/web/serviceWorker'
import * as ReactDOMClient from 'react-dom/client'

const container = document.getElementById('root')
const root = ReactDOMClient.createRoot(container)

root.render(<App />)
serviceWorker.unregister()
window.addEventListener('beforeunload', () => {
  window.eel.close_python()
})
window.addEventListener('load', () => {
  let eelScript = document.getElementById('eel-script')
  console.log(eelScript)
  if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    // dev code
    eelScript.setAttribute('src', 'http://localhost:3001/eel.js')
  } else {
    eelScript.setAttribute('src', '/eel.js')
  }
})
