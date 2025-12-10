#developer 

## When you change `port=5001` to `5002` in `app.py`}

You must update every place that references the old port

💡 Use recursive `grep` to find every reference to a port inside **systemd services** and **NGINX config**

### 1. Systemd Services Files
Update required only if the services explicitly sets the port. 

Examples that **must be updated**:
```bash
ExecStart=/usr/bin/gunicorn -b 127.0.0.1:5001 app:app
ExecStart=/usr/bin/uvicorn app:app --host 127.0.0.1 --port 5001
```

Examples that **does not need update:**
```bash
ExecStart=/usr/bin/python3 /path/to/app.py
```

(Port is controlled inside the Python file)

#### 1. Check Systemd services files

Systemmd unit files are usually in: 
- `/etc/systemd/system/`
- `/lib/systemd/system/`

Search for anything that contains 5001(replace with the port you want):

```bash
grep -Rni "5001" /etc/nginx/sites-available/
grep -Rni "5001" /etc/nginx/sites-enabled/
```

To search for any port definition in general:

```bash
grep -RniE "port|500[0-9]|80[0-9][0-9]" /etc/systemd/system/
```

- [[How to see only services that contain ports]]
### 2. NGINX Configuration
Always update if `proxy_pass` points to the old port

Example:
```nginx
proxy_pass http://127.0.0.1:5001;
```
Change to:
```nginx
proxy_pass http://127.0.0.1:5002;
```

#### 2. Check NGINX configuration

NGINX configs are usually in:

- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

To find **any** proxy lines pointing to local ports:
```bash
grep -RniE "proxy_pass.*[0-9]{4}" /etc/nginx/
```

Search for the port:
```bash
grep -Rni "5001" /etc/nginx/sites-available/
grep -Rni "5001" /etc/nginx/sites-enabled/
```
### 3. Restart After Changes
```bash
sudo systemctl daemon-reload
sudo systemctl restart yourservice.service
sudo systemctl restart nginx
```