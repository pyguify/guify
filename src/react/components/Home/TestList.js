import React from 'react'
import ListGroup from 'react-bootstrap/ListGroup'
import { useState, useEffect } from 'react'
import Form from 'react-bootstrap/Form'
import Container from 'react-bootstrap/Container'
import { eel } from '../../App'

const RUNNING = 'running'
const PENDING = 'pending'
const IDLE = 'idle'

export default function TestList() {
  const [tests, setTests] = useState([])
  const [queue, setQueue] = useState([])
  const [workerStatus, setWorkerStatus] = useState(IDLE)
  const [currentJob, setCurrentJob] = useState('')

  const updateQueue = () => {
    eel.worker_status()(({ queue, state, currentJob }) => {
      setQueue(queue)
      setWorkerStatus(state)
      setCurrentJob(currentJob)
    })
  }

  useEffect(() => {
    eel.all_tests()(({ tests }) => setTests(tests))
  }, [])

  useEffect(() => {
    updateQueue()
    setInterval(updateQueue, 1000)
  }, [])

  return (
    <Container id="test-list">
      <ListGroup>
        <form id="test-list-form">
          {tests.map(({ name, requiredParams, description, verbose_name }) => (
            <ListGroup.Item
              key={name}
              className={currentJob === name ? workerStatus : ''}
            >
              <Form.Check type="switch" id={name}>
                <Form.Check.Label>
                  <Form.Check.Input
                    type="checkbox"
                    className="test-checkbox"
                    name={name}
                    {...(workerStatus !== 'idle' && {
                      checked: queue.includes(name),
                    })}
                  />
                  <span>
                    {verbose_name ? verbose_name : name}
                    <small className="d-block text-body-secondary">
                      {description}
                    </small>
                  </span>
                </Form.Check.Label>
              </Form.Check>
            </ListGroup.Item>
          ))}
        </form>
      </ListGroup>
    </Container>
  )
}
