import React from 'react'
import ListGroup from 'react-bootstrap/ListGroup'
import { useState, useEffect } from 'react'
import Form from 'react-bootstrap/Form'
import Container from 'react-bootstrap/Container'
import { eel } from '../../App'

export default function TestSection({
  workerState,
  currentJob,
  name,
  verbose_name,
  description,
  queue,
}) {
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    setChecked(queue.includes(name))
  }, [queue])

  const handleClick = (event) => {
    event.preventDefault()
    const { name, checked } = event.target
    if (checked) {
      eel.add_to_queue(name)()
    } else {
      eel.remove_from_queue(name)()
    }
  }

  return (
    <ListGroup.Item
      key={name}
      className={currentJob === name ? workerState : ''}
    >
      <Form.Check type="switch" id={name}>
        <Form.Check.Label>
          <Form.Check.Input
            type="checkbox"
            className="test-checkbox"
            name={name}
            onClick={handleClick}
            checked={checked}
            disabled={workerState !== 'idle'}
          />
          <span>
            {verbose_name ? verbose_name : name}
            <small className="d-block text-body-secondary">{description}</small>
          </span>
        </Form.Check.Label>
      </Form.Check>
    </ListGroup.Item>
  )
}
