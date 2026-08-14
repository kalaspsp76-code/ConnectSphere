# 🌐 ConnectSphere – Social Media Platform

ConnectSphere is a full-stack social media web application developed using **Python and Django**.

The platform allows users to create accounts, manage profiles, share text and image posts, like and comment on posts, follow other users, explore people, and receive notifications.

This project was developed as a practical full-stack web development project to demonstrate backend development, database relationships, authentication, media uploads, and responsive frontend design.

---

## 🎯 Project Overview

The goal of ConnectSphere is to create a simple and modern social networking platform where users can connect, communicate, and share content with other users.

The application includes user authentication, profile management, social interactions, image-based posts, following functionality, notifications, and an interactive dashboard.

---

## ✨ Features

### 🔐 Authentication
- User registration
- User login
- User logout
- Django authentication system

### 👤 User Profiles
- View personal profile
- View other users' profiles
- Edit profile
- Update biography
- Upload profile picture

### 📝 Posts
- Create text posts
- Upload images with posts
- Display posts in the dashboard
- Display post creation time
- View post author

### ❤️ Social Interactions
- Like posts
- Unlike posts
- Display like count
- Add comments
- Display comments
- Share posts

### 👥 Follow System
- Follow users
- Unfollow users
- Display following status
- Discover other users

### 🔔 Notifications
- Follow notifications
- Interaction notifications
- Unread notification count
- Notification status

### 🔍 Explore
- Discover users
- View user profiles
- Find new people to connect with

### 📱 Responsive UI
- Clean dashboard
- Responsive layout
- Modern cards and navigation
- Mobile-friendly design

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Django 6.1

### Database

- SQLite

### Media Handling

- Pillow

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Git Bash

---

## 🏗️ Project Structure

```text
ConnectSphere/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── static/
│   │   └── core/
│   │       └── css/
│   │           └── style.css
│   │
│   ├── templates/
│   │   └── core/
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── ConnectSphere/
│   └── urls.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
