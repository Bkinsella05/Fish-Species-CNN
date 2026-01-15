from ultralytics import YOLO

#This is the YOLO v8 Model that will annoate all of the data

model = YOLO("yolov8s.pt") #Can use nano if overfitting occurs "yolov8n.pt"

model.train(
    data="data.yaml",
    epochs=150,
    imgsz=640,
    batch=16,
    pretrained=True,
    patience=20,
    augment=True
)