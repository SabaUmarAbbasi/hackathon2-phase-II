import requests
import time

# Start the server in a subprocess
import subprocess
server_process = subprocess.Popen(['python3', 'start_backend.py'])

# Wait a bit for the server to start
time.sleep(5)

# Test the registration endpoint
try:
    response = requests.post(
        'http://localhost:8000/api/auth/register',
        json={'email': 'test@example.com', 'password': 'testpassword'}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Kill the server process
server_process.terminate()
server_process.wait()