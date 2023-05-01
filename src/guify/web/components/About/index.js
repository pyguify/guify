import { Card, Col } from 'react-bootstrap'
export default function AboutTab() {
  return (
    <Card id="about" style={{ maxWidth: 600, marginTop: 80 }}>
      <Card.Header>About</Card.Header>
      <Card.Body>
        <Card.Text>
          This is a simple framework for writing sequence tests in python <br />
          Tests are defined in python under test_scripts directory
          <br />
          Tests are run in a separate process
          <br />
          Tests cant be run in parallel,
          <br />
          available by web browser from remote machine on:
          <a href="http://localhost:8080/">localhost:8080</a>
        </Card.Text>
      </Card.Body>
      <Card.Footer>
        <span>
          <small>Made by Michael Druyan</small>
        </span>
      </Card.Footer>
    </Card>
  )
}
