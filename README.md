# KGXperience CRM

**KGXperience CRM** is a comprehensive Customer Relationship Management (CRM) application developed using Django. The project aims to provide a user-friendly interface for managing customer interactions, streamlining business processes, and improving overall efficiency.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Secure login and registration system with session management.
- **Dashboard**: Overview of key metrics and activities.
- **Customer Management**: Add, edit, and view customer details.
- **Task Management**: Track and manage tasks and follow-ups.
- **Reporting**: Generate and view reports based on customer data and interactions.
- **Responsive Design**: User-friendly interface optimized for both desktop and mobile devices.

## Technologies Used

- **Django**: A high-level Python web framework for building robust and scalable web applications.
- **HTML/CSS**: For creating and styling the frontend of the application.
- **JavaScript**: For enhancing the interactivity of the web application.
- **Bootstrap**: For responsive and modern UI components.
- **SQLite/PostgreSQL**: Database management (default is SQLite, configurable to PostgreSQL).

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/kgxperience-crm.git
    cd kgxperience-crm
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment:**

    - On Windows:
    
        ```bash
        venv\Scripts\activate
        ```
    
    - On macOS/Linux:
    
        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the Application:**

    Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- **Login**: Access the login page at `/login/`.
- **Dashboard**: After logging in, you will be redirected to the dashboard to manage customers and tasks.
- **Customer Management**: Navigate to the customer management section to add or edit customer details.
- **Task Management**: Manage tasks and view follow-ups from the task management section.
- **Reporting**: Generate and view reports from the reporting section.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
