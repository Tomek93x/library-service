# Library Service API

A full-stack Django REST API for managing a library system: book inventory, borrowings, users, payments (Stripe), and Telegram notifications.

## 📋 Project Description

This project modernizes a traditional library by implementing an online management system for book borrowings. The system optimizes library administrators' work and makes the service more user-friendly.

**Problem solved:**
- Manual paper-based tracking of books, borrowings, and payments
- No real-time inventory management
- Cash-only payments
- No automated overdue notifications

**Solution:**
- Web-based REST API for all library operations
- Automated Stripe payment processing
- Real-time Telegram notifications
- JWT-based authentication
- Scheduled daily overdue checks

---

## ✨ Features

### Books Management
- ✅ Full CRUD operations (admin only)
- ✅ Public book listing and search
- ✅ Inventory tracking
- ✅ Cover type (HARD/SOFT) support

### User Management
- ✅ Custom user model with email authentication
- ✅ JWT token-based authentication
- ✅ User registration and profile management
- ✅ Admin/staff role permissions

### Borrowing System
- ✅ Create borrowings with automatic inventory updates
- ✅ Filter by user and active/returned status
- ✅ Return functionality with fine calculation
- ✅ Automatic payment creation on borrowing

### Payment Processing
- ✅ Stripe payment integration
- ✅ Automatic payment session creation
- ✅ Payment success/cancel webhooks
- ✅ Fine calculation for overdue returns
- ✅ Payment status tracking (PENDING/PAID)

### Notifications
- ✅ Telegram bot integration
- ✅ New borrowing notifications
- ✅ Daily overdue check notifications
- ✅ Successful payment notifications

### Background Tasks
- ✅ Django-Q integration for async tasks
- ✅ Scheduled daily overdue checks
- ✅ Redis-backed task queue

---

## 🏗️ Architecture

The system follows a microservices-inspired architecture with the following components:

- **Books Service**: Manage book catalog and inventory
- **Users Service**: Handle authentication and user profiles
- **Borrowings Service**: Manage borrowing operations
- **Payments Service**: Process payments via Stripe
- **Notifications Service**: Send Telegram notifications
- **Background Tasks**: Django-Q cluster for scheduled tasks

All services communicate via REST API endpoints documented in Swagger.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL 15+ (or SQLite for development)
- Redis 7+
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone the repository**
