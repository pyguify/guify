# GUIfy

---

Simplest form of GUI for automation scripts.

Made with eel as python backend and react used as frontend.

## How to use

```bash
pip install guify
```

```py
# main.py
import GUIfy from guify

# Instantiate the app, variables are optional.
# app_name is the title of the app shown on the top, equivalent to <title /> tag in HTML
# report_dir is the directory where reports will be stored
# report_prefix is the prefix of the report, if none, it will be 'report'
# if set to 'serial_number', this will be requested in the gui.
app = GUIfy(app_name='GUIfy', port=8080, report_dir=None, report_prefix=None) # default app_name is 'GUIfy'

# Register the function "test_1"
# All variables are optional
# name - the name of the "test" in the gui
# priority - Sets the order of the tests, priority 0 will run before priority 1
# description - the small text description under the test's name in the gui.
@app.register(name='Test 1', priority=0, description='This is a test')
# Define the test, each argument that "test_1"
# requires will be automatically prompted for in the gui.
# no arg will be requested twice.
def test_1(example_arg):
    # app.monitor object represents the textarea on the right-hand side of the gui
    # app.monitor.clear_text() - sets the text to empty string
    app.monitor.clear_text()

    # app.monitor.set_text(text) - sets the text to whatever is passed to it
    app.monitor.set_text('This is a test\n')

    # app.monitor.append_text(text) - appends whatever passed to it to the textarea
    app.monitor.append_text('This is a test2\n')

    # app.prompt_user(prompt) - pops up a modal in the gui and asks user to click OK or cancel.
    # app.prompt_user will return True if user clicked OK and False if user clicked cancel
    result = app.prompt_user('This is a prompt') # True if user clicked OK, False if user clicked Cancel

    # app.config get something from config tab, acts similar to configparser
    # config stored in config.ini in the current working directory.
    foo = app.config.get('example','foo') # == bar

    # Specify the return type, this is used for report generation
    # if function returns True then test considered as Passed
    # if function returns False then test considered as Failed
    return True


# this test will be registered after test_1, because its priority arg is higher.
@app.register(name='Test 2', priority=1, description='This is the second test.')
def test_2(example_arg, second_arg):
    app.monitor.clear_text()




app.run()

```

---

### Monitor object

app.monitor is the monitor object representing the preview window on right hand side of the GUI,

- set_text(text: str) -> None // will set the text in the monitor to whatever passed in "text" argument
- append_text(text: str) -> None // will append the next to the monitor
- clear_text(text: str) -> None // will clear all text in the monitor

---

## Config tab

"app.config" is an object representing the config tab.
All configurations are stored in config.ini.

### app.config methods:

- save() // Save config to config.ini
- load() // Load config from config.ini
- get_section() // load() and return an entire section as a dictionary
- get(section, attribute) // load() and get value of attribute in section
- set(section, attribute, value) // load() and set value of attribute in section and then save().

Assuming this is the config file:

```ini
[example]
foo = bar
```

This will be the correct usage of app.config object

```py
app.config.get_section('example') -> {'foo': 'bar'}
app.config.get('example', 'foo') -> 'bar'
```

---

## Building

Theoretically its possible to build an executable with eel using the following:

```bash
py -m eel index.py build --onefile --noconsole --name <whatever_u_want> --icon=public/favicon.ico
```

Please not that this hasn't been tested yet.
