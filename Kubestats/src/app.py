from flask import Flask
import socket
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def kubestats():
    getcwd = os.getcwd()
    node_id = None
    try:
      node_ip = subprocess.check_output("curl http://169.254.169.254/0.1/meta-data/network", shell=True)
      node_ip = format_ip(node_ip)
    except IOError:
      print "Error meta-data server not running on this machine"
#    top = subprocess.check_output("ps", shell=True)
#    output = 'Newest \nHostname: %s \n Top: %s \n\n Node IP: %s\n\n' % (socket.gethostname(), top, node_ip)
#    return output
     return 'testing new'

def format_ip(node_ip):
    split_by_name = node_ip.split("externalIp\":\"", 1)[1]
    split_by_name = split_by_name.split("\",", 1)[0]
    return split_by_name

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
