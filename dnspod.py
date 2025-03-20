import requests
import json

class DNSPod:
    def __init__(self, dnspod_config):
        self.dnspod_config = dnspod_config
        self.record_line = '默认'
        self.common_headers = {
            'User-Agent': dnspod_config['user_agent'],
        }
        self.common_payload = {
            'login_token': dnspod_config['login_token'],
            'format': 'json',
            'domain': dnspod_config['domain'],
        }

    def GetRecordId(self, record_name, record_type):
        if not record_name.endswith(self.dnspod_config['domain']):
            return 'Error: Invalid domain'
        
        record_name = record_name[:-(len(self.dnspod_config['domain']) + 1)]

        r = requests.post('https://dnsapi.cn/Record.List', headers=self.common_headers, data=self.common_payload)
        record_data = json.loads(r.text)

        if record_data['status']['code'] != '1':
            return 'Error: Request error'
        record_info_list = record_data['records']

        for record_info in record_info_list:
            if record_name == record_info['name'] and record_type == record_info['type']:
                return record_info['id']
        
        return 'Error: Not found'

    def GetRecordValue(self, record_id):
        payload = {
            'record_id': record_id,
            'remark': '',
        }
        payload.update(self.common_payload)
        r = requests.post('https://dnsapi.cn/Record.Info', headers=self.common_headers, data=payload)
        record_data = json.loads(r.text)
        return record_data['record']['value']

    def ChangeRecord(self, record_name, record_type, record_value):
        id = self.GetRecordId(record_name, record_type)

        if id.startswith('Error'):
            return 'Error: Get record id - ' + id
        
        if record_type != 'A' and record_type != 'AAAA':
            return 'Error: Record type not support'
        
        if record_value == self.GetRecordValue(id):
            return 'NoChange'
        
        payload = {
            'record_line': self.record_line,
            'record_id': id,
            'value': record_value,
            'record_type': record_type,
            'sub_domain': record_name[:-(len(self.dnspod_config['domain']) + 1)],
        }

        payload.update(self.common_payload)

        r = requests.post('https://dnsapi.cn/Record.Modify', headers=self.common_headers, data=payload)
        record_data = json.loads(r.text)

        if record_data['status']['code'] != '1':
            return 'Error: Request error'
        print(record_data)
        return 'OK'
