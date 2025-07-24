# Interactive Google Calendar Scheduler

A web application built with **FastAPI** that allows users to interactively select dates
on a calendar and add various event types (e.g., duty, blood donation) directly to their **Google Calendar**.

***

## Key Features

* **Google OAuth 2.0 Integration:** Securely log in with your Google account.
* **Interactive Calendar UI:** A dynamic, client-side rendered calendar for easily selecting and deselecting multiple dates.
* **Custom Event Types:** Define different types of events (e.g., Duty, Day Off) with unique colors.
* **Continuous Shift Cycle:** The calendar's background follows a continuous, 3-day shift cycle.
* **Direct Calendar Integration:** Events are added to the user's primary calendar with a single click.
* **Responsive Design:** The interface is designed to work on both desktop and mobile devices.

***

## Tech Stack

* **Backend:** Python, FastAPI
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Authentication:** Google OAuth 2.0
* **API:** Google Calendar API v3
* **Configuration:** Pydantic, python-dotenv

***

## Installation and Setup

Follow these steps to run the project locally.

### 1. Prerequisites

* **Python 3.9+**
* A Google account and a configured project in the **Google Cloud Console**.

### 2. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/google-calendar-scheduler.git](https://github.com/YOUR_USERNAME/google-calendar-scheduler.git)
cd google-calendar-scheduler
```

### 3. InActive the Repository  

1. Create and Activate a Virtual Environment
Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

```bash
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```
3. Configure Environment Variables
You need to create two configuration files in the root project directory:

a) .env file:
Create a file named .env and add a secret key for session management.

```bash
# Generate a random string (e.g., using `secrets.token_hex(32)` in Python)
SECRET_KEY="your_super_long_and_random_secret_key_here"
```

b) credentials.json file:

Go to your project in the Google Cloud Console.

Navigate to "APIs & Services" > "Credentials".

Create an "OAuth 2.0 Client ID" for a "Web application".

In the "Authorized redirect URIs" field, add the following:

http://127.0.0.1:8000/auth/callback

Download the JSON file, rename it to credentials.json, and place it in the project's root directory.

Usage
Run the FastAPI application using uvicorn:

```bash
uvicorn app.main:app --reload
```
The application will be available in your browser at http://127.0.0.1:8000.