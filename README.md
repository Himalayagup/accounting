# Accounting Backend & Frontend

## Overview
This project is a comprehensive Indian accounting software solution. It consists of a Django-based backend for managing masters, transactions, and compliance logic, and a Next.js-based frontend for the user interface.

## Project Structure
- `accounting_backend/`: The root directory (Django Backend).
    - `masters/`: App for managing Masters (Ledgers, Items, etc.).
    - `transactions/`: App for managing Vouchers and Transactions.
    - `core/`: Core utilities and base configurations.
    - `users/`: User authentication and management.
- `accounting_frontend/`: The Next.js Frontend application.
    - `src/app/`: App Router pages and layouts.
    - `src/components/`: Reusable UI components.
    - `public/`: Static assets.

## Tech Stack

### Backend
- **Framework**: Django
- **API**: Django REST Framework
- **Database**: SQLite (Development)

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Library**: React 19
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI
- **Icons**: Lucide React
- **HTTP Client**: Axios

## Setup Instructions

### Backend (Django)
1. **Prerequisites**: Python 3.8+ installed.
2. **Virtual Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   .\venv\Scripts\activate
   # Unix/MacOS:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Run Server**:
   ```bash
   python manage.py runserver
   ```

### Frontend (Next.js)
1. **Navigate to the frontend directory**:
   ```bash
   cd accounting_frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Run Development Server**:
   ```bash
   npm run dev
   ```

## API Documentation
The backend API is versioned (e.g., `/api/v1/`). Refer to the specific app URLs for endpoint details.

## License
[License Information]
