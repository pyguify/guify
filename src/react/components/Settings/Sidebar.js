import { Form } from 'react-bootstrap'

export default function Sidebar() {
  return (
    <div>
      <Form.Label htmlFor="reportGeneration">Report Generation</Form.Label>
      <Form.Check
        type="switch"
        id="reportGeneration"
        label="Enable Report Generation"
      />
    </div>
  )
}
