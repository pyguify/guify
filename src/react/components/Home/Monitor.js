import React, { useEffect, useRef, useState } from 'react'

export default function Monitor(props) {
  const [monitorText, setMonitorText] = useState('')
  const [autoScroll, setAutoScroll] = useState(true)

  useEffect(() => {
    window.eel.get_monitor_text()(setMonitorText)
  }, [])

  useEffect(() => {
    let monitor = document.getElementById('monitor-text')
    if (monitor && autoScroll) {
      monitor.scrollTop = monitor.scrollHeight
    }
  }, [monitorText, autoScroll])

  const handleScroll = (e) => {
    const monitor = e.target
    let currentScrollPosition =
      monitor.scrollTop - monitor.scrollHeight + monitor.clientHeight
    if (currentScrollPosition > -120) {
      setAutoScroll(true)
    } else {
      setAutoScroll(false)
    }
  }
  window.eel.expose(setMonitorText, 'set_monitor_text')
  return (
    <div className="container" id="monitor">
      <textarea
        id="monitor-text"
        disabled
        value={monitorText}
        onScroll={handleScroll}
      />
    </div>
  )
}
