import React, { useEffect } from 'react'
import { useState, useMemo } from 'react'
import ListGroup from 'react-bootstrap/ListGroup'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import { eel } from '../../App'

export default function WorkerStatus() {
  const statuses = useMemo(() => {
    return {
      idle: 'idle',
      running: 'running',
      pending: 'pending',
      done: 'done',
    }
  }, [])

  const [status, setStatus] = useState(statuses.idle)
  const [currentJob, setCurrentJob] = useState(null)
  const [prompt, setPrompt] = useState(null)

  const updateStatus = () => {
    eel.worker_status()((r) => {
      if (r.state !== status) {
        setStatus(r.state)
      }
      if (currentJob !== r.currentJob) {
        setCurrentJob(r.currentJob)
      }
      if (prompt !== r.prompt) {
        setPrompt(r.prompt)
      }
    })
  }

  useEffect(() => {
    setInterval(updateStatus, 1000)
  }, [updateStatus])

  const answerPrompt = (answer) => {
    return () => {
      eel.answer_prompt(answer)
      setPrompt(null)
    }
  }

  const statusVariant = () => {
    if (status === statuses.idle) {
      return 'secondary'
    } else if (status === statuses.running) {
      return 'primary'
    } else if (status === statuses.pending) {
      return 'warning'
    } else if (status === statuses.done) {
      return 'info'
    }
  }

  return (
    <>
      <Modal show={prompt} backdrop="static" keyboard={false}>
        <Modal.Header>
          <Modal.Title>Please Confirm</Modal.Title>
        </Modal.Header>
        <Modal.Body>{prompt}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={answerPrompt('cancel')}>
            Cancel
          </Button>
          <Button variant="primary" onClick={answerPrompt('ok')}>
            OK
          </Button>
        </Modal.Footer>
      </Modal>

      <ListGroup id="worker-status" horizontal>
        <ListGroup.Item variant={statusVariant()}>
          Status: {status}
        </ListGroup.Item>
        <ListGroup.Item variant={statusVariant()}>
          Current Job: {!currentJob && 'None'} {currentJob}
        </ListGroup.Item>
      </ListGroup>
    </>
  )
}
