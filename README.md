# IvyCamLink

A lightweight Python module that automates ADB bridging and connects straight to headless Android hosts to ingest high-speed camera frame arrays natively inside OpenCV.

## 📦 Features

* **Zero Terminal Overhead**: Automatically flushes, registers, and establishes your local `adb forward` port routing entirely from code.
* **Remote Hardware Control**: Sends instant upstream control triggers (`0x01` to START / `0x02` to STOP) to manage remote phone camera deployment lifetimes efficiently.
* **OpenCV Drop-In Compatible**: Implements a standard class architecture matching the familiar `cv2.VideoCapture` layout structure (`open()`, `read()`, `release()`).

## 📥 Installation

Ensure you have your core vision dependencies configured before importing the module wrapper:

```bash
pip install opencv-python numpy