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

