import React, { useEffect, useState } from 'react'
import { Nav, Container, Tab, Button } from 'react-bootstrap'
import ConfigPane from './ConfigPane'
import SectionNav from './SectionNav'

export default function SideBar({ setError }) {
  const [config, setConfig] = useState(null)

  const refreshConfig = () => {
    window.eel.get_config()((cfg) => {
      setConfig(cfg)
    })
  }

  window.eel.expose(refreshConfig, 'refresh_config')

  const addSection = () => {
    window.eel.config_add_section('new_section')(() => {
      refreshConfig()
    })
  }

  useEffect(() => {
    refreshConfig()
  }, [])

  return (
    <div style={{ display: 'flex', flexDirection: 'row' }}>
      <Tab.Container>
        <Container id="config-sidebar" style={{ maxWidth: 400 }}>
          <Nav
            variant="pills"
            className="flex-column"
            activeKey=""
            style={{
              flexWrap: 'nowrap',
              justifyContent: 'flex-start',
              overflowY: 'scroll',
              height: '94%',
            }}
          >
            {config &&
              Object.keys(config).map((sectionName) => (
                <SectionNav
                  key={sectionName}
                  sectionName={sectionName}
                  setError={setError}
                />
              ))}
          </Nav>
          <Button
            style={{ position: 'absolute', bottom: 30 }}
            onClick={addSection}
          >
            + Add Section
          </Button>
        </Container>
        <hr />
        <Container id="config-tab-pane">
          <Tab.Content>
            {config &&
              Object.keys(config).map((sectionName) => (
                <Tab.Pane
                  key={sectionName}
                  eventKey={sectionName}
                  className="flex-column"
                >
                  <ConfigPane
                    eventKey={sectionName}
                    config={config}
                    setError={setError}
                  />
                </Tab.Pane>
              ))}
          </Tab.Content>
        </Container>
      </Tab.Container>
    </div>
  )
}
