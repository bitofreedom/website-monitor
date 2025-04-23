# Website Monitor

This project is a simple website monitoring tool that checks the availability of a specified website at regular intervals. It logs the status of the website and sends SMS alerts if the website goes down or comes back up.

## Features

- Monitors a specified website's status.
- Logs status updates with timestamps.
- Sends SMS alerts using Twilio when the website goes down or comes back up.

## Files

- `src/website_monitor.py`: Contains the main logic for monitoring the website's status.
- `requirements.txt`: Lists the dependencies required for the project.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: Documentation for the project.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd website-monitor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the Twilio SMS settings in `src/website_monitor.py`:
   - Replace `your_account_sid` and `your_auth_token` with your Twilio credentials.
   - Update `TWILIO_PHONE_NUMBER` and `ADMIN_PHONE_NUMBER` with the appropriate phone numbers.

4. Run the website monitor:
   ```
   python src/website_monitor.py
   ```

## Usage

The website monitor will check the specified website every 5 minutes (300 seconds) by default. You can modify the `CHECK_INTERVAL` in `src/website_monitor.py` to change the frequency of checks.

## License

This project is licensed under the MIT License.