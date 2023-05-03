import React from 'react'
import Layout from './components/Layout'
import './style/bootstrap/bootstrap.min.css'
import './style/bootstrap/bootstrap-grid.min.css'
import './style/bootstrap/bootstrap-reboot.min.css'
import './style/App.css'
export const eel = window.eel

const App = () => {
  return <Layout />
}

window.eel.app_name()((r) => {
  document.title = r
})

// for some weird reason declaring this function
// inside the react component doesn't work
// so we declare it here:
function setMonitorText(text) {
  // the Monitor is the textarea on the right hand side.
  const monitor = document.getElementById('monitor-text')
  if (!monitor) return
  let currentScrollPosition =
    monitor.scrollTop - monitor.scrollHeight + monitor.clientHeight
  monitor.value = text
  if (currentScrollPosition > -20) {
    monitor.scrollTop = monitor.scrollHeight
  }
}
window.eel.expose(setMonitorText, 'set_text')

export default App
