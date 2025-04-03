from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime, timedelta
import threading
from pynput import mouse, keyboard
import time  # Ensure time module is imported

app = Flask(__name__)
app.secret_key = 'your_secret_key'

logger = None
stop_flag = threading.Event()


@app.route('/')
def index():
    session.clear()  # Clear the session when the application starts
    default_output_path = "C:\\Users\\F7OUTO9\\Documents\\Inactivity_Logging"
    if 'monitoring' not in session:
        session['monitoring'] = False
    monitoring = session.get('monitoring', False)
    return render_template('index.html', default_output_path=default_output_path, monitoring=monitoring, datetime=datetime)

@app.route('/start', methods=['POST'])
def start():
    global logger, stop_flag
    file_path = request.form.get('file_path')
    end_time_str = request.form.get('end_time')

    print(f"Received file_path: {file_path}")
    print(f"Received end_time_str: {end_time_str}")

    # Set default end time to 11:59:59 PM if no value is provided
    if end_time_str:
        try:
            end_time = datetime.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
        except ValueError:
            return "Invalid date format. Please use 'mm/dd/yyyy hh:mm:ss'.", 400
    else:
        current_time = datetime.now()
        end_time = current_time.replace(hour=23, minute=59, second=59, microsecond=0)

    print(f"Parsed end_time: {end_time}")

    if not file_path:
        return "File path must be provided", 400

    # Ensure the file_path is a valid file path
    if os.path.isdir(file_path):
        # Generate a dynamic file name based on the current date and time
        timestamp = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
        file_path = os.path.join(file_path, f"{timestamp}.txt")
        print(f"Updated file_path to: {file_path}")

    # Validate file path
    try:
        output_dir = os.path.dirname(file_path)
        print(f"Output directory: {output_dir}")
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
    except PermissionError:
        return "Permission denied: Unable to create the specified directory", 403
    except Exception as e:
        return f"Error: {e}", 400

    # Start the monitoring process
    logger = InactivityLogger(output_file=file_path, end_time=end_time, stop_flag=stop_flag)
    stop_flag.clear()
    threading.Thread(target=logger.start).start()

    # Set monitoring status to True
    session['monitoring'] = True
    print("Monitoring started successfully.")
    return redirect(url_for('index'))


@app.route('/stop', methods=['POST'])
def stop():
    global logger, stop_flag
    if logger and not stop_flag.is_set():
        stop_flag.set()
        logger.stop()

    # Set monitoring status to False
    session['monitoring'] = False
    print("Monitoring stopped successfully.")
    return redirect(url_for('index'))


@app.route('/process_logs', methods=['GET'])
def process_logs():
    default_output_path = "C:\\Users\\F7OUTO9\\Documents\\Inactivity_Logging"
    return render_template('process_logs.html', default_output_path=default_output_path)


@app.route('/load_logs', methods=['POST'])
def load_logs():
    log_directory = request.form.get('log_directory')

    if not log_directory or not os.path.exists(log_directory):
        return "Log directory must be provided and exist", 400

    # Get all files in the directory and sort them by last modified time (newest first)
    log_files = sorted(
        [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))],
        key=lambda x: os.path.getmtime(os.path.join(log_directory, x)),
        reverse=True
    )

    return render_template('process_logs.html', log_files=log_files, default_output_path=log_directory)


@app.route('/process_log', methods=['POST'])
def process_log():
    log_file = request.form.get('log_file')
    log_directory = request.form.get('log_directory')

    if not log_directory or not log_file:
        return "Log directory and log file must be provided", 400

    log_file_path = os.path.join(log_directory, log_file)

    total_inactivity = timedelta()
    start_time = None
    stop_time = None

    print(f"Processing log file: {log_file_path}")

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                print(f"Reading line: '{line}'")

                if 'Script started at:' in line:
                    parts = line.split('Script started at: ')
                    if len(parts) > 1:
                        start_time = parts[1].strip()
                    print(f"Detected start time: {start_time}")

                elif 'Script stopped at:' in line:
                    parts = line.split('Script stopped at: ')
                    if len(parts) > 1:
                        stop_time = parts[1].strip()
                    print(f"Detected stop time: {stop_time}")

                elif 'Total Inactivity Duration:' in line:
                    print("Found 'Total Inactivity Duration:'")
                    parts = line.split('Total Inactivity Duration: ')
                    print(f"Inactivity parts: {parts}")
                    if len(parts) > 1:
                        inactivity_duration_str = parts[1].strip()
                        print(f"Inactivity Duration String: '{inactivity_duration_str}'")
                        try:
                            h, m, s = map(float, inactivity_duration_str.split(':'))
                            total_inactivity += timedelta(hours=int(h), minutes=int(m), seconds=s,
                                                          milliseconds=round((s % 1) * 1000))
                            print(f"Added inactivity duration: {h}:{m}:{s}, Total so far: {total_inactivity}")
                        except ValueError as ve:
                            print(f"Error parsing inactivity duration: {ve}")

    print(f"Start Time: {start_time}, Stop Time: {stop_time}, Final Total Inactivity: {total_inactivity}")

    return render_template('show_log.html', start_time=start_time, stop_time=stop_time,
                           total_inactivity=total_inactivity)


@app.route('/view_file', methods=['POST'])
def view_file():
    log_file = request.form.get('log_file')
    log_directory = request.form.get('log_directory')

    if not log_directory or not log_file:
        return "Log directory and log file must be provided", 400

    log_file_path = os.path.join(log_directory, log_file)

    if not os.path.exists(log_file_path):
        return f"File '{log_file}' does not exist in the directory '{log_directory}'", 404

    with open(log_file_path, 'r') as file:
        file_contents = file.read()

    return render_template('view_file.html', log_file=log_file, file_contents=file_contents)

class InactivityLogger:
    def __init__(self, output_file=None, end_time=None, stop_flag=None):
        self.output_file = output_file or "output.txt"
        self.end_time = end_time
        self.stop_flag = stop_flag
        self.inactivity_start = None
        self.stopped = False
        self.active = threading.Event()
        self.active.set()

        # Ensure the directory exists
        output_dir = os.path.dirname(self.output_file)
        print(f"Initializing InactivityLogger with output_file: {self.output_file}")
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")

        start_time = datetime.now()
        self.log_output(f"Script started at: {start_time}\n")

    def log_output(self, message):
        try:
            print(f"Writing to log file: {self.output_file}")
            with open(self.output_file, "a") as file:
                file.write(message + "\n")
        except PermissionError as e:
            print(f"PermissionError: {e}")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def keyboard_activity(self, key):
        self.reset_activity()

    def mouse_activity(self, x, y, button, pressed):
        self.reset_activity()

    def reset_activity(self):
        if self.inactivity_start is not None:
            inactivity_end = datetime.now()
            inactivity_duration = inactivity_end - self.inactivity_start
            if inactivity_duration >= timedelta(minutes=5):
                log_content = f"Inactivity Start: {self.inactivity_start} | Inactivity End: {inactivity_end} | Total Inactivity Duration: {inactivity_duration}"
                self.log_output(log_content)
        self.inactivity_start = None
        self.active.set()

    def monitor_inactivity(self):
        while True:
            if self.stop_flag.is_set():
                self.stop()
                break

            current_time = datetime.now()
            if self.end_time and current_time > self.end_time:
                self.stop()
                break

            if not self.active.is_set():
                if self.inactivity_start is None:
                    self.inactivity_start = current_time
            else:
                if self.inactivity_start is not None:
                    inactivity_end = current_time
                    inactivity_duration = inactivity_end - self.inactivity_start
                    if inactivity_duration >= timedelta(minutes=5):
                        log_content = f"Inactivity Start: {self.inactivity_start} | Inactivity End: {inactivity_end} | Total Inactivity Duration: {inactivity_duration}"
                        self.log_output(log_content)
                    self.inactivity_start = None
                self.active.clear()

            time.sleep(1)

    def start(self):
        self.stop_flag.clear()
        mouse_listener = mouse.Listener(on_click=self.mouse_activity)
        keyboard_listener = keyboard.Listener(on_press=self.keyboard_activity)
        mouse_listener.start()
        keyboard_listener.start()
        inactivity_thread = threading.Thread(target=self.monitor_inactivity)
        inactivity_thread.start()
        mouse_listener.join()
        keyboard_listener.join()
        inactivity_thread.join()

    def stop(self):
        if self.stopped:
            return
        self.stopped = True
        stop_time = datetime.now()
        self.log_output(f"Script stopped at: {stop_time}\n")


if __name__ == '__main__':
    app.run(debug=True, port=5001)