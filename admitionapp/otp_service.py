import requests
import random

# DXING API Credentials
DXING_SECRET = "7b8ae820ecb39f8d173d57b51e1fce4c023e359e"
DXING_ACCOUNT = "1741445642812b4ba287f5ee0bc9d43bbf5bbe87fb67cc5a0aa3836"
DXING_BASE_URL = "https://app.dxing.in/api/send/whatsapp"

# OTP storage (in-memory for simplicity, consider using cache or database in production)
otp_storage = {}

def generate_otp():
    """Generate a 6-digit random OTP"""
    return str(random.randint(100000, 999999))

def send_otp(mobile):
    """Generate and send OTP via WhatsApp using DXING API"""
    # Generate new OTP
    otp = generate_otp()
    
    # Store OTP for verification later
    otp_storage[mobile] = otp
    
    url = f"{DXING_BASE_URL}?secret={DXING_SECRET}&account={DXING_ACCOUNT}&recipient={mobile}&type=text&message=Your%20OTP%20is%20{otp}&priority=1"

    print(f"Sending OTP to {mobile}: {otp}")  # Debugging
    response = requests.get(url)

    print(f"DXING Response: {response.text}")  # Debugging

    try:
        response_data = response.json()
        if response.status_code == 200 and response_data.get("status") == "success":
            return {"status": "success", "message": "OTP sent via WhatsApp"}
        else:
            return {"status": "failed", "message": response_data.get("message", "Unknown error")}
    except Exception as e:
        return {"status": "failed", "message": f"Error parsing response: {e}"}

def verify_otp(mobile, entered_otp):
    """Verify if the entered OTP matches the one sent to the mobile number"""
    if mobile in otp_storage and otp_storage[mobile] == entered_otp:
        # Clear OTP after successful verification
        del otp_storage[mobile]
        return True
    return False