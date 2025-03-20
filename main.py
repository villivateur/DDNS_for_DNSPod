from flask import Flask
from flask import request
from flask import jsonify
from ipaddress import ip_address, IPv4Address
from dnspod import DNSPod
from config import CONFIG_DATA

app = Flask(__name__)


def CheckIpVersion(ip):
    try:
        return 'IPv4' if type(ip_address(ip)) is IPv4Address else 'IPv6'
    except ValueError:
        return 'Invalid'


@app.route('/')
def DDNS():
    if request.method != 'GET':
        return jsonify({'code': 4, 'msg': 'GET method only'}), 400

    domain = request.args.get('domain')
    token = request.args.get('token')

    matchConfig = None
    for config in CONFIG_DATA:
        if config['token'] == token:
            matchConfig = config['dnspod']

    if matchConfig == None:
        return jsonify({'code': 1, 'msg': 'Invalid token'}), 403

    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']

    ip_version = CheckIpVersion(ip)
    if ip_version == 'IPv4':
        record_type = 'A'
    elif ip_version == 'IPv6':
        record_type = 'AAAA'
    else:
        return jsonify({'code': 2, 'msg': 'Bad IP'}), 400
    
    dnspod = DNSPod(matchConfig)
    ret = dnspod.ChangeRecord(domain, record_type, ip)
    if ret.startswith('Error'):
        return jsonify({'code': 3, 'msg': ret}), 500
    elif ret == "NoChange":
        return jsonify({'code': 0, 'msg': 'OK, No Change'}), 200
    else:
        return jsonify({'code': 0, 'msg': 'OK'}), 200

if __name__ == '__main__':
    app.run(host='::', port=8000)
