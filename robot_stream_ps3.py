import socket
import subprocess

UDP_PORT = 7123
VIDEO_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

print("Waiting for client HELLO...")
data, client_addr = sock.recvfrom(1024)

client_ip = client_addr[0]
print("Client connected:", client_ip)

cmd = [
    "ffmpeg",

    "-f", "v4l2",
    "-input_format", "yuyv422",
    "-video_size", "640x480",
    "-framerate", "30",          
    "-i", "/dev/video0",        

    "-vcodec", "libx264",
    "-preset", "ultrafast",
    "-tune", "zerolatency",
    "-g", "30",
    "-pix_fmt", "yuv420p",

    "-f", "rtp",
    "-sdp_file", "stream_ps3.sdp",
    f"rtp://{client_ip}:5000"
]

print("Starting video stream...")
subprocess.run(cmd)
