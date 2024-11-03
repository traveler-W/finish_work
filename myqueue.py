import numpy
import cv2
import queue
import threading
from PyQt5.QtGui import QPixmap, QImage
import predict
con_push = threading.Condition()
queues = queue.Queue(100)
QueueSetPix = queue.Queue(1000)


#hellow

def mat_to_qpixmap(cv_image):
    # 确保图像是8位深度
    if cv_image.dtype != numpy.uint8:
        raise TypeError("cv::Mat dtype should be uint8")

    # 根据通道数确定QImage的格式
    if cv_image.ndim == 2:  # 灰度图像
        q_image = QImage(cv_image.data, cv_image.shape[1], cv_image.shape[0], cv_image.strides[0],
                         QImage.Format_Grayscale8)
    elif cv_image.ndim == 3:
        if cv_image.shape[2] == 3:  # BGR图像
            q_image = QImage(cv_image.data, cv_image.shape[1], cv_image.shape[0], cv_image.strides[0],
                             QImage.Format_RGB888)
            q_image = q_image.rgbSwapped()  # 交换红蓝通道
        elif cv_image.shape[2] == 4:  # BGRA图像
            q_image = QImage(cv_image.data, cv_image.shape[1], cv_image.shape[0], cv_image.strides[0],
                             QImage.Format_ARGB32)
            q_image = q_image.rgbSwapped()  # 交换红蓝通道
        else:
            raise ValueError("Unsupported image format")
    else:
        raise ValueError("Unsupported image format")

    # 将QImage转换为QPixmap
    qpixmap = QPixmap.fromImage(q_image)
    return qpixmap
# 生产者
class Producer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.predict = predict.predict()
        self.url = None
        self.num = None

    def set_url(self,url):
            self.url = url

    def setNum(self,num):
        self.predict.set_classes(num)

    def run(self):
        cap = cv2.VideoCapture(self.url)
        # 检查视频是否正确打开
        if not cap.isOpened():
            print("无法打开视频文件！")
            return
        while cap.isOpened():
            ret,frame = cap.read()
            con_push.acquire()
            while queues.full():
                # 等待通知
                con_push.wait()
            frame_temp = self.predict.detech(frame)
            queues.put(mat_to_qpixmap(frame_temp))
            con_push.notify()
            # 释放锁
            con_push.release()


# 消费者
class Consumers(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while 1:
            con_push.acquire()
            while queues.empty():
                con_push.wait()
            frame = queues.get()
            QueueSetPix.put(frame)
            con_push.notify()  # 唤醒其它线程
            con_push.release()