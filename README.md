# 🛡️ ZoneGuard AI: Industrial Safety & Modbus TCP System

## 📌 Project Overview
ZoneGuard AI is a comprehensive, production-ready Computer Vision system engineered specifically for industrial and manufacturing safety. The system continuously analyzes real-time CCTV feeds to detect workers and ensure strict adherence to PPE (Personal Protective Equipment) protocols, specifically tracking hardhats and safety vests.

Beyond standard detection, the system bridges software and industrial hardware. It monitors mathematically defined "restricted machine zones" using perspective-aware spatial logic. Upon detecting a safety breach, it instantly transmits **Modbus TCP** signals to connected PLCs (Programmable Logic Controllers) to trigger alarms or halt machinery.

## 📊 Dataset & AI Training
The high accuracy of this system is driven by a highly specialized, custom dataset. The data was meticulously collected, merged, and modified from various diverse sources by **Mohammed alsimy**. By curating, filtering, and re-annotating these datasets to reflect actual factory lighting, angles, and conditions, the resulting YOLOv8 model achieves robust performance in real-world industrial environments.

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
```

## 📂 File Directory & Functionality
*   `models/best_production.onnx`: The compiled and optimized AI weights ready for fast inference without requiring PyTorch.
*   `training/train_yolov8.py`: The original scripts detailing the custom dataset preparation and the YOLOv8 model training process.
*   `app.py`: The main application file containing the Gradio interactive web interface and the Modbus PLC integration logic.
*   `main.py`: The core standalone detection script for processing video streams locally.
*   `calibrate.py`: A utility script used to draw and define the precise pixel coordinates of the restricted danger polygons on the video frame.
*   `requirements.txt`: The exact list of Python libraries and versions needed to run the project.
*   `Dockerfile`: The blueprint for packaging the entire system into a secure, portable container for edge servers.
*   `.gitignore` & `.dockerignore`: Security and optimization files to prevent uploading large media or local caches to repositories.

## 🚀 How to Run (Local Environment)
1. **Clone the repository:**
   ```bash
   git clone [https://github.com//mohamedarifq8-alt/ZoneGuard-AI-Industrial-Safety.git](https://github.com//mohamedarifq8-alt/ZoneGuard-AI-Industrial-Safety.git)
   cd ZoneGuard-AI-Industrial-Safety
