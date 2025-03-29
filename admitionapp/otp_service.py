import requests
import random

# Your SMS API credentials and URL
AUTH_KEY = "2912AJeMdgzzYFoa642d4643P43"
API_BASE_URL = "http://sms.moplet.com/api/sendhttp.php"
SENDER_ID = "IMCBSG"
DLT_TE_ID = "1707174317520989989"

# OTP storage (in-memory for simplicity, consider using cache or database in production)
otp_storage = {}

def generate_otp():
    """Generate a 6-digit random OTP"""
    return str(random.randint(100000, 999999))

def send_otp(mobile):
    """Generate and send OTP via SMS using the provided Moplet SMS API"""
    # Generate new OTP
    otp = generate_otp()
    
    # Store OTP for verification later
    otp_storage[mobile] = otp
    
    # Create the OTP message with your specific format
    message = f"OTP for Login to Online Admission Form Application is {otp} .Do not Share to anyone. IMC BUSINESS SOLUTIONS"
    
    # Prepare parameters for the API request
    params = {
        "authkey": AUTH_KEY,
        "mobiles": mobile,
        "message": message,
        "sender": SENDER_ID,
        "route": "4",
        "country": "91",
        "DLT_TE_ID": DLT_TE_ID
    }
    
    print(f"Sending OTP to {mobile}: {otp}")  # Debugging
    
    # Make the API request
    response = requests.get(API_BASE_URL, params=params)
    
    print(f"API Response: {response.text}")  # Debugging
    
    # Check if the message was sent successfully based on the response
    # You may need to adjust this based on the actual response format from your API
    if response.status_code == 200:
        return {"status": "success", "message": "OTP sent via SMS"}
    else:
        return {"status": "failed", "message": f"Failed to send OTP: {response.text}"}

def verify_otp(mobile, entered_otp):
    """Verify if the entered OTP matches the one sent to the mobile number"""
    if mobile in otp_storage and otp_storage[mobile] == entered_otp:
        # Clear OTP after successful verification
        del otp_storage[mobile]
        return True
    return False