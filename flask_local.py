
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
    return pyphoon_getter("")
    
@app.route('/pyphoon/<arguments>')
def pyphoon_getter(arguments=""):

    args = ['python' , 'src/__init__.py']
    if arguments: args += arguments.split()

    # if request.method == 'GET':

    #process = subprocess.Popen(['python3' , 'pyphoon/src/__init__.py' ], stdout=subprocess.PIPE)
    #process = subprocess.Popen(['python' , '-h' ], stdout=subprocess.PIPE)
    #out, err = process.communicate()

    process = subprocess.Popen(args, #shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out = ["<pre>\n"]
    for line in process.stdout: out.append(cgi.escape(line.decode("utf-8", 'ignore'),True))
    for line in process.stderr: out.append(cgi.escape(line.decode("utf-8", 'ignore'),True)) 
    out.append("</pre>\n")
    return "".join(out)

def a():
    return pyphoon_getter()