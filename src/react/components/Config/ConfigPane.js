import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'
import Tab from 'react-bootstrap/Tab'
import React, { useEffect, useState } from 'react'

export default function ConfigPane({ configSection, handleChange }) {
  return (
    <>
      {configSection &&
        Object.entries(configSection).map(([key, value]) => (
          <InputGroup
            className="mb-3"
            key={key}
            style={{ width: '40vw', maxWidth: 800, minWidth: 400 }}
          >
            <InputGroup.Text
              id={key}
              style={{ width: '50%', justifyContent: 'center' }}
            >
              {key}
            </InputGroup.Text>
            <Form.Control
              type="text"
              aria-label={key}
              aria-describedby={key}
              defaultValue={value}
              onChange={(e) => handleChange(key, e.target.value)}
            />
          </InputGroup>
        ))}
    </>
  )
}
