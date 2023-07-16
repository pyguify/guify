import React, { useEffect, useState } from 'react'

export default function Monitor(props) {
  const [monitorText, setMonitorText] = useState('')
  useEffect(() => {
    window.eel.get_monitor_text()(setMonitorText)
  }, [])
  window.eel.expose(setMonitorText, 'set_monitor_text')
  return (
    <div className="container" id="monitor">
      <textarea id="monitor-text" disabled value={monitorText} />
    </div>
  )
}
