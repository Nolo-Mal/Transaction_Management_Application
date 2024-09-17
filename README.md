# Project Title
Transaction Management Application

## Description
This is a Flask-based web application designed to manage and view transaction records. It allows users to log in, search for transactions, view details, and download them as an Excel file. The app provides functionality for session management, transaction searching, and more.

## Features
- User Authentication: Login functionality for users. The username is case-insensitive and users can reset their password using the "Forgot Password" feature.

- Transaction Search: Search transactions using various filters such as merchant number, transaction date, retrieval reference number (RRN), device ID, and authorization code.

- Session Management: User sessions expire after 10 minutes of inactivity.

- Transaction Dashboard: View a list of transactions based on search results in a well-organized table.
Download Transactions: Download the search results in Excel format.

- Clear Transactions: Admin function to clear all transactions from the database.

- Support Page: Access contact details for support.

## Installation
Ensure that you have the following installed on your system:

1.  Python 3.x
2.  Flask
3.  SQLAlchemy
4.  pandas
5.  xlsxwriter

## Usage

- Login: Use the following default credentials:

    Username: ab025z6
    Password: nolo2105

- After logging in, you can search transactions and download results.

- Forgot Password: If you forget your password, enter your username and click the "Forgot Password" link to generate a new one.

- Transaction Search: Enter the required filters (merchant number, date, RRN, etc.) on the dashboard to filter the results.

- Download Transactions: Click on the download button to get an Excel file of the search results.

- Clear Transactions: Clear all transactions by making a POST request to /clear_transactions.


## File Structure

1. app.py: Main Flask application that handles routing, transaction searches, and downloads.
2. templates/: Contains HTML templates for the app's views (login, dashboard, support, etc.).
3. static/: Static assets such as CSS files.
4. transactions.db: SQLite database where transaction records are stored.

## Contributing
Contributions are welcome. Please create a pull request or raise an issue.

## License
This project is licensed under the MIT License.

## Support
If you encounter any issues or have questions, feel free to reach out to the support team listed in the app or contact Lehlohonolo Maluleka at lehlohonolomaluleka@gmail.com.



