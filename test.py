from ultralytics import YOLO
import cv2
model = YOLO("models/yolo11s.pt")


im = cv2.imread("cars/1.jpg")
source = "cars"


results = model(im)

for index,result in  enumerate(results):
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    nn = result.plot()
    nn.show()