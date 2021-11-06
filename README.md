# DDNS_for_DNSPod

Simple python DDNS server based on DNSPod APIs

## Usage

1. Rename `config_sample.py` to `config.py`
2. Get your dnspod token from dnspod.cn
3. Edit `config.py` as you go
4. The `TOKEN` field is for your client to connect to your server
5. Add your A or AAAA record for DDNS on dnspod.cn. (This server can only deal with exist records)
6. On your client, request https://[yourserver]/?domain=[your ddns domain]&token=[your token in step 4]
7. if you have a proxy server such as Nginx, please set up the `X-Real-IP` and `X-Forwarded-For` header (read <https://www.digitalocean.com/community/questions/how-do-i-forward-client-ip-instead-of-proxy-ip-in-nginx-reverse-proxy>)
