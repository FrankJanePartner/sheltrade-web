# Sheltrade Web Platform

## Project Overview
Sheltrade is a comprehensive web platform designed to facilitate financial transactions, wallet management, gift card sales, and user notifications. The platform supports user profiles with customizable preferences such as preferred currency and phone number. It provides a secure and user-friendly interface for managing transactions and gift cards.

## User Roles and Access
The platform distinguishes between different types of users with specific roles and access levels:

- **Regular Users:** These users have access to the full range of functionalities including wallet management, transactions, gift card sales, notifications, and profile settings.
- **Staff and Superusers:** These users have administrative privileges and access the platform's admin interface. Their functionalities are not included in the mobile app.
- **Workers Group:** Users belonging to the "Workers" group are also redirected to the admin interface and do not have functionalities in the mobile app.

## Mobile App Development with React Native and Expo
This project supports building a mobile application for regular users using React Native and Expo. The mobile app will provide access to the core functionalities of the platform, excluding any features available only to staff, superusers, or workers group members.

### Getting Started
To build the mobile app, follow these steps:

1. **Set up the development environment:**
   - Install [Node.js](https://nodejs.org/)
   - Install [Expo CLI](https://docs.expo.dev/get-started/installation/) by running:
     ```
     npm install -g expo-cli
     ```
2. **Create a new React Native project with Expo:**
   ```
   expo init sheltrade-mobile
   ```
3. **Implement the mobile app features:**
   - Use the platform's API endpoints to interact with user data, transactions, wallets, gift cards, and notifications.
   - Ensure that the app only allows access to functionalities for regular users (exclude staff, superusers, and workers).
   - Implement authentication and user profile management consistent with the web platform.
4. **Run and test the app:**
   ```
   cd sheltrade-mobile
   expo start
   ```
   Use the Expo Go app on your mobile device or an emulator to test the application.

### Notes
- The mobile app should not include any administrative features or access for staff, superusers, or workers group users.
- Ensure proper handling of user roles and permissions when interacting with the backend API.
- Follow best practices for React Native and Expo development to create a performant and user-friendly mobile experience.

---

This README provides an overview of the Sheltrade platform and guidance for building a mobile app tailored for regular users. For more detailed API documentation and backend development, refer to the respective project files and documentation.

## Project Flow Description

Below is a textual flowchart describing the main flow of the Sheltrade platform:

1. **User Authentication**
   - User logs in via email/username or phone number.
   - Authentication is verified against stored credentials.

2. **Role-Based Redirection**
   - If user is in the "Workers" group, staff, or superuser:
     - Redirect to the admin interface for administrative tasks.
   - Else:
     - Redirect to the user dashboard.

3. **User Dashboard**
   - Displays user transactions, wallet balance, gift cards, and notifications.
   - Users can update profile details including preferred currency and phone number.

4. **Wallet and Transactions**
   - Users can view and manage their wallet balance.
   - Transactions are recorded and displayed in the dashboard.

5. **Gift Cards**
   - Users can buy and sell gift cards.
   - Gift card details are accessible from the dashboard.

6. **Notifications**
   - Users receive notifications about account activities.
   - Notifications can be marked as read or viewed in detail.

7. **Settings and Profile Management**
   - Users can change username, update phone number, and set preferred currency.
   - Changes trigger notifications to inform users of updates.

8. **Mobile App Scope**
   - The mobile app built with React Native and Expo targets regular users only.
   - Staff, superusers, and workers group users do not have access to the mobile app functionalities.

This flow provides a high-level overview of how users interact with the Sheltrade platform and the separation of roles within the system.
