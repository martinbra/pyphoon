
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import subprocess
import cgi

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/pyphoon/')
def pyphoon_only():
    return pyphoon_getter()

@app.route('/pyphoon/<arguments>')
def pyphoon_getter(arguments=""):

    args = ['python3' , 'mysite2/pyphoon/src/__init__.py']

    if arguments: args += arguments.split()

    returned_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    # wait for the process to terminate
    out = ["<pre>\n"]
    out.append(cgi.escape(returned_output.decode("utf-8", 'ignore'),True))
    out.append("</pre>\n")
    return "".join(out)
