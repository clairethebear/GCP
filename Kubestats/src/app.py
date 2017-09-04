from flask import Flask
import socket
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    getcwd = os.getcwd()
    top = subprocess.check_output("ps", shell=True)
    output = 'Newest \nHostname: %s \n Top: %s' % (socket.gethostname(), top)
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0')
