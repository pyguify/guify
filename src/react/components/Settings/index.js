import React, { useState, useEffect } from 'react'
import {
  Container,
  Form,
  OverlayTrigger,
  Popover,
  Button,
} from 'react-bootstrap'

export default function Settings() {
  const [disabled, setDisabled] = useState(true)
  const [reportGeneration, setReportGeneration] = useState(false)
  const [reportDir, setReportDir] = useState('')
  const [reportFilename, setReportFilename] = useState('')
  const [timeout, setTimeout] = useState()

  useEffect(() => {
    updateSettings()
  }, [])

  useEffect(() => {
    if (!reportGeneration) {
      setReportDir('')
    } else {
      window.eel.get_settings()(({ reports }) => {
        setReportDir(reports.reports_dir)
      })
    }
  }, [reportGeneration])

  const updateSettings = () => {
    window.eel.get_settings()(({ reports }) => {
      setReportDir(reports.reports_dir)
      setReportGeneration(reports.reports_dir !== '')
      setReportFilename(reports.report_prefix)
      setDisabled(false)
    })
  }

  const filenamePopover = (props) => (
    <Popover id="report-filename-tooltip" {...props}>
      <Popover.Header as="h3">Report Filename</Popover.Header>
      <Popover.Body>
        The variable which will be taken from the passed parameters and used as
        the filename for the report. If the variable is not defined, the report
        will be named "report.html".
      </Popover.Body>
    </Popover>
  )

  const reportDirPopover = (props) => (
    <Popover id="report-directory-tooltip" {...props}>
      <Popover.Header as="h3">Report Directory</Popover.Header>
      <Popover.Body>The directory where the report will be saved</Popover.Body>
    </Popover>
  )

  const handleSave = () => {
    var newConfig = {
      reports: {
        reports_dir: reportDir,
        report_prefix: reportFilename,
      },
    }
    window.eel.set_settings(newConfig)()
    updateSettings()
  }

  return (
    <div>
      <h1>Settings</h1>
      <Container>
        <Form.Label htmlFor="reportGeneration">Report Generation</Form.Label>
        <Form.Check
          type="switch"
          id="reportGeneration"
          label="Enable Report Generation"
          disabled={disabled}
          checked={reportGeneration}
          onChange={(e) => {
            setReportGeneration(e.target.checked)
          }}
        />
        <br />
        <Form.Label htmlFor="report-directory">Report Directory</Form.Label>
        <OverlayTrigger
          placement="right"
          delay={{ show: 250, hide: 400 }}
          overlay={reportDirPopover}
        >
          <Form.Control
            type="text"
            id="report-directory"
            disabled={disabled || !reportGeneration}
            value={reportDir}
            onChange={(e) => {
              setReportDir(e.target.value)
            }}
          />
        </OverlayTrigger>
        <br />

        <Form.Label htmlFor="report-filename">Report Filename</Form.Label>
        <report-filename>
          <OverlayTrigger
            placement="right"
            delay={{ show: 250, hide: 400 }}
            overlay={filenamePopover}
          >
            <Form.Control
              type="text"
              id="report-filename"
              aria-describedby="questionmark-cursor"
              disabled={disabled}
              value={reportFilename}
              onChange={(e) => {
                setReportFilename(e.target.value)
              }}
            />
          </OverlayTrigger>
        </report-filename>

        <br />
        <Button size="lg" onClick={handleSave}>
          Save
        </Button>
      </Container>
    </div>
  )
}
