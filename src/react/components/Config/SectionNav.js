import React, { useEffect, useRef, useState } from 'react'
import { Nav, Form } from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faPenToSquare,
  faCheck,
  faTrashCan,
} from '@fortawesome/free-solid-svg-icons'

export default function SectionNav({ sectionName, setError }) {
  const [isSaved, setIsSaved] = useState(true)
  const [newName, setNewName] = useState(sectionName)
  const sectionRef = useRef(null)

  const handleSave = () => {
    window.eel.config_update_section_name(
      sectionName,
      newName,
    )(({ success, msg }) => {
      if (!success) {
        setIsSaved(false)
        setNewName(sectionName)
        setError(msg)
      } else {
        setIsSaved(true)
      }
    })
  }

  const handleDelete = () => {
    window.eel.config_delete_section(sectionName)(({ success, msg }) => {
      if (!success) {
        setError(msg)
      } else {
        setError(null)
      }
    })
  }

  useEffect(() => {
    if (!isSaved) return
    sectionRef.current.click()
  }, [isSaved])

  const handleEdit = () => {
    setIsSaved(false)
  }

  return (
    <>
      {isSaved && (
        <Nav.Item key={sectionName} className="config-section-item">
          <FontAwesomeIcon
            icon={faPenToSquare}
            onClick={handleEdit}
            size="xl"
            style={{ cursor: 'pointer', marginTop: '0.0em' }}
          />
          <Nav.Link
            className="config-section-link"
            eventKey={sectionName}
            ref={sectionRef}
          >
            {sectionName}
          </Nav.Link>
        </Nav.Item>
      )}
      {!isSaved && (
        <Nav.Item
          key={sectionName}
          style={{ display: 'flex', marginBottom: 10 }}
        >
          <FontAwesomeIcon
            icon={faCheck}
            onClick={handleSave}
            color="green"
            style={{
              marginTop: '0.3em',
              marginRight: '0.4em',
              cursor: 'pointer',
            }}
            size="xl"
          />
          <FontAwesomeIcon
            icon={faTrashCan}
            onClick={handleDelete}
            color="red"
            style={{
              marginTop: '0.3em',
              marginRight: '0.4em',
              cursor: 'pointer',
            }}
            size="xl"
          />

          <Form.Control
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSave()}
          />
        </Nav.Item>
      )}
    </>
  )
}
