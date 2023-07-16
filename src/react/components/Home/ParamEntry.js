import Form from 'react-bootstrap/Form'
import { useEffect, useState } from 'react'

export default function ParamEntry({ workerState, name, paramValues }) {
  const [value, setValue] = useState(paramValues[name])

  useEffect(() => {
    setValue(paramValues[name])
  }, [paramValues])

  const onChange = (e) => {
    window.eel.set_param(name, e.target.value)()
  }

  const toTitleCase = (str) => {
    return str.replace(
      /\w\S*/g,
      (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    )
  }

  return (
    <Form.Control
      type="text"
      className="mb-2"
      name={name}
      placeholder={toTitleCase(name.replace('_', ' '))}
      key={name}
      disabled={workerState !== 'idle'}
      value={value}
      onChange={onChange}
    />
  )
}
