import cv2
import numpy as np
from ultralytics import YOLO

# ==========================================
# 1. Basic Settings
# ==========================================
MODEL_PATH = "models/best.onnx"
VIDEO_PATH = "videos/test_video.mp4"

print("[INFO] Loading YOLO model...")
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("[ERROR] Cannot open video file.")
    exit()

# ==========================================
# 2. Define Restricted Zone (Virtual Fence)
# ==========================================
# These are virtual (polygon) coordinates representing the danger zone around the machine.
# You will need to change these numbers to fit the machine dimensions in your video.
#danger_zone = np.array([[351, 425], [328, 531], [891, 500], [801, 412]], np.int32)
danger_zone = np.array([[719, 517], [893, 510], [959, 670], [744, 681], [559, 620], [717, 518]], np.int32)
#frame_count = 0  # Frame counter (used to create a blinking effect for the alarm)

# ==========================================
# 3. Main Processing Loop
# ==========================================
# New variables for speed control
frame_count = 0
skip_frames = 2  # Process one frame and skip two frames to speed up the video

while True:
    success, frame = cap.read()
    if not success:
        break
    
    frame_count += 1
    
    # --- Solve slowness issue: Skip frames ---
    # If the frame is not the one to be processed, skip to the next one immediately
    if frame_count % skip_frames != 0:
        continue 
    
    # --- Solve confusion issue: Add confidence threshold conf=0.55 ---
    # This prevents the model from recognizing unclear tools and objects
    results = model(frame, verbose=False, conf=0.40)
    boxes = results[0].boxes
    
    persons = []
    ppes = [] 
    
    for box in boxes:
        cls_id = int(box.cls[0])
        coords = box.xyxy[0].cpu().numpy()
        
        if cls_id == 1:
            persons.append(coords)
        elif cls_id in [0, 2]:
            ppes.append((cls_id, coords))

    # Draw the restricted zone
    overlay = frame.copy()
    cv2.fillPoly(overlay, [danger_zone], (0, 0, 255))
    cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
    cv2.polylines(frame, [danger_zone], isClosed=True, color=(0, 0, 255), thickness=2)

    zone_breach_active = False

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
                if ppe_cls == 2: has_vest = True  # <--- Here was the error, we changed 7 to 2

        if inside_zone:
            zone_breach_active = True
            if (frame_count % 10) < 5:
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)
            label = "DANGER: ZONE BREACH!"
        elif has_helmet and has_vest:
            color = (0, 255, 0)
            label = "SAFE"
        else:
            color = (0, 165, 255)
            label = "WARNING: Missing PPE"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.circle(frame, (foot_x, foot_y), 5, color, -1)

    if zone_breach_active:
        cv2.putText(frame, "!!! ZONE BREACH DETECTED !!!", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("ZoneGuard AI - Industrial Safety", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



danger_zone = np.array([[1066, 486], [1002, 413], [396, 350], [376, 602]], np.int32)