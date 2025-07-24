# My Blog - Django Content Management System

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
   source ../venv/bin/activate
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

### Site Configuration
- **Admin Settings**: Configure site name, copyright, pagination
- **Feature Toggles**: Enable/disable search, pinning, categories
- **Display Options**: Control visibility of author info, dates, badges

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

## 📝 Usage

### Creating Posts
1. Login to access "New Post"
2. Choose visibility (Public/Private)
3. Add title, content, and optional category
4. Set mood and priority for personal posts
5. Attach files if needed

### Managing Content
- **My Posts**: View and manage your posts
- **Pinned Posts**: Quick access to important posts
- **Search**: Find posts by title, content, or category
- **Admin**: Configure site settings and manage all content

## 🔒 Security

- User authentication required for content creation
- CSRF protection enabled
- User-specific content access control
- Secure file upload handling

## 📄 License

Open source under MIT License.

---

**Happy Blogging! 📝✨** 
