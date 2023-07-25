from src.guify import GUIfy
import logging
from time import sleep
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
# app.monitor.write('hello world\n') // appends text to the text area
# app.monitor.set_text('hello world\n') // sets the text area to 'hello world'
# app.monitor.flush() // clears the text area
# app.prompt_user('prompt') -> (True if OK, False if CANCEL)


@app.register(priority=0, name="test 1", description="test1")
def test1(test_arg):
    app.prompt_user("Please confirm:", "test1")
    print("Running test!")
    print(str(app.prompt_user('test_arg:', test_arg)) + "\n")
    print(app.config.insert('example', 'foo', 'bar'))
    app.prompt_user(app.config.get_all(), 'foo')
    app.config.delete('example', 'foo')

    return True


@app.register(priority=1, name="test 2", description="test2")
def test2(test_arg2):
    print("Running test2!")
    print(app.prompt_user("Please confirm:", "test2"))
    try:
        raise Exception("test")
    except Exception as e:
        print(str(e) + "\n")
        raise

    return True


@app.register()
def test3():
    return None


@app.register()
def test4():
    return None


@app.register()
def test5():
    return None


@app.register()
def test6():
    return None


@app.register()
def test7():
    return None


@app.register()
def test8():
    return None


app.run(_eel_kwargs=eel_kwargs if DEBUG else {})
