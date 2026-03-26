# IP Subnet Calculator (Django)

Simple web-based IPv4/IPv6 subnet calculator built with Django.

## Features

- Accepts CIDR input like `192.168.1.10/24` or `2001:db8::1/64`
- Calculates network, mask, host range, and capacity
- Handles edge IPv4 cases (`/31`, `/32`)
- Includes basic test coverage for service logic and web view

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Run tests

```powershell
python manage.py test
```

