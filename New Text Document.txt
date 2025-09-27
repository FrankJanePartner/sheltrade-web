# Sheltrade Web Platform

## Project Overview
Sheltrade is a comprehensive financial platform designed to facilitate a variety of financial transactions including wallet management, gift card sales, and user notifications. The platform supports user profiles with customizable preferences such as preferred currency and phone number. It provides a secure and user-friendly interface for managing transactions, gift cards, and notifications.

The platform distinguishes between different user roles, including regular users, staff, superusers, and a special "Workers" group, each with specific access levels and functionalities.

## What You Can Do on the Platform
- Manage your wallet balance and view transaction history.
- Buy and sell gift cards securely.
- Receive and manage notifications related to your account activities.
- Update your profile details including username, phone number, and preferred currency.
- Access a personalized dashboard tailored to your user role.

## What You Can Do with the Code
- Extend or customize the platform by adding new features or modifying existing ones.
- Integrate with external APIs for additional financial services.
- Build a mobile application using the provided API endpoints.
- Manage user roles and permissions to tailor access control.
- Utilize the modular app structure to maintain and scale the platform efficiently.

## Project Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (optional but recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd sheltrade-web
```

### Step 2: Create and Activate a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
Install all required Python packages using pip:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root directory with the following variables:
```
VTPass_API_KEY=your_vtpass_api_key_here
VTPass_PUBLIC_KEY=your_vtpass_public_key_here
VTPass_SECRET_KEY=your_vtpass_secret_key_here
VTPass_BASE_URL=https://sandbox.vtpass.com/api
VTPass_EMAIL=your_email@example.com
VTPass_PASSWORD=your_password_here
DEBUG=True
```
Replace the placeholder values with your actual credentials.

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```
Access the platform at `http://127.0.0.1:8000/` in your web browser.

## API Endpoints Overview
The platform exposes several key API endpoints for interaction:

- `/api/wallet/` - Manage wallet balance and transactions.
- `/api/giftcard/` - Buy, sell, and verify gift cards.
- `/api/notifications/` - Retrieve and manage user notifications.
- `/api/profile/` - Update and retrieve user profile information.
- `/api/auth/` - User authentication and registration endpoints.

Each endpoint supports standard HTTP methods (GET, POST, PUT, DELETE) as appropriate. Authentication is required for most endpoints.

## Colors and Styling
The platform uses a consistent color scheme to enhance user experience:

- Primary Color: #007bff (Blue) - Used for buttons, links, and highlights.
- Secondary Color: #6c757d (Gray) - Used for secondary buttons and text.
- Success Color: #28a745 (Green) - Used for success messages and indicators.
- Danger Color: #dc3545 (Red) - Used for error messages and warnings.
- Background Color: #f8f9fa (Light Gray) - Used for page backgrounds.

These colors are defined in the CSS files located in `static/core/css/` and applied throughout the UI components.

## Packages and Libraries Used
The project leverages several key packages and libraries:

- Django: Web framework for backend development.
- Django REST Framework: For building RESTful APIs.
- Requests: For making HTTP requests to external APIs.
- Puppeteer: For automated UI testing.
- Coverage.py: For test coverage measurement.
- React Native & Expo (optional): For mobile app development.
- Other Django apps: billPayments, giftcard, crypto, mobileTopUp, wallet, sheltradeAdmin for modular functionality.

## Project Flow Overview
1. User Authentication via email/username or phone number.
2. Role-Based Redirection to user dashboard or admin interface.
3. User Dashboard with transactions, wallet, gift cards, and notifications.
4. Wallet and Transactions management.
5. Gift Card buying and selling.
6. Notifications management.
7. Profile and Settings management.

## Additional Notes
- The platform uses environment variables for sensitive information and configuration.
- User roles are enforced to restrict access to certain features.
- The project includes multiple Django apps for modular functionality.
- For mobile app development, refer to the `mobile app` section below.

## Mobile App Development (Optional)
The platform supports building a mobile application for regular users using React Native and Expo. The mobile app provides access to core functionalities excluding administrative features.

### Mobile App Setup
1. Install Node.js and Expo CLI.
2. Create a new React Native project with Expo.
3. Use the platform's API endpoints for data interaction.
4. Run and test the app using Expo Go or an emulator.

---

This README provides a comprehensive overview of the Sheltrade platform, its capabilities, setup instructions, API details, styling guide, and development notes to help developers and users get started quickly.
