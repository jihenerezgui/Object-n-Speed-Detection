import cv2 as cv
from numpy import mean

def getTheCircle(frame):
    global xArray
    global yArray
    global speedMoyenne
    global speedKmTotal

    try:
        output = frame.copy()
    except:
        return False
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # detect circles in the image
    # image: The input image.
    # method: Detection method.
    # dp: the Inverse ratio of accumulator resolution and image resolution.
    # mindst: minimum distance between centers od detected circles.
    # param_1 and param_2: These are method specific parameters.
    # min_Radius: minimum radius of the circle to be detected.
    # max_Radius: maximum radius to be detected.
    if frame.shape[0] == 480:
        detectedCircles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1,
                                          frame.shape[0], param1=200, param2=10, minRadius=30, maxRadius=100)
    else:
        detectedCircles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1,
                                          frame.shape[0], param1=200, param2=10, minRadius=30, maxRadius=60)

    try:
        for(x, y, r) in detectedCircles[0, :]:

            cv.circle(output, (int(x), int(y)), int(r), (200, 129, 154), 3)
            cv.circle(output, (int(x), int(y)), 2, (0, 255, 255), 3)

            if not xArray:
                xArray.append(x)
                yArray.append(y)
                print('miam')
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
    return True

