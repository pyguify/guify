import React, { useEffect, useState } from 'react'
import { eel } from '../../App'

export default function Monitor(props) {
  const [monitorText, setMonitorText] = useState('')
  useEffect(() => {
    eel.get_monitor_text()(setMonitorText)
  }, [])
  eel.expose(setMonitorText, 'set_monitor_text')
  return (
    <div className="container" id="monitor">
      <textarea id="monitor-text" disabled value={monitorText} />
    </div>
  )
}
