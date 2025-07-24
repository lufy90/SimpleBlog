# SimpleBlog - Simple blog system by Django

A modern Django blog application with unified content management, search functionality, and configurable settings.

## ✨ Features

- **Blog Posts**: Create, edit, and publish posts with SEO-friendly URLs
- **Personal Posts**: Private posts with mood tracking and categories
- **Search**: Full-text search across posts and content
- **Pinning**: Pin important posts for quick access
- **File Uploads**: Attach images and documents to posts
- **Settings Management**: Configure site name, pagination, and features through admin
- **Responsive Design**: Modern Bootstrap 5 interface

## 🚀 Quick Start

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
   pip install django
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

## 🎯 Key Features

### Content Management
- **Public Posts**: Published blog posts visible to everyone
- **Private Posts**: Personal posts with mood tracking
- **Categories**: Organize posts by topics
- **File Attachments**: Upload images and documents

### Search & Organization
- **Full-Text Search**: Search across titles, content, and categories
- **Post Pinning**: Pin important posts for quick access
- **Pagination**: Configurable posts per page

## 🔧 Configuration

Access the admin interface to configure:
- **Site Information**: Name, description, tagline
- **Content Settings**: Posts per page, search results
- **Display Settings**: Show/hide author info, dates, categories
- **Footer Information**: Copyright text, powered by text
- **Feature Toggles**: Enable/disable specific features

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (configurable)
- **Frontend**: Bootstrap 5, Font Awesome
- **Python**: 3.x

## 🔒 Security

- User authentication required for content creation
- CSRF protection enabled
- User-specific content access control
- Secure file upload handling

## 📄 License

Open source under MIT License.

---

**Happy Blogging! 📝✨** 
