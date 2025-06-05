from flask import Flask, render_template, Response
import cv2
import os
import random
from ultralytics import YOLO

app = Flask(__name__)

video_path = "C:/Users/Shubh.Shah/Documents/video_summarization/cv_engineer_sample_repo/object-tracking-yolov8-deep-sort-master/output.mkv"
model = YOLO("yolov8n.pt")  # Your model path

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]
detection_threshold = 0.5

def generate_frames():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    while ret:
        results = model(frame)

        for result in results:
            object_counter = 0
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                if score > detection_threshold:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    color = colors[object_counter % len(colors)]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    object_counter += 1

        # Encode frame to JPEG

        #cv2.imshow("frame", frame)

        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        ret, frame = cap.read()

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
