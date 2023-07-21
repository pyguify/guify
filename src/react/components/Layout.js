import React from 'react'
import { Tab, Tabs } from 'react-bootstrap'
import { useState } from 'react'
import HomeTab from './Home'
import WorkerStatus from './Home/WorkerStatus'
import AboutTab from './About'
import ConfigTab from './Config'
import SettingsTab from './Settings'

export default function Layout() {
  return (
    <div id="layout">
      <Tabs defaultActiveKey="home">
        <Tab eventKey="home" title="Home" style={{ maxHeight: "calc(100vh - 60px)"}}>
          <HomeTab />
        </Tab>
        <Tab eventKey="config" title="Config" style={{flexDirection: "column"}}>
          <ConfigTab />
        </Tab>
        <Tab eventKey="settings" title="Settings">
          <SettingsTab />
        </Tab>
        <Tab eventKey="about" title="About">
          <AboutTab />
        </Tab>
      </Tabs>
    </div>
  ) // prettier-ignore
}
