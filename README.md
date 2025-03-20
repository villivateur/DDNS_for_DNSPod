# DDNS_for_DNSPod

Simple python DDNS server based on DNSPod APIs

## Usage

1. Rename `config_sample.py` to `config.py`
2. Get your dnspod token from dnspod.cn
3. Edit `config.py` as you go, you may add more than one 2nd level domain and dnspod login credential
4. The `token` field is for your client to connect to your server
5. Add your A or AAAA record for DDNS on dnspod.cn. (This server can only deal with existing records)
6. On your client, request https://[yourserver]/?domain=[your ddns domain]&token=[your token in step 4]
7. if you have a proxy server such as Nginx, please set up the `X-Real-IP` and `X-Forwarded-For` header (read <https://www.digitalocean.com/community/questions/how-do-i-forward-client-ip-instead-of-proxy-ip-in-nginx-reverse-proxy>)

## Sample Nginx config

```nginx
server {
    server_name v4.example.com v6.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    listen [::]80;
    listen 80;
}
```

Then you may request https://v4.example.com/?domain=myddns.example.com&token=xxxxxxxxxxxxxxx

## Sample systemd service file

```ini
[Unit]
Description=DDNS for DNSPod
After=network.target

[Service]
Type=simple
User=username
Restart=on-failure
RestartSec=5s
ExecStart=/usr/bin/python3 /path/to/DDNS_for_DNSPod/main.py

[Install]
WantedBy=multi-user.target
```
