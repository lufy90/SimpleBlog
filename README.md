# SimpleBlog - Simple blog system by Django

A modern Django blog application with unified content management, search functionality, and configurable settings.

## Features

- **Blog Posts**: Create, edit, and publish posts with SEO-friendly URLs
- **Search**: Full-text search across posts and content
- **Pinning**: Pin important posts for quick access
- **File Uploads**: Attach images and documents to posts
- **Settings Management**: Configure site name, pagination, and features through admin
- **Multi Users**: Multiple users supported

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment

### Installation

1. **Activate virtual environment**
   ```bash
   cd SimpleBlog
   python -m venv venv
   source ./venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install django pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

5. **Initialize settings**
   ```bash
   python manage.py init_settings
   ```

6. **Start server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

7. **Access the application**
   - Blog: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Technology Stack
- **Backend**: Django 5.2.4
- **Database**: SQLite (configurable)
- **Frontend**: Bootstrap 5, Font Awesome
- **Python**: 3.x

## Preview

We may preview the project at https://lufy.org (⚠️ this isn't demo site).

## Deploy

Nginx + gunicorn/wsgi/asgi

### Prerequisites

**nginx** and **gunicorn** already installed in operating system.

### simpleblog and nginx config files

```
## simpleblog service file: /etc/systemd/system/simpleblog.service (this is the Rocky linux way, the real location for nginx conf file may up to the OS)
[Unit]
Description=SimpleBlog Gunicorn
After=network.target

[Service]
User=root
Group=nginx
WorkingDirectory=/opt/SimpleBlog/
ExecStart=/venv/bin/gunicorn blog.wsgi:application \
          --bind unix:/run/simpleblog.sock \
          --workers 2 \
          --timeout 120
RuntimeDirectoryMode=775
Restart=always

[Install]
WantedBy=multi-user.target
```

```
## nginx config file: /etc/nginx/conf.d/simpleblog.conf
server {
    listen <port>; ## replace port to numberic port
    server_name <server_name>; ## replace server_name to your domain name
    client_max_body_size 16M;

    location /static/ {
            alias /SimpleBlog/staticfiles/;
    }

    location /media/ {
            alias /SimpleBlog/media/;
    }
    location / {
            proxy_pass http://unix:/run/simpleblog.sock;
    }
}
```

### Collect static files and update SimpleBlog settings.

```
## collect static files
./manage.py collectstatic
```

```
## edit blog/settings.py, make followed changes
DEBUG = False                                  ## Set to False to disable django debug feature
CSRF_TRUSTED_ORIGINS = ["<Domain name>"]       ## Set the domain name as trusted origin
```

### Start the services

```
systemctl start simpleblog
systemctl restart nginx
```

## License

Open source under MIT License.

---

**Happy Blogging!** 
