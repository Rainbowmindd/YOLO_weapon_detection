import cv2
from ultralytics import YOLO

# Załaduj swój wytrenowany model YOLOv8
model = YOLO('best.pt')

# Otwórz kamerę (0 = domyślna)
cap = cv2.VideoCapture(0)

# Upewnij się, że kamera się otworzyła
if not cap.isOpened():
    print("Nie udało się otworzyć kamery")
    exit()

print("Kamera uruchomiona. Naciśnij 'q', aby zakończyć.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    for box in results.boxes:
        cls = int(box.cls)
        conf = float(box.conf)
        label = model.names[cls]

        if label == 'weapon' and conf > 0.5:
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

           
            text = f'{label} ({conf * 100:.1f}%)'
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    
    cv2.imshow('Weapon Detection - Press Q to quit', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
