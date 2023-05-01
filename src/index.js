import React from 'react'
import './react/style/index.css'
import App from './react/App'
import * as serviceWorker from './react/serviceWorker'
import * as ReactDOMClient from 'react-dom/client'

if (process.env.NODE_ENV === 'development') {
  window.eel.set_host('ws://localhost:3001')
}

const container = document.getElementById('root')
const root = ReactDOMClient.createRoot(container)

root.render(<App />)

serviceWorker.unregister()
window.addEventListener('beforeunload', () => {
  window.eel.close_python()
})
