import React from 'react'
import ListGroup from 'react-bootstrap/ListGroup'
import { useState, useEffect } from 'react'
import Form from 'react-bootstrap/Form'
import Container from 'react-bootstrap/Container'
import TestSection from './TestSection'
import { eel } from '../../App'

export default function TestList({ workerState, currentJob, queue }) {
  const [tests, setTests] = useState([])

  useEffect(() => {
    eel.all_tests()(({ tests }) => setTests(tests))
  }, [])

  return (
    <Container id="test-list">
      <ListGroup>
        <form id="test-list-form">
          {tests.map(({ name, description, verbose_name }) => (
            <TestSection
              key={name}
              name={name}
              description={description}
              verbose_name={verbose_name}
              workerState={workerState}
              currentJob={currentJob}
              queue={queue}
            />
          ))}
        </form>
      </ListGroup>
    </Container>
  )
}
