from glob import glob
import pyautogui
import time
from datetime import datetime
import re
import random

# For a later time - ML / OPENCV mods
# from cv2 import divide


roseCheckImg = 'Images\\0_CHECK_FOR_ROSE.png'
heartImg = 'Images\\1_HEART.png'
commentImg = 'Images\\2_ADD_COMMENT.png'
likeImg = 'Images\\3_SEND_LIKE.png'

counter = 0
imgCounter = 0
skipCounter = 0

s = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")


def getStartTime():
    return ("Start Date & Time = " + str(s))


def getEndTime():
    e = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")
    return ("End Date & Time = " + str(e))


dividerBig = "===================================================================================================="
divider = "--------------------------------------------------"

defaultWaitTimeSecs = 3
pyautogui.FAILSAFE = True


def defaultLoc():
    pyautogui.moveTo(100, 150)


def wait(x):
    i = 1
    while i <= x:
        print("waiting... " + str(i) + " seconds")
        time.sleep(1)
        i += 1

# def waitToLoad():
#     defaultLoc()
#     try:
#         coinbase_x,coinbase_y=pyautogui.locateCenterOnScreen(loadingImg,grayscale=True,confidence=0.7)
#         if coinbase_x > 0:
#             try:
#                 page3_x,page3_y=pyautogui.locateCenterOnScreen(page3,grayscale=True,confidence=0.7)
#                 if page3_x > 0:
#                     print("We are on page 3!")
#                     return
#             except:
#                 print("Loading...")
#                 wait(3)
#                 waitToLoad()
#     except:
#         return False


def clickFromLocation(ImagePath):
    try:
        x, y = pyautogui.locateCenterOnScreen(
            ImagePath, grayscale=True, confidence=0.5)
        pyautogui.click(x, y)
        print("clicked on image from " + str(ImagePath))
        global imgCounter
        imgCounter += 1
    except:
        print("SKIPPED! cound't find image from " + str(ImagePath))
        global skipCounter
        skipCounter += 1
        return


def scroll(Pixels):
    pyautogui.scroll(Pixels)
    print("scrolled down " + str(Pixels) + " pixels")


def typeMessage(MessageString):
    pyautogui.typewrite(MessageString, interval=0.01)


punArray = ["Add joke here",
            "Add pun here"]


def randomPunGenerator(punArray):
    randNum = random.randint(0, len(punArray)-1)
    return punArray[randNum]


def sequence():
    defaultLoc()
    clickFromLocation(heartImg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(commentImg)
    wait(defaultWaitTimeSecs)
    msg = str(randomPunGenerator(punArray))
    print("Joke: \n" + msg + "\n")
    typeMessage(msg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(likeImg)
    wait(defaultWaitTimeSecs)


def logAll():
    logFile = open("log.txt", "r+")
    content = logFile.read()
    printSkip = ("Skipped Images = " + str(skipCounter) + " Images")
    printComplete = ("Completed Images = " + str(imgCounter) + " Images")
    printTotal = ("Total Images = " +
                  str(imgCounter + skipCounter) + " Images")
    log = ("\n\n" + dividerBig + "\n" + getStartTime() + "\n" + divider + "\n" + printSkip + "\n" + printComplete +
           "\n" + printTotal + "\n" + divider + "\n" + getEndTime() + "\n" + dividerBig + "\n\n")
    logFile.seek(0)
    logFile.write(log + content)
    print(log)
    logFile.close()


def looper():
    global counter
    while counter < 200:
        try:
            counter += 1
            print("Like #" + str(counter))
            sequence()
            print(divider)

        except KeyboardInterrupt:
            return

        finally:
            logAll()


looper()
