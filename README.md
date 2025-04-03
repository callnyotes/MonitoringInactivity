# MonitoringInactivity

This project is a Flask-based application designed to monitor user inactivity and log it to a file. It provides a web interface for starting and stopping the monitoring process, processing log files, and viewing inactivity reports.

________________________________________

Features
•	Start and Stop Monitoring: Allows users to start and stop monitoring inactivity.
•	Dynamic Log File Creation: Automatically generates log files with timestamps or uses a user-specified file path.
•	Inactivity Logging: Logs periods of inactivity longer than 5 minutes.
•	Log Processing: Processes log files to calculate total inactivity duration and displays start and stop times.
•	View Logs: Allows users to view the contents of specific log files.
•	Quick Links Section: Provides a section for commonly used links.

________________________________________

File Overview
1. app.py
This is the main Flask application file. It contains the following routes and logic:
  •	/ (Index Route):
    o	Displays the main page with options to start or stop monitoring.
    o	Initializes the monitoring session variable to False when the application starts.
  •	/start:
    o	Starts the monitoring process.
    o	Accepts a file path and an optional end time from the user.
    o	Dynamically generates a log file name if a directory is provided.
    o	Sets session['monitoring'] to True.
  •	/stop:
    o	Stops the monitoring process.
    o	Sets session['monitoring'] to False.
  •	/process_logs:
    o	Displays a page for processing log files.
  •	/load_logs:
    o	Loads log files from a specified directory and displays them in the interface.
  •	/process_log:
    o	Processes a specific log file to calculate total inactivity duration and displays start and stop times.
  •	/view_file:
    o	Displays the contents of a specific log file.

2. index.html
This is the main HTML template for the application. It includes:
  •	A form to start monitoring with fields for file path and end time.
  •	A button to stop monitoring.
  •	A section to display the "Monitoring is currently running..." message when monitoring is active.
  •	A quick links section for commonly used URLs.

4. process_logs.html
This template displays the log files in a specified directory and allows users to select and process a specific log file.

5. show_log.html
This template displays the results of processing a log file, including:
  •	Start time.
  •	Stop time.
  •	Total inactivity duration.

7. view_file.html
This template displays the contents of a specific log file.

9. start_app.bat
A batch file to start the Flask application. It runs the app.py file on port 5001.

________________________________________

How It Works
1. Starting the Application
  •	Run the start_app.bat file to start the Flask application.
  •	Open a browser and navigate to http://127.0.0.1:5001.

2. Starting Monitoring
  •	Enter a file path in the "File Path" field. If a directory is provided, a log file with a timestamped name will be created in that directory.
  •	Optionally, enter an end time in the format mm/dd/yyyy hh:mm:ss. If no end time is provided, monitoring will stop at 11:59:59 PM of the current day.
  •	Click the "Start Monitoring" button to begin monitoring.

3. Stopping Monitoring
  •	Click the "Stop Monitoring" button to stop the monitoring process.

4. Processing Logs
  •	Navigate to the "Log Processing Page" by clicking the corresponding button.
  •	Enter the directory containing the log files and load the logs.
  •	Select a log file to process and view the total inactivity duration, start time, and stop time.

5. Viewing Logs
  •	Select a log file from the list and view its contents.

________________________________________

Requirements
•	Python 3.10 or higher
•	Flask
•	Pynput

________________________________________

Installation
1.	Clone the repository:
      git clone https://github.com/your-username/MonitoringActivity.git
      cd MonitoringActivity

2.	Create a virtual environment:
      python -m venv venv

3.	Activate the virtual environment:
  o	On Windows:
      venv\Scripts\activate
  o	On macOS/Linux:
      source venv/bin/activate

4.	Install the required dependencies:
      pip install -r requirements.txt

________________________________________

Usage
1.	Start the application:
      python app.py

2.	Open a browser and navigate to http://127.0.0.1:5001.

3.	Use the interface to start/stop monitoring, process logs, and view log files.

________________________________________

Example Log File
A sample log file might look like this:
Script started at: 03/31/2025 10:00:00
Inactivity Start: 03/31/2025 10:15:00 | Inactivity End: 03/31/2025 10:20:00 | Total Inactivity Duration: 0:05:00
Script stopped at: 03/31/2025 11:00:00

________________________________________

Troubleshooting
•	"Monitoring is currently running..." message appears incorrectly:
    o	Ensure the session['monitoring'] variable is properly initialized in the / route.
•	PermissionError when creating log files:
    o	Verify that the application has write permissions for the specified directory.
•	Invalid date format error:
    o	Ensure the end time is entered in the format mm/dd/yyyy hh:mm:ss.

