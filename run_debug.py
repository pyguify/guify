from src.guify import GUIfy
import logging
import sys
logging.basicConfig(level=logging.DEBUG, filename='log.txt')

DEBUG = True
if DEBUG:
    eel_kwargs = dict(
        directory='src',
        app=None,
        page={'port': 3000},
        port=3001,
        app_mode=False,
        debug=True
    )
app = GUIfy("Testing GUIfy", redirect_stdout=True)
# app:
# app.config.get('example', 'foo') -> 'bar' (from config.ini)
# app.config.get_section('example') -> {'foo': 'bar'} (from config.ini)
# app.config.set('example', 'foo', 'baz') // sets foo to baz in config.ini
# app.monitor // text area object in the main tab
# app.monitor.append_text('hello world\n') // appends text to the text area
# app.monitor.set_text('hello world\n') // sets the text area to 'hello world'
# app.monitor.flush() // clears the text area
# app.prompt_user('prompt') -> (True if OK, False if CANCEL)


@app.register(priority=1, name="test 1", description="test1")
def test1(test_arg):
    print("Running test!")
    raise Exception("Test exception")
    return True


@app.register(priority=0, name="test 2", description="test2")
def test2(test_arg2):

    return True


app.run(_eel_kwargs=eel_kwargs if DEBUG else {})
