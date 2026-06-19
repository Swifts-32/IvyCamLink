import socket
import cv2
import numpy as np
import struct
import subprocess
import time
import sys

class IvyCamCapture:
    def __init__(self, port=5001, ip='127.0.0.1'):
        self.port = port
        self.ip = ip
        self.sock = None
        self.is_running = False

    def _setup_adb_ports(self):
        """Automates the entire ADB configuration workflow cleanly from code."""
        print(f"Configuring local physical Android ADB connections on port {self.port}...")
        try:
            # Clear out historic channels
            subprocess.run(["adb", "forward", "--remove-all"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Apply the new active bridge link tunnel target
            subprocess.run(["adb", "forward", f"tcp:{self.port}", f"tcp:{self.port}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✓ ADB forward port configurations active [tcp:{self.port}]!")
        except subprocess.CalledProcessError as e:
            print(f"✗ ADB configuration failed: {e.stderr.decode().strip()}")
            print("Make sure your phone is connected and USB Debugging is turned on.")
            sys.exit(1)
        except FileNotFoundError:
            print("✗ ADB executable could not be found. Please check your system PATH.")
            sys.exit(1)

    def open(self):
        """Establishes the connection to the headless service and starts the camera."""
        self._setup_adb_ports()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        connected = False
        for attempt in range(5):
            try:
                self.sock.connect((self.ip, self.port))
                connected = True
                break
            except socket.error:
                print(f"Waiting for headless service... (Attempt {attempt+1}/5)")
                time.sleep(1)
                
        if not connected:
            print("✗ Could not connect to the Android background app service.")
            return False

        print("✓ Connected to headless server!")
        print("Sending Remote Wake Command: START (0x01)")
        self.sock.sendall(bytes([0x01]))
        self.is_running = True
        return True

    def read(self):
        if not self.is_running or self.sock is None:
            return False, None

        try:
            # OPTIMIZATION: Check if there's an overwhelming amount of data waiting in the buffer.
            # If our script falls behind, we skip old packets to snap straight back to the real-time live frame.
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            
            # Read image data length header
            header = self.sock.recv(4)
            if not header or len(header) < 4:
                return False, None
                
            frame_len = struct.unpack('>I', header)[0]
            
            # Retrieve payload bytes
            frame_data = bytearray()
            while len(frame_data) < frame_len:
                packet = self.sock.recv(frame_len - len(frame_data))
                if not packet:
                    break
                frame_data.extend(packet)
                
            if len(frame_data) < frame_len:
                return False, None

            # Convert to OpenCV compatible image array
            np_data = np.frombuffer(frame_data, dtype=np.uint8)
            cv_frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            
            if cv_frame is None:
                return False, None
                
            return True, cv_frame

        except Exception as e:
            print(f"Error reading stream frame: {e}")
            return False, None

    def release(self):
        """Gracefully turns off the remote phone camera and closes the socket."""
        if self.sock:
            print("\nSending Remote Shutdown Command: STOP (0x02)")
            try:
                self.sock.sendall(bytes([0x02]))
                time.sleep(0.1)  # Brief processing pause window
            except Exception:
                pass
            self.sock.close()
            self.sock = None
        self.is_running = False
        print("Network pipeline closed down successfully.")

    def set_focus(self, percentage):
        """
        Sets the camera focus distance manually.
        :param percentage: Integer from 0 (Infinity) to 100 (Macro / Closest Focus).
        """
        if not self.is_running or self.sock is None:
            return False

        # Constrain boundary values securely between 0 and 100
        percentage = max(0, min(100, int(percentage)))
        
        try:
            # Send Focus Command (0x03) followed by the focus percentage value byte
            self.sock.sendall(bytes([0x03, percentage]))
            return True
        except Exception as e:
            print(f"Failed to send focus command: {e}")
            return False