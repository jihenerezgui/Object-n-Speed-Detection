#!/usr/bin/env python3.10

from array import array
import numpy as np
import cv2 as cv
from numpy import mean
from detection import detect
import time

capture = cv.VideoCapture('/dev/video2')

frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
# out = cv.VideoWriter('outpyCircle.avi', cv.VideoWriter_fourcc(
#     'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
xArray = []
yArray = []
speedMoyenne = []
speedKmTotal = []


class FPSHandler:
    def __init__(self, cap=None):
        self.timestamp = time.time()
        self.start = time.time()
        self.frame_cnt = 0

    def next_iter(self):
        self.timestamp = time.time()
        self.frame_cnt += 1

    def fps(self):
        return self.frame_cnt / (self.timestamp - self.start)

def getSpeed(position):
    global xArray
    global yArray
    global speedMoyenne
    global speedKmTotal
    
    if len(position) == 0: 
        return None 

    speedKm = 0
    x, y = position[0], position[1]
    try:
        
        if not xArray:
            xArray.append(x)
            yArray.append(y)
        else:
            speedX = xArray[-1] - x
            speedY = yArray[-1] - y
            xArray.append(x)
            yArray.append(y)
            speedY = abs(speedY)
            speedX = abs(speedX)
            speed = speedX + speedY
            speedMoyenne.append(speed)
            speedKm = speed * x / y
            speedKmTotal.append(speedKm)

            print("x :", x, "  -    y :", y, "  -    speed: ", speed, "  -  speedAverage:", mean(speedMoyenne),
                    "  -  Speed Pixel/second: ", speedKm, "  -  Average pixels/second: ",  mean(speedKmTotal))

    except:
        print('not working')
        pass
    #cv.imshow('output', output)
    #return speedKm
    return mean(speedKmTotal[-3:])


def main():
    fps = FPSHandler()
    while True:
        fps.next_iter()
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        _, frame = capture.read()
         #------Variables for the Model ---------#
        # 0: 'background',
        # 1: 'aeroplane', 
        # 2: 'bicycle',
        # 3: 'bird', 
        # 4: 'boat',
        # 5: 'bottle', 
        # 6: 'bus', 
        # 7: 'car',
        # 8: 'cat', 
        # 9: 'chair',
        # 10: 'cow', 
        # 11: 'diningtable',
        # 12: 'dog',
        # 13: 'horse',
        # 14: 'motorbike',
        # 15: 'person',
        # 16: 'pottedplant',
        # 17: 'sheep',
        # 18: 'sofa',
        # 19: 'train',
        # 20: 'tvmonitor'
        # Ajouter la liste d'objet désiré comme deuxième argument(vous référé au commentaire précédent)
        #img, center = detect(frame, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        img, center = detect(frame, [7]) #Pour detecter les voitures
        speed = getSpeed(center)

        cv.putText(img, "Fps: {:.2f}".format(
            fps.fps()), (6, 15), cv.FONT_HERSHEY_TRIPLEX, 0.4, color=(255, 255, 255))
        if speed is not None:
            cv.putText(img, "Speed Pixel/second:: {:.2f}".format(speed), (6, 40), cv.FONT_HERSHEY_TRIPLEX, 0.4, color=(102, 0, 102))
        #print(img.shape)
        
        cv.imshow('Image', img)
        # if img:
        #     break
        #time.sleep(0.1)
    capture.release()
    #out.release()
    cv.destroyAllWindows()
    return


if __name__ == "__main__":
    main()
