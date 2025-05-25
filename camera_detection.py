import cv2
from ultralytics import YOLO
import os
from datetime import datetime
import shutil

# Folder na detekcje
output_dir = 'detected_weapons'

# Usuń stary folder i utwórz pusty na nowo
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Załaduj model
model = YOLO('best.pt')

# Włącz kamerę
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Nie udało się otworzyć kamery")
    exit()

print("Kamera uruchomiona. Naciśnij 'q', aby zakończyć.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    weapon_detected = False

    for box in results.boxes:
        cls = int(box.cls)
        conf = float(box.conf)
        label = model.names[cls]

        if label == 'weapon' and conf > 0.5:
            weapon_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            text = f'{label} ({conf * 100:.1f}%)'
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if weapon_detected:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{output_dir}/weapon_{timestamp}.jpg'
        cv2.imwrite(filename, frame)
        print(f'[ALERT] Wykryto broń! Zapisano: {filename}')

        # ALERT w prawym dolnym rogu
        alert_text = "ALERT: Weapon detected!"
        (tw, th), _ = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        x_alert = frame.shape[1] - tw - 20
        y_alert = frame.shape[0] - 20

        # Tło + tekst
        cv2.rectangle(frame, (x_alert - 10, y_alert - th - 10), 
                             (x_alert + tw + 10, y_alert + 10), (0, 0, 255), -1)
        cv2.putText(frame, alert_text, (x_alert, y_alert),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow('Weapon Detection - Press Q to quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
