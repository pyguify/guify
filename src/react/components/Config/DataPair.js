import InputGroup from 'react-bootstrap/InputGroup'
import React, { useEffect, useRef, useState } from 'react'
import { Form } from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faPlus,
  faFloppyDisk,
  faTrash,
} from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
library.add(faPlus, faFloppyDisk, faTrash)
export default function DataPair({
  defaultKey,
  defaultValue,
  sectionName,
  setError,
}) {
  const [isSaved, setIsSaved] = useState(true)
  const [key, setKey] = useState(defaultKey)
  const [value, setValue] = useState(defaultValue)

  useEffect(() => {
    setKey(defaultKey)
    setValue(defaultValue)
  }, [defaultKey, defaultValue])

  const updateKey = async (oldKey, newKey) => {
    window.eel.config_update_key(
      sectionName,
      oldKey,
      newKey,
    )(({ success, msg }) => {
      if (!success) {
        setIsSaved(false)
        setKey(oldKey)
        setError(msg)
      } else {
        setError(null)
      }
    })
  }

  const valueRef = useRef(null)

  const updateValue = async (key, value) => {
    window.eel.config_update_value(
      sectionName,
      key,
      value,
    )(() => setIsSaved(true))
  }

  const handleChangeKey = (e) => {
    setKey(e.target.value)
    setIsSaved(false)
  }

  const handleChangeValue = (e) => {
    setValue(e.target.value)
    setIsSaved(false)
  }

  const handleSave = async () => {
    await updateKey(defaultKey, key)
    await updateValue(key, value)
    setIsSaved(true)
  }

  const handleDelete = () => {
    window.eel.config_delete_row(sectionName, key)()
  }

  return (
    <div className="data-pair">
      <InputGroup
        className="mb-3"
        key={defaultKey}
        style={{
          width: '40vw',
          maxWidth: 800,
          minWidth: 400,
        }}
      >
        <Form.Control
          id={defaultKey}
          style={{ justifyContent: 'center' }}
          value={key}
          onChange={handleChangeKey}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === 'Tab') {
              handleSave().then(() => {
                setTimeout(() => {
                  valueRef.current.focus()
                }, 100)
              })
            }
          }}
        />

        <Form.Control
          type="text"
          aria-label={defaultKey}
          aria-describedby={defaultKey}
          value={value}
          onChange={handleChangeValue}
          ref={valueRef}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === 'Tab') {
              handleSave()
            }
          }}
        />
      </InputGroup>
      {!isSaved && (
        <FontAwesomeIcon
          style={{
            marginBottom: '1rem',
            marginLeft: '1rem',
            cursor: 'pointer',
          }}
          size="xl"
          icon={faFloppyDisk}
          onClick={handleSave}
        />
      )}
      <FontAwesomeIcon
        style={{ marginBottom: '1rem', marginLeft: '1rem', cursor: 'pointer' }}
        size="xl"
        icon={faTrash}
        color="#a32014"
        onClick={handleDelete}
      />
    </div>
  )
}
