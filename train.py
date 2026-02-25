from ultralytics import YOLO 

def main () :
    model = YOLO ('yolov8n-obb.pt')
    model.train(data='data.yaml', epochs=50, imgsz=640, batch=4, name='yolov8_obb_model', patience=5)

if __name__== '__main__' :
    main()
