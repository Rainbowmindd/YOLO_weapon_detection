from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

model = YOLO('./models/best.pt')
print("Model classes:", model.names)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    img_bytes = file.read()
    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    results = model(pil_img)

    detections = []
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)
            conf = float(box.conf)
            label = model.names[cls]

            if label == 'weapon' and conf > 0.5:
                detections.append({
                    'label': label,
                    'confidence': round(conf, 4)
                })

    detected = len(detections) > 0
    return jsonify({
        'detected': detected,
        'detections': detections
    })

if __name__ == '__main__':
    app.run(debug=True)


