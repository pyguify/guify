import React from 'react'
import ListGroup from 'react-bootstrap/ListGroup'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'

export default function WorkerStatus({
  workerState,
  workerStates,
  currentJob,
  promptText,
  promptTitle,
  setPrompt,
}) {
  const answerOk = () => {
    window.eel.answer_prompt('ok')(() => {
      console.log('answered prompt')
      setPrompt(null)
    })
  }
  const answerCancel = () => {
    window.eel.answer_prompt('cancel')(() => {
      console.log('answered prompt')
      setPrompt(null)
    })
  }

  const statusVariant = () => {
    switch (workerState) {
      case workerStates.idle:
        return 'secondary'
      case workerStates.running:
        return 'primary'
      case workerStates.pending:
        return 'warning'
      case workerStates.done:
        return 'info'
      default:
        return 'secondary'
    }
  }

  return (
    <>
      <Modal show={promptText} backdrop="static" keyboard={false}>
        <Modal.Header>
          <Modal.Title>{promptTitle}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{promptText}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={answerCancel}>
            Cancel
          </Button>
          <Button variant="primary" onClick={answerOk}>
            OK
          </Button>
        </Modal.Footer>
      </Modal>

      <ListGroup id="worker-status" horizontal>
        <ListGroup.Item variant={statusVariant()}>
          Status: {workerState}
        </ListGroup.Item>
        <ListGroup.Item variant={statusVariant()}>
          Current Job: {!currentJob && 'None'} {currentJob}
        </ListGroup.Item>
      </ListGroup>
    </>
  )
}
