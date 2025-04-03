# Monitoring Activity

This project is a Flask-based application designed to monitor user inactivity and log it to a file. It provides a web interface for starting and stopping the monitoring process, processing log files, and viewing inactivity reports.

## Features

- **Start and Stop Monitoring:** Allows users to start and stop monitoring inactivity.
- **Dynamic Log File Creation:** Automatically generates log files with timestamps or uses a user-specified file path.
- **Inactivity Logging:** Logs periods of inactivity longer than 5 minutes.
- **Log Processing:** Processes log files to calculate total inactivity duration and displays start and stop times.
- **View Logs:** Allows users to view the contents of specific log files.
- **Quick Links Section:** Provides a section for commonly used links.

## File Overview

1. **app.py**

   This is the main Flask application file. It contains the following routes and logic:

   - `/ (Index Route):`
     - Displays the main page with options to start or stop monitoring.
     - Initializes the `session['monitoring']` variable to False when the application starts.

   - `/start:`
     - Starts the monitoring process.
     - Accepts a file path and an optional end time from the user.
     - Dynamically generates a log file name if a directory is provided.
     - Sets `session['monitoring']` to True.

   - `/stop:`
     - Stops the monitoring process.
     - Sets `session['monitoring']` to False.

   - `/process_logs:`
     - Displays a page for processing log files.

   - `/load_logs:`
     - Loads log files from a specified directory and displays them in the interface.

   - `/process_log:`
     - Processes a specific log file to calculate total inactivity duration and displays start and stop times.

   - `/view_file:`
     - Displays the contents of a specific log file.

2. **Requirements**

   - Python 3.10 or higher
   - Flask
   - Pynput

3. **Installation**

   1. Clone the repository:

      ```bash
      git clone https://github.com/your-username/MonitoringActivity.git
      cd MonitoringActivity
      ```

   2. Create a virtual environment:

      ```bash
      python -m venv venv
      ```

   3. Activate the virtual environment:
      - On Windows:

        ```bash
        venv\Scripts\activate
        ```

      - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

   4. Install the required dependencies:

      ```bash
      pip install -r requirements.txt
      ```

4. **Usage**

   1. Start the application:

      ```bash
      python app.py
      ```

   2. Open a browser and navigate to [http://127.0.0.1:5001](http://127.0.0.1:5001).
   3. Use the interface to start/stop monitoring, process logs, and view log files.


## Example Log File
A sample log file might look like this:

Script started at: 03/31/2025 10:00:00
Inactivity Start: 03/31/2025 10:15:00 | Inactivity End: 03/31/2025 10:20:00 | Total Inactivity Duration: 0:05:00
Script stopped at: 03/31/2025 11:00:00


## Troubleshooting

- **"Monitoring is currently running..." message appears incorrectly:**
  - Ensure the `session['monitoring']` variable is properly initialized in the / route.

- **PermissionError when creating log files:**
  - Verify that the application has write permissions for the specified directory.

- **Invalid date format error:**
  - Ensure the end time is entered in the format mm/dd/yyyy hh:mm:ss.


