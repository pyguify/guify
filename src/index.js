import React from 'react'
import './react/style/index.css'
import App from './react/App'
import * as serviceWorker from './react/serviceWorker'
import * as ReactDOMClient from 'react-dom/client'

if (process.env.NODE_ENV === 'development') {
  // The host is set by eel.js (which is served by python)
  // and the default host is the host of the page that loads eel.js
  // so we need to set the host to the python server
  window.eel.set_host('ws://localhost:3001')
  // NOTE: in the postbuild.js we change the src of 
  // #eel-script to /eel.js
}

const container = document.getElementById('root')
const root = ReactDOMClient.createRoot(container)

root.render(<App />)



// eel's service worker
serviceWorker.unregister()
window.addEventListener('beforeunload', () => {
  window.eel.close_python()
})
