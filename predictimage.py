from ultralytics import YOLO
import glob 

# Load a pretrained YOLOV8 model
model= YOLO("emailmodel.pt")
#folder_path='./videos/'
#list_images=glob.glob(folder_path+'*.png')

model.predict(source="./images/1.png", show=True, save=True, conf=0.5, save_txt=True)

"""for source in list_images:
    model.predict(source=source, show=True, save=True, conf=0.5, save_txt=True)"""