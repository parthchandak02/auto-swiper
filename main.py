import pyautogui
import time
import re

roseCheckImg = 'Images\\0_CHECK_FOR_ROSE.png'
heartImg = 'Images\\1_HEART.png'
commentImg = 'Images\\2_ADD_COMMENT.png'
likeImg = 'Images\\3_SEND_LIKE.png'


defaultWaitTimeSecs = 15
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
            ImagePath, grayscale=True, confidence=0.7)
        pyautogui.click(x, y)
        print("clicked on image from " + str(ImagePath))
    except:
        print("SKIPPED! cound't find image from " + str(ImagePath))
        return


def scroll(Pixels):
    pyautogui.scroll(Pixels)
    print("scrolled down " + str(Pixels) + " pixels")


def typeMessage(MessageString):
    pyautogui.write(MessageString, interval=0.01)


def sequence():
    defaultLoc()
    clickFromLocation(heartImg)
    wait(1)
    clickFromLocation(commentImg)
    wait(1.5)
    typeMessage("What ends up on tiny beaches?")
    wait(1)
    clickFromLocation(likeImg)
    wait(1)


counter = 0
while counter < 500:
    counter += 1
    print("Like #" + str(counter))
    sequence()
    print("--------------------------------------------------")
