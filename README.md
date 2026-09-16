# 🛡️ ZoneGuard AI: Industrial Safety & Modbus TCP System

## 📌 Project Overview
ZoneGuard AI is a production-ready Computer Vision system designed to enforce industrial safety protocols in real-time. Built specifically for manufacturing and factory environments, it uses a custom-trained **YOLOv8** model to detect workers and ensure PPE (Personal Protective Equipment) compliance.

What sets this project apart is its seamless integration with industrial hardware. Using perspective-aware spatial logic, it monitors restricted machine zones and instantly triggers **Modbus TCP** signals to Programmable Logic Controllers (PLCs) whenever a critical zone breach occurs, enabling immediate machine shutdown or alarm activation.

## ⚙️ Core Features
* **Custom AI Inference:** Optimized ONNX runtime (achieving 95% mAP50) for fast, accurate detection of Hardhats, Vests, and Workers.
* **Spatial Geometry Logic:** Implements *Bird's Eye View* (Point Polygon Test) to eliminate perspective distortion and false positives in red-zone monitoring.
* **PLC Hardware Integration:** Built-in Modbus TCP client (`pyModbusTCP`) to send immediate, real-time hardware interrupts to industrial controllers.
* **Interactive Dashboard:** Containerized **Gradio** web interface for real-time CCTV video processing, testing, and PLC status visualization.
* **Production Ready:** Fully containerized with Docker, utilizing lightweight `opencv-python-headless` for edge server deployment.

## 🛠️ Technology Stack
* **AI/Computer Vision:** Python, Ultralytics YOLOv8, OpenCV.
* **Industrial Protocol:** Modbus TCP/IP.
* **Web UI & Deployment:** Gradio, Docker.

## 📂 Project Structure
```text
ZoneGuard_Project/
├── models/
│   └── best.onnx      # Optimized AI weights (Available via Drive)
├── training/
│   └── train.py           # Original model training scripts
├── app.py                        # Gradio Web UI & Modbus TCP logic
├── main.py                       # Local core detection logic
├── requirements.txt              # Frozen Python dependencies
├── Dockerfile                    # Containerization configuration
├── .gitignore                    # Git tracking exclusions
└── .dockerignore                 # Docker build exclusions
