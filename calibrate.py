import cv2

# Your video path
VIDEO_PATH = "videos/test_video.mp4" 

def draw_polygon(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN: # On left mouse button click
        points.append([x, y])
        print(f"Point recorded: [{x}, {y}]")

points = []
cap = cv2.VideoCapture(VIDEO_PATH)
success, frame = cap.read() # Take only the first frame (image) from the video

if success:
    cv2.namedWindow("Calibration")
    cv2.setMouseCallback("Calibration", draw_polygon)
    
    print("Click with the mouse on 4 corners around the machine to define the restricted zone.")
    print("Press the 'q' key when finished.")
    
    while True:
        temp_frame = frame.copy()
        # Draw points and lines while clicking
        for i, pt in enumerate(points):
            cv2.circle(temp_frame, tuple(pt), 5, (0, 0, 255), -1)
            if i > 0:
                cv2.line(temp_frame, tuple(points[i-1]), tuple(pt), (0, 0, 255), 2)
        if len(points) == 4:
            cv2.line(temp_frame, tuple(points[3]), tuple(points[0]), (0, 0, 255), 2)
            
        cv2.imshow("Calibration", temp_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("\n=== Copy this line and paste it into the main.py file ===")
    print(f"danger_zone = np.array({points}, np.int32)")

cap.release()
cv2.destroyAllWindows()