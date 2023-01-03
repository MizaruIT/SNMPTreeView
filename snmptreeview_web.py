from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException
from snmpclientclass import SnmpClient, SnmpError
import os, sys
import json 
sys.path.append('.')

#Flask app
app = Flask(__name__, static_folder = "static")

#snmpclient = SnmpClient(None, None, None, None, None, None, None, None, None)

class ipRequired(Exception):
    pass

# To handle the different exceptions/errors
@app.errorhandler(Exception)
def handle_exception(e):
    return str(e), 500
    #return render_template('index.html', version=None, data=None, error=e), 500

@app.route('/getvalue')
def getvalue():
    snmp_params = request.args.to_dict()
    snmp = SnmpClient(snmp_params['ip'], 161, snmp_params['community'], int(snmp_params['version']), snmp_params['userName'], snmp_params['authKey'], snmp_params['privKey'], snmp_params['authProtocol'], snmp_params['privProtocol'])  
    oid, value = snmp.get_Request(snmp_params['oid'])
    return str(value) 

@app.route('/setvalue')
def setvalue():
    snmp_params = request.args.to_dict()
    snmp = SnmpClient(snmp_params['ip'], 161, snmp_params['community'], int(snmp_params['version']), snmp_params['userName'], snmp_params['authKey'], snmp_params['privKey'], snmp_params['authProtocol'], snmp_params['privProtocol'])  
    value = snmp.set_Request(snmp_params['oid'], snmp_params['new_value'], snmp_params['datatype'])
    return str(value)

#add option to set value in terminal
#for the first request, do a get request and if return nothing, end
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET' and request.args:
        snmp_params = request.args.to_dict()
        snmp = SnmpClient(snmp_params['ip'], 161, snmp_params['community'], int(snmp_params['version']), snmp_params['userName'], snmp_params['authKey'], snmp_params['privKey'], snmp_params['authProtocol'], snmp_params['privProtocol'])   
        if not snmp_params['ip']:
            raise ipRequired('IP/address is required.') 
        else:
            data_got = snmp.getAllInfos_fromSub(snmp_params['oid'])
            return json.dumps(data_got)
    return render_template('index.html', snmp_args=None)
