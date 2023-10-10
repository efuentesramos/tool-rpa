from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8n.yaml')

# Train the model using the 'coco128.yaml' dataset for 100 epochs
results = model.train(data='config_emails.yaml', epochs=100)