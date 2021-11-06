import requests
import json
from config import DNSPOD_CONFIG

RECORD_LINE = '默认'

common_headers = {
    'User-Agent': DNSPOD_CONFIG['user_agent'],
}

common_payload = {
    'login_token': DNSPOD_CONFIG['login_token'],
    'format': 'json',
    'domain': DNSPOD_CONFIG['domain'],
}

def GetRecordId(record_name, record_type):
    if not record_name.endswith(DNSPOD_CONFIG['domain']):
        return 'Error: Invalid domain'
    
    record_name = record_name[:-(len(DNSPOD_CONFIG['domain']) + 1)]

    r = requests.post('https://dnsapi.cn/Record.List', headers=common_headers, data=common_payload)
    record_data = json.loads(r.text)

    if record_data['status']['code'] != '1':
        return 'Error: Request error'
    record_info_list = record_data['records']

    for record_info in record_info_list:
        if record_name == record_info['name'] and record_type == record_info['type']:
            return record_info['id']
    
    return 'Error: Not found'

def GetRecordValue(record_id):
    payload = {
        'record_id': record_id,
        'remark': '',
    }
    payload.update(common_payload)
    r = requests.post('https://dnsapi.cn/Record.Info', headers=common_headers, data=payload)
    record_data = json.loads(r.text)
    return record_data['record']['value']

def ChangeRecord(record_name, record_type, record_value):
    id = GetRecordId(record_name, record_type)

    if id.startswith('Error'):
        return 'Error: Get record id - ' + id
    
    if record_type != 'A' and record_type != 'AAAA':
        return 'Error: Record type not support'
    
    if record_value == GetRecordValue(id):
        return 'NoChange'
    
    payload = {
        'record_line': RECORD_LINE,
        'record_id': id,
        'value': record_value,
        'record_type': record_type,
        'sub_domain': record_name[:-(len(DNSPOD_CONFIG['domain']) + 1)],
    }

    payload.update(common_payload)

    r = requests.post('https://dnsapi.cn/Record.Modify', headers=common_headers, data=payload)
    record_data = json.loads(r.text)

    if record_data['status']['code'] != '1':
        return 'Error: Request error'
    print(record_data)
    return 'OK'
