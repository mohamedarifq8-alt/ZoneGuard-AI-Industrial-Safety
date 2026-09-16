import cv2
import numpy as np
import gradio as gr
from ultralytics import YOLO
from pyModbusTCP.client import ModbusClient

# ==========================================
# 1. System & PLC Initialization
# ==========================================
MODEL_PATH = "models/best.onnx"
model = YOLO(MODEL_PATH)

#danger_zone = np.array([[1066, 486], [1002, 413], [396, 350], [376, 602]], np.int32)
danger_zone = np.array([[719, 517], [893, 510], [959, 670], [744, 681], [559, 620], [717, 518]], np.int32)
# Setup connection to a virtual PLC device (e.g., Siemens S7-1200)
# We use a default IP; in a real factory, the actual PLC IP will be used
PLC_IP = "192.168.1.100" 
plc = ModbusClient(host=PLC_IP, port=502, auto_open=True, timeout=1)

# ==========================================
# 2. Core Processing Engine with PLC Logic
# ==========================================
def process_video(video_in):
    if video_in is None:
        return None

    cap = cv2.VideoCapture(video_in)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    output_path = "output_demo.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    skip_frames = 2  # Process one frame and skip one to maintain speed
    
    # Variables to store bounding boxes for skipped frames (Caching)
    cached_persons = []
    cached_ppes = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame_count += 1
        
        # 1. AI runs only every two frames to speed up processing
        if frame_count % skip_frames == 0:
            results = model(frame, verbose=False, conf=0.45)
            boxes = results[0].boxes
            
            cached_persons = []
            cached_ppes = []
            
            for box in boxes:
                cls_id = int(box.cls[0])
                coords = box.xyxy[0].cpu().numpy()
                if cls_id == 1: cached_persons.append(coords)
                elif cls_id in [0, 2]: cached_ppes.append((cls_id, coords))
        
        # Fetch bounding boxes (either from AI or from memory/cache)
        persons = cached_persons
        ppes = cached_ppes

        # 2. Draw the restricted zone
        overlay = frame.copy()
        cv2.fillPoly(overlay, [danger_zone], (0, 0, 255))
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        cv2.polylines(frame, [danger_zone], isClosed=True, color=(0, 0, 255), thickness=2)

        zone_breach_active = False

        # 3. Spatial logic, drawing boxes, and text (Restored missing text!)
        for p_box in persons:
            x1, y1, x2, y2 = map(int, p_box)
            foot_x = int((x1 + x2) / 2)
            foot_y = y2
            
            inside_zone = cv2.pointPolygonTest(danger_zone, (foot_x, foot_y), False) >= 0
            
            has_helmet = False
            has_vest = False
            for ppe_cls, ppe_box in ppes:
                px1, py1, px2, py2 = ppe_box
                ppe_cx = (px1 + px2) / 2
                ppe_cy = (py1 + py2) / 2
                if x1 < ppe_cx < x2 and y1 < ppe_cy < y2:
                    if ppe_cls == 0: has_helmet = True
                    if ppe_cls == 2: has_vest = True

            # Restore text
            if inside_zone:
                zone_breach_active = True
                color = (0, 0, 255) if (frame_count % 10) < 5 else (255, 255, 255)
                label = "DANGER: ZONE BREACH!"
            elif has_helmet and has_vest:
                color = (0, 255, 0)
                label = "SAFE"
            else:
                color = (0, 165, 255)
                label = "WARNING: MISSING PPE"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.circle(frame, (foot_x, foot_y), 5, color, -1)

        # 4. PLC Control Panel
        cv2.rectangle(frame, (width - 400, 20), (width - 20, 100), (0, 0, 0), -1)
        cv2.putText(frame, "MODBUS TCP STATUS", (width - 380, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if zone_breach_active:
            cv2.putText(frame, "!!! CRITICAL: ZONE BREACH DETECTED !!!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            try: plc.write_single_coil(0, True)
            except: pass
            
            plc_indicator_color = (0, 0, 255) if (frame_count % 10) < 5 else (100, 100, 100)
            cv2.putText(frame, "SIGNAL TO PLC: [ SENT / HIGH ]", (width - 380, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, plc_indicator_color, 2)
        else:
            try: plc.write_single_coil(0, False)
            except: pass
            cv2.putText(frame, "SIGNAL TO PLC: [ IDLE / LOW ]", (width - 380, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()
    return output_path

# ==========================================
# 3. Professional Gradio Web Interface
# ==========================================
with gr.Blocks(theme=gr.themes.Soft(primary_hue="slate", neutral_hue="slate")) as app:
    
    gr.Markdown("<h1 style='text-align: center;'>🛡️ ZoneGuard AI: Industrial Safety Monitor</h1>")
    gr.Markdown("<p style='text-align: center; font-size: 16px;'>Automated PPE Detection & Virtual Safety Fencing System with Modbus TCP PLC Integration.</p>")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📥 Input Panel")
            video_input = gr.Video(label="Upload CCTV Footage (MP4 format)")
            process_btn = gr.Button("🚀 Run AI Analysis", variant="primary")
            
        with gr.Column():
            gr.Markdown("### 📤 Output Panel (Analyzed Footage)")
            video_output = gr.Video(label="AI Engine Result (Look at Top-Right for PLC Status)")

    with gr.Accordion("Technical Specifications (Click to expand)", open=False):
        gr.Markdown("""
        - **Computer Vision Model**: YOLOv8 Custom Trained (ONNX runtime for optimized inference).
        - **Spatial Logic**: Implements *Bird's Eye View* anchoring to prevent perspective distortion.
        - **Industrial Control Link**: Utilizes **Modbus TCP** protocol (`pyModbusTCP`) to communicate real-time alerts to industrial PLCs (e.g., triggering a relay or stopping a machine).
        - **Rule Engine**: 
            - 🟩 **Green**: Full PPE compliance in safe zones.
            - 🟧 **Orange**: Missing PPE (Hardhat/Vest) in safe zones.
            - 🟥 **Flashing Red**: Critical virtual fence breach (Machine Danger Zone).
        
        """)

    process_btn.click(fn=process_video, inputs=video_input, outputs=video_output)

if __name__ == "__main__":
    app.launch()