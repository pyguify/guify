import React, { useState, useMemo, useEffect } from 'react'
import { Container, Button, Modal } from 'react-bootstrap'
import TestList from './TestList'
import ParamList from './ParamList'
import Monitor from './Monitor'
import WorkerStatus from './WorkerStatus'
import { eel } from '../../App'

export default function HomeTab() {
  const workerStates = useMemo(() => {
    return {
      idle: 'idle',
      running: 'running',
      pending: 'pending',
      done: 'done',
    }
  }, [])
  const [error, setError] = useState(null)
  const [workerState, setWorkerState] = useState(workerStates.idle)
  const [currentJob, setCurrentJob] = useState(null)
  const [promptText, setPromptText] = useState(null)
  const [promptTitle, setPromptTitle] = useState(null)
  const [queue, setQueue] = useState([])

  const setPrompt = (title, msg) => {
    setPromptTitle(title)
    setPromptText(msg)
  }

  eel.expose(setWorkerState, 'set_state')
  eel.expose(setCurrentJob, 'set_current_job')
  eel.expose(setPrompt, 'prompt')
  eel.expose(setQueue, 'set_queue')

  useEffect(() => {
    eel.get_state()(setWorkerState)
    eel.get_current_job()(setCurrentJob)
    eel.get_queue()(setQueue)
    eel.get_prompt()(setPrompt)
  }, [])

  const handleClose = () => setError(null)
  const getParams = () => {
    const params = {}
    const form = document.getElementById('params-form')
    for (const element of form.elements) {
      if (element.name && element.value !== '') {
        params[element.name] = element.value
      }
    }
    return params
  }

  const getTests = () => {
    const tests = []
    const form = document.getElementById('test-list-form')
    const checkboxes = form.querySelectorAll('input[type="checkbox"]')
    for (const checkbox of checkboxes) {
      if (checkbox.checked) {
        tests.push(checkbox.name)
      }
    }
    return tests
  }

  const runTests = () => {
    const params = getParams()
    const tests = getTests()

    eel.run_tests(
      tests,
      params,
    )(function (result) {
      if (result.error) {
        setError(result.error)
      }
    })
  }

  return (
    <>
      <Modal show={Boolean(error)} onHide={handleClose}>
        <Modal.Header>
          <Modal.Title>Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>{error}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
      <Container
        className="flex-column"
        style={{ maxHeight: 'calc(100vh-80px)' }}
      >
        <TestList
          id="test-list"
          workerState={workerState}
          currentJob={currentJob}
          queue={queue}
        />
        <ParamList id="param-list" workerState={workerState} />
        <WorkerStatus
          workerState={workerState}
          workerStates={workerStates}
          currentJob={currentJob}
          promptText={promptText}
          promptTitle={promptTitle}
          setPrompt={setPrompt}
        />
        <Button onClick={runTests} id="run-tests-button">
          Run Tests
        </Button>
      </Container>
      <Container className="flex-column">
        <Monitor />
      </Container>
    </>
  )
}
