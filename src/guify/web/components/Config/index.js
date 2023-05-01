import React, { useEffect, useState } from 'react'
import ConfigPane from './ConfigPane'
import SideBar from './SideBar'
import { Button } from 'react-bootstrap'

export default function ConfigTab() {
  const [config, setConfig] = useState(null)

  useEffect(() => {
    window.eel.get_config()(({ config }) => {
      setConfig(config)
    })
  }, [])

  const updateConfig = (section, key, value) => {
    const newConfig = { ...config }
    if (!newConfig[section]) {
      newConfig[section] = {}
    }
    newConfig[section][key] = value
    setConfig(newConfig)
    saveConfig()
  }

  const saveConfig = () => {
    window.eel.save_config(config)(() => {
      window.eel.get_config()(({ config }) => {
        setConfig(config)
      })
    })
  }
  return (
    <>
      <SideBar
        config={config}
        setConfig={setConfig}
        updateConfig={updateConfig}
        saveConfig={saveConfig}
      />
      <Button variant="primary" id="config-save-button" onClick={saveConfig}>
        Save
      </Button>
    </>
  )
}
