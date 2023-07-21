import Form from 'react-bootstrap/Form'
import Container from 'react-bootstrap/Container'
import { useEffect, useMemo, useState } from 'react'
import ParamEntry from './ParamEntry'
export default function ParamList({ workerState }) {
  const [params, setParams] = useState([])
  const [paramValues, setParamValues] = useState({})

  window.eel.expose(setParamValues, 'update_params')

  const updateParams = (params) => {
    setParams(params.sort())
  }
  window.eel.expose(updateParams, 'update_param_list')

  useEffect(() => {
    window.eel.all_params()(({ params }) => {
      setParams(params.sort())
    })
    window.eel.get_params()((p) => {
      setParamValues(p)
    })
  }, [])
  return (
    <Container id="params">
      <form id="params-form">
        {params &&
          params.map((param) => (
            <ParamEntry
              key={param}
              name={param}
              paramValues={paramValues}
              workerState={workerState}
              updateParams={setParamValues}
            />
          ))}
      </form>
    </Container>
  )
}
