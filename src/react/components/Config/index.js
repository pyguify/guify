import React, { useEffect, useState } from 'react'
import SideBar from './SideBar'
import { Button, Modal } from 'react-bootstrap'

export default function ConfigTab() {
  const [error, setError] = useState(null)
  return (
    <>
      <Modal show={error} onHide={() => setError(null)}>
        <Modal.Header>
          <Modal.Title>Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>{error}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setError(null)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
      <SideBar setError={setError} />
    </>
  )
}
