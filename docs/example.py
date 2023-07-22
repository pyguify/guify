import guify

app = guify.GUIfy()
# app:
# app.config.get('example', 'foo') -> 'bar'
# app.config.get_section('example') -> {'foo': 'bar'}
# app.config.update_key('example', 'foo', 'baz') // updates the value of the key 'foo' in the section 'example' to 'baz'
# app.config.update_value('example', 'foo', 'baz') // sets the value of the key 'foo' in the section 'example' to 'baz'
# full api of app.config available in homepage of guify on github
# app.monitor // text area object in the main tab
# app.monitor.append_text('hello world\n') // appends text to the text area
# app.monitor.set_text('hello world\n') // sets the text area to 'hello world'
# app.monitor.flush() // clears the text area
# app.prompt_user('title', 'prompt') -> (True if OK, False if CANCEL)


@app.register(priority=1, name="test 1", description="test1")
def test1(test_arg):
    print("Running test1\n")
    app.config.insert('example', 'foo', 'bar')
    print(str(app.prompt_user('test_arg:', test_arg)))
    print(app.config.get_section('example'))
    app.config.delete('example', 'foo')
    return True


@app.register(priority=0, name="test 2", description="test2")
def test2(test_arg2):
    print("Running test2\n")

    return True


app.run()
