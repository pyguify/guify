import React, { useEffect, useState } from 'react'
import { Nav, Container, Tab } from 'react-bootstrap'
import ConfigPane from './ConfigPane'

export default function SideBar({ config, updateConfig, setConfig }) {
  const [defaultTab, setDefaultTab] = useState(null)
  useEffect(() => {
    console.log('test')
    if (config) {
      setDefaultTab(Object.keys(config)[0])
    }
  }, [config && Object.keys(config)[0]])

  return (
    <div style={{ display: 'flex', flexDirection: 'row' }}>
      <Tab.Container>
        <Container id="config-sidebar" style={{ maxWidth: 400 }}>
          <Nav variant="pills" className="flex-column" activeKey={defaultTab}>
            {config &&
              Object.keys(config).map((section_name) => (
                <Nav.Item key={section_name}>
                  <Nav.Link eventKey={section_name}>{section_name}</Nav.Link>
                </Nav.Item>
              ))}
          </Nav>
        </Container>
        <hr />
        <Container id="config-tab-pane">
          <Tab.Content>
            {config &&
              Object.entries(config).map(([section_name, section]) => (
                <Tab.Pane
                  key={section_name}
                  eventKey={section_name}
                  className="flex-column"
                >
                  <ConfigPane
                    eventKey={section_name}
                    configSection={section}
                    handleChange={(key, value) => {
                      updateConfig(section_name, key, value)
                    }}
                  />
                </Tab.Pane>
              ))}
          </Tab.Content>
        </Container>
      </Tab.Container>
    </div>
  )
}
