import requests
import time
from twilio.rest import Client
from datetime import datetime

# Configuration
WEBSITE_URL = "https://example.com"  # Replace with your website URL
CHECK_INTERVAL = 300  # 5 minutes in seconds
TIMEOUT = 10  # Timeout for the request in seconds

# Twilio SMS Configuration (replace with your credentials)
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio phone number
ADMIN_PHONE_NUMBER = "+1234567890"   # Admin phone number to receive alerts

# Status tracking
last_status = None
consecutive_failures = 0
failure_threshold = 2  # Number of consecutive failures before sending alert

def check_website():
    global last_status, consecutive_failures
    
    try:
        response = requests.get(WEBSITE_URL, timeout=TIMEOUT)
        
        # Check if status code indicates success (2xx) or redirect (3xx)
        if response.status_code < 400:
            current_status = "UP"
            log_status(current_status, response.status_code)
            
            # If site was previously down, notify that it's back up
            if last_status == "DOWN":
                send_sms(f"Website is back UP: {WEBSITE_URL}\n"
                        f"Status code: {response.status_code}")
            
            consecutive_failures = 0
            last_status = current_status
            return True
        
        # Handle 4xx and 5xx status codes
        current_status = "DOWN"
        log_status(current_status, response.status_code)
        consecutive_failures += 1
        
    except requests.exceptions.RequestException as e:
        current_status = "DOWN"
        log_status(current_status, str(e))
        consecutive_failures += 1
    
    # Check if we need to send an alert
    if consecutive_failures >= failure_threshold and last_status != "DOWN":
        send_sms(f"Website is DOWN: {WEBSITE_URL}\n"
                f"Error: {current_status} - {response.status_code if 'response' in locals() else e}")
    
    last_status = current_status
    return False

def log_status(status, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] Status: {status} - {details}"
    print(log_message)
    
    # Optionally write to a log file
    with open("website_monitor.log", "a") as f:
        f.write(log_message + "\n")

def send_sms(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )
        print(f"SMS alert sent to {ADMIN_PHONE_NUMBER}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")

def main():
    print(f"Starting website monitor for {WEBSITE_URL}")
    print(f"Checking every {CHECK_INTERVAL/60} minutes")
    
    while True:
        check_website()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()