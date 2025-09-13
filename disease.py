
from ultralytics import YOLO
def main():
    model = YOLO("best.pt")

    # Input image
    img_path = "test.jpg"
    results = model(img_path, conf=0.25,verbose=False)

    # Loop through detections and print class names
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        return (cls_name)
