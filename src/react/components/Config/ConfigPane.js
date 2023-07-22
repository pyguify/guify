import React, { useEffect, useState } from 'react'
import { Button, Modal } from 'react-bootstrap'
import DataPair from './DataPair'

export default function ConfigPane({ eventKey, config, setError }) {
  const [configSection, setConfigSection] = useState(null)

  const sectionName = eventKey

  useEffect(() => {
    setConfigSection(config[sectionName])
  }, [config])

  const newRow = () => {
    window.eel.config_insert_row(sectionName)
  }

  return (
    <>
      {configSection &&
        Object.entries(configSection).map(([key, value]) => (
          <DataPair
            defaultKey={key}
            defaultValue={value}
            sectionName={sectionName}
            setError={setError}
          />
        ))}
      <Button variant="primary" onClick={(e) => newRow()}>
        +
      </Button>
    </>
  )
}
