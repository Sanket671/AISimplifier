import subprocess
import threading
import time
import requests
import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_backend():
    """Run the Flask backend server"""
    try:
        # Change to backend directory and run app.py
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        os.chdir(backend_dir)
        
        print("Starting backend server...")
        # Use the same Python executable that's running this script
        subprocess.run([sys.executable, 'app.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Backend failed with error: {e}")
    except Exception as e:
        print(f"Unexpected error in backend: {e}")

def run_frontend():
    """Serve the frontend files"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='.', **kwargs)
    
    server = HTTPServer(("localhost", 3000), Handler)
    print("Frontend server running at http://localhost:3000")
    print("Open this URL in your browser to access the application")
    server.serve_forever()

def wait_for_backend():
    """Wait for backend to be ready"""
    print("Waiting for backend to start...")
    for i in range(45):  # Wait up to 15 seconds
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=1)
            if response.status_code == 200:
                print("✓ Backend is ready!")
                return True
        except requests.RequestException:
            if i % 3 == 0:  # Print status every 3 seconds
                print(f"Waiting... ({i+1}/15 seconds)")
            time.sleep(1)
    print("✗ Backend didn't start in time")
    return False

if __name__ == '__main__':
    print("Starting Legal Document Simplifier...")
    print("Backend will run on: http://localhost:5000")
    print("Frontend will run on: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers\n")
    
    # Start backend in a thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to be ready
    if wait_for_backend():
        # Start frontend
        run_frontend()
    else:
        print("Failed to start. Check backend logs for errors.")
        print("You can try running the backend manually:")
        print("cd backend && python app.py")
        sys.exit(1)
