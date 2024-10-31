
from ultralytics import YOLO


temp = ["person",
  "bicycle",
  "car",
  "motorcycle",
  "airplane",
  "bus",
  "train",
  "truck",
  "boat",
  "traffic_light",
  "fire_hydrant"]

class predict():
    def __init__(self):
        self.model = YOLO("models/yolo11s.pt")
        self.classes = []

    def detech(self,im):
        results = self.model.predict(im,classes=self.classes)
        return results[0].plot()

    def set_classes(self,num:str):
        self.classes.clear()
        if num == temp[0]:
            self.classes.append(0)
        elif num == temp[1]:
            self.classes.append(1)
        elif num == temp[2]:
            self.classes.append(2)
        elif num == temp[3]:
            self.classes.append(3)
        elif num == temp[4]:
            self.classes.append(4)
        elif num == temp[5]:
            self.classes.append(5)
        elif num == temp[6]:
            self.classes.append(6)
        elif num == temp[7]:
            self.classes.append(7)
        elif num == temp[8]:
            self.classes.append(8)
        elif num == temp[9]:
            self.classes.append(9)
        elif num == temp[10]:
            self.classes.append(10)
        else:
            pass
