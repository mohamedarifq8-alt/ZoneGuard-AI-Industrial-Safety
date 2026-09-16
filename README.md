# 🛡️ ZoneGuard AI: Industrial Safety & Modbus TCP System
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Vision-E21937)](https://github.com/ultralytics/ultralytics)
[![Modbus TCP](https://img.shields.io/badge/Modbus_TCP-Protocol-F28500)](https://pymodbustcp.readthedocs.io/)
[![Gradio](https://img.shields.io/badge/Gradio-Web_UI-FF7C00)](https://gradio.app)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-Inference-005CED?logo=onnx&logoColor=white)](https://onnxruntime.ai)
[![Roboflow](https://img.shields.io/badge/Roboflow-Custom_Dataset-6400FF)](https://universe.roboflow.com/mohamed-arif/zoneguard_production_data)


## 📌 Project Overview
**ZoneGuard AI** is a comprehensive, production-ready Computer Vision system engineered specifically for industrial and manufacturing safety. The system continuously analyzes real-time CCTV feeds to detect workers and ensure strict adherence to PPE (Personal Protective Equipment) protocols, specifically tracking hardhats and safety vests.

Beyond standard detection, the system bridges software and industrial hardware. It monitors mathematically defined "restricted machine zones" using perspective-aware spatial logic. Upon detecting a safety breach, it instantly transmits **Modbus TCP** signals to connected PLCs (Programmable Logic Controllers) to trigger alarms or halt machinery.


<img width="1904" height="942" alt="Screenshot 2026-09-16 230604" src="https://github.com/user-attachments/assets/030cadd3-6784-452c-bb02-1c4c617648f9" />
---

## 📊 Dataset & AI Training
The high accuracy of this system is driven by a highly specialized, custom dataset. We meticulously collected, merged, and modified data from various diverse sources to suit the project's needs. By curating, filtering, and re-annotating these datasets to reflect actual factory lighting, angles, and conditions, the resulting YOLOv8 model achieves robust performance in real-world industrial environments.

* **Dataset Link:** You can access the official dataset on Roboflow via [ZoneGuard Production Data](https://universe.roboflow.com/mohamed-arif/zoneguard_production_data).

---


## ⚙️ Core Features
*   **Custom AI Inference:** Optimized ONNX runtime (achieving 95% mAP50) for fast, accurate detection of Hardhats, Vests, and Workers.
*   **Spatial Geometry Logic:** Implements *Bird's Eye View* (Point Polygon Test) to eliminate perspective distortion and false positives in red-zone monitoring.
*   **PLC Hardware Integration:** Built-in Modbus TCP client (`pyModbusTCP`) to send immediate, real-time hardware interrupts to industrial controllers.
*   **Interactive Dashboard:** Containerized **Gradio** web interface for real-time CCTV video processing, testing, and PLC status visualization.
*   **Production Ready:** Fully containerized with Docker, utilizing lightweight `opencv-python-headless` for edge server deployment.

---

## 🛠️ Technology Stack
*   **AI / Computer Vision:** Python, Ultralytics YOLOv8, OpenCV
*   **Industrial Protocol:** Modbus TCP/IP
*   **Web UI & Deployment:** Gradio, Docker

---

## 📂 Project Structure
```text
ZoneGuard_Project/
├── models/
│   └── best.onnx         # Optimized AI weights (Available via Drive)
├── training/
│   └── train.py          # Original model training scripts
├── app.py                # Gradio Web UI & Modbus TCP logic
├── main.py               # Local core detection logic
├── requirements.txt      # Frozen Python dependencies
├── Dockerfile            # Containerization configuration
├── .gitignore            # Git tracking exclusions
└── .dockerignore         # Docker build exclusions
```

### 📄 Directory & Functionality Breakdown
*   `models/best_production.onnx`: The compiled and optimized AI weights ready for fast inference without requiring PyTorch.
*   `training/train_yolov8.py`: The original scripts detailing the custom dataset preparation and the YOLOv8 model training process.
*   `app.py`: The main application file containing the Gradio interactive web interface and the Modbus PLC integration logic.
*   `main.py`: The core standalone detection script for processing video streams locally.
*   `calibrate.py`: A utility script used to draw and define the precise pixel coordinates of the restricted danger polygons on the video frame.
*   `requirements.txt`: The exact list of Python libraries and versions needed to run the project.
*   `Dockerfile`: The blueprint for packaging the entire system into a secure, portable container for edge servers.
*   `.gitignore` & `.dockerignore`: Security and optimization files to prevent uploading large media or local caches to repositories.

---

## ⚡ Performance & Known Limitations
* **Processing Latency:** When processing high-resolution video files via the Gradio UI, a slight delay may be observed. This is an expected behavior caused by sequential frame-by-frame processing and Gradio's web-socket communication overhead. In this current iteration, inference is optimized for standard hardware without advanced hardware-specific compilation (e.g., TensorRT).

## 🔮 Future Enhancements & Scalability
While the current architecture robustly handles video files and simulated PLC signals, it is designed as a foundation for scalable enterprise deployment:
* **Multi-Camera RTSP Streams:** Upgrading the pipeline using Python `multithreading` and NVIDIA DeepStream to ingest and process live IP camera feeds from across the factory simultaneously.
* **Hardware Acceleration:** Compiling the ONNX weights into **TensorRT** engines to achieve ultra-low latency inference, essential for mission-critical machine shutdowns.
* **Live Recording & Alerting:** Integrating direct live-camera hooks to automatically record and save short video clips of safety breaches, alongside sending automated Email/SMS notifications.



## 🚀 How to Run (Local Environment)

### 1. Clone the repository
```bash
git clone https://github.com
cd ZoneGuard-AI-Industrial-Safety
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python app.py
```

---

## 🐳 Edge Server Deployment (Docker)

### 1. Build the Docker image
```bash
docker build -t zoneguard-ai .
```

### 2. Run the container
```bash
docker run -p 7860:7860 zoneguard-ai
```


## 🔗 Resources

### Model Weights (.onnx): [https://drive.google.com/file/d/143GWa60ptO086fEblpKrGwMheP-s6TEy/view?usp=sharing]

### Real-time Demo Video: [ضع_رابط_درايف_هنا]



## 👨‍💻 Author
**Mohammed Arif Mahyoub Haider**
*Electrical Engineer - Computer and Industrial Control*
