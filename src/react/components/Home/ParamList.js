import Form from 'react-bootstrap/Form'
import Container from 'react-bootstrap/Container'
import { useEffect, useMemo, useState } from 'react'
const eel = window.eel
export default function ParamList(props) {
  const [params, setParams] = useState([])
  const [paramValues, setParamValues] = useState({})
  const [workerStatus, setWorkerStatus] = useState('idle')

  const updateStatus = () => {
    eel.worker_status()(({ state, params }) => {
      if (state !== workerStatus) {
        setWorkerStatus(state)
      }
      setWorkerStatus(state)
      setParamValues(params)
    })
  }

  useEffect(() => {
    setInterval(updateStatus, 1000)
  }, [])

  useEffect(() => {
    eel.all_params()((p) => {
      setParams(p.params)
    })
  }, [setParams])

  const toTitleCase = (str) => {
    return str.replace(
      /\w\S*/g,
      (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    )
  }

  return (
    <Container id="params">
      <form id="params-form">
        {params &&
          params.map((param) => (
            <Form.Control
              type="text"
              className="mb-2"
              name={param}
              placeholder={toTitleCase(param.replace('_', ' '))}
              key={param}
              disabled={workerStatus !== 'idle'}
              {...(workerStatus !== 'idle' && { value: paramValues[param] })}
            />
          ))}
      </form>
    </Container>
  )
}
