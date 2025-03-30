import time
import threading
import http.server
import socketserver
from picamera2 import Picamera2
from io import BytesIO
from PIL import Image

PORT = 8000  # HTTP Port

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

class StreamingHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/video_feed":
            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=frame")
            self.end_headers()

            try:
                while True:
                    # Capture a frame from Picamera2
                    frame = picam2.capture_array("main")
                
                    # Convert frame to JPEG
                    buffer = BytesIO()
                    Image.fromarray(frame).save(buffer, format="JPEG")
                    jpg_bytes = buffer.getvalue()

                    self.wfile.write(b"--frame\r\n")
                    self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                    self.wfile.write(jpg_bytes)
                    self.wfile.write(b"\r\n")
                    time.sleep(0.1)  # 10 FPS
            except (BrokenPipeError, ConnectionResetError):
                print("Client disconnected.")
        
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("0.0.0.0", PORT), StreamingHandler) as server:
    print(f"Streaming server started at http://0.0.0.0:{PORT}/video_feed")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server.")
