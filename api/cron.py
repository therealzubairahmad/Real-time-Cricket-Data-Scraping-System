from http.server import BaseHTTPRequestHandler
import sys
import os

# Add parent directory to path so we can import from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler import run_scheduler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # Run the scheduler
        try:
            run_scheduler()
            self.wfile.write('Scheduler executed successfully'.encode())
        except Exception as e:
            self.wfile.write(f'Error executing scheduler: {str(e)}'.encode())
