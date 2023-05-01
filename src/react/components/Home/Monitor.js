import React, { useEffect, useMemo } from 'react'
import { eel } from '../../App'

export default function Monitor(props) {
  const poll = useMemo(() => {
    return () => {
      const monitor = document.getElementById('monitor-text')
      if (!monitor) return
      eel.get_monitor_text()((text) => {
        let currentScrollPosition =
          monitor.scrollTop - monitor.scrollHeight + monitor.clientHeight

        monitor.value = text

        if (currentScrollPosition > -20) {
          monitor.scrollTop = monitor.scrollHeight
        }
      })
    }
  }, [])
  useEffect(() => {
    poll()
  }, [poll])
  return (
    <div className="container" id="monitor">
      <textarea id="monitor-text" disabled />
    </div>
  )
}
