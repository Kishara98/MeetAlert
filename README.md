
# Google Meet Notification Desktop Widget

A simple Python-based desktop widget that fetches upcoming Google Meet meetings from your Google Calendar and notifies you of them. The widget utilizes the Google Calendar API and Tkinter to display meeting information on your desktop.



## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)

---

## Features

- Displays upcoming Google Meet meetings directly on your desktop.
- Automatically fetches meetings from Google Calendar.
- Updates every hour to check for new meetings.
- Easy to use with a lightweight Tkinter-based UI.

## Prerequisites

Before running the widget, ensure you have the following installed on your system:

- Python 3.6 or later
- [Google Cloud Project](https://console.cloud.google.com/) with Google Calendar API enabled.
- Required Python libraries:
  - `google-api-python-client`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `tkinter` (comes pre-installed with Python on most platforms)

## Installation

1. **Clone this repository** to your local machine:
    ```bash
    git clone https://github.com/Kishara98/MeetAlert.git
    cd MeetAlert-master
    ```

2. **Create a Google Cloud Project** and enable the Google Calendar API:

   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Navigate to **APIs & Services** > **Library**, search for "Google Calendar API", and enable it.
   - Go to **Credentials** and create **OAuth 2.0 Client IDs** for a **Desktop App**.
   - Download the `credentials.json` file and place it in the root directory of this project.

3. **Install the required dependencies** using pip:
    ```bash
    pip install -r requirements.txt
    ```

    *(Create a `requirements.txt` with the following content)*:
    ```
    google-api-python-client
    google-auth-httplib2
    google-auth-oauthlib
    tk
    ```

4. **Run the application**:
    ```bash
    python desktop_meeting_notifier.py
    ```

    The first time you run the app, it will open a browser window asking you to authenticate with your Google account. After that, a `token.json` file will be generated for subsequent runs.

## Usage

Once the app is authenticated, it will fetch upcoming Google Meet meetings for the next hour and display them in a Tkinter-based widget on your desktop. The widget refreshes the meeting list at regular intervals.



## Customization

You can modify the widget’s refresh interval or display settings by editing the `show_meetings()` function inside the Python script.

### Adding Auto-Refresh (Optional)

If you want the widget to automatically refresh every 5 minutes, you can add the following line to the `show_meetings()` function:

```python
root.after(300000, show_meetings)  # Refresh every 5 minutes
```

## Contributing

Feel free to contribute to the project by submitting issues or pull requests. Here's how you can get started:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

