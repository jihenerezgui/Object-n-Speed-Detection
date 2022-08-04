import cv2
import dlib
from imutils import face_utils



def detect(img, search):
  #--------Model Path---------#
  proto_file = 'SSD_MobileNet_prototxt.txt'
  model_file = 'SSD_MobileNet.caffemodel'

  #------Variables for the Model ---------#
  classNames = {0: 'background',
                1: 'aeroplane', 2: 'bicycle',
                3: 'bird', 4: 'boat',
                5: 'bottle', 6: 'bus', 7: 'car',
                8: 'cat', 9: 'chair',
                10: 'cow', 11: 'diningtable',
                12: 'dog', 13: 'horse',
                14: 'motorbike', 15: 'person',
                16: 'pottedplant',
                17: 'sheep', 18: 'sofa',
                19: 'train', 20: 'tvmonitor'}

  input_shape = (300, 300)
  mean = (127.5, 127.5, 127.5)
  scale = 0.007843

  #---------Load The Model--------#
  net = cv2.dnn.readNetFromCaffe(proto_file, model_file)

  #------image preprocessing----#
  blob = cv2.dnn.blobFromImage(img,
                              scalefactor=scale,
                              size=input_shape,
                              mean=mean,
                              swapRB=True)
  # since our image is already in the BGR form

  net.setInput(blob)
  results = net.forward()
  center = []
  for i in range(results.shape[2]):
      #center = []
      # confidence
      confidence = round(results[0, 0, i, 2], 2)
      if confidence > 0.7:

          # class id
          id = int(results[0, 0, i, 1])
          if id in search:
          
            # 3-6 contains the coordinate
            x1, y1, x2, y2 = results[0, 0, i, 3:7]
            
            # scale these coordinates to out image pixel
            ih, iw, ic = img.shape
            x1, x2 = int(x1*iw), int(x2*iw)
            y1, y2 = int(y1 * ih), int(y2 * ih)
            center.append(int(x1 + (x2 - x1) / 2))
            center.append(int(y1 + (y2 - y1) / 2))
            #center = (int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2))
            cv2.rectangle(img,
                          (x1, y1),
                          (x2, y2),
                          (0, 200, 0), 2)
            cv2.putText(img, f'{classNames[id]}:{confidence*100}',
                        (x1+30, y1-30),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1, (255, 0, 0), 1)
            # cv2.circle(img, (center[0],
            #                  center[1]), 1, (0, 255, 255), 1)

  img = cv2.resize(img, (640, 720))
  #cv2.imshow('Image', img)
  # cv2.imwrite('output1.jpg',img) # Uncomment this line to save the output
  
  return img, center


if __name__ == "__main__":
    img = cv2.imread('chair.jpg')
    detect(img)
