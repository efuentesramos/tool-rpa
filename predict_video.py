from ultralytics import YOLO

# Load a pretrained YOLOV8 model
model= YOLO("bestv4.pt")

# Run interface on the source
model.predict(source="./videos/gmail2.mkv", show=True, save=True, conf=0.5, save_txt=True, imgsz=640)
model.val()