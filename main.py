import pyautogui
import time
from datetime import datetime
import random

# Image paths
roseCheckImg = 'Images/0_CHECK_FOR_ROSE.png'
heartImg = 'Images/1_HEART.png'
commentImg = 'Images/2_ADD_COMMENT.png'
likeImg = 'Images/3_SEND_LIKE.png'

# Counters
counter = 0
imgCounter = 0
skipCounter = 0

# Start time
s = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")

def getStartTime():
    return ("Start Date & Time = " + str(s))

def getEndTime():
    e = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")
    return ("End Date & Time = " + str(e))

dividerBig = "=" * 100
divider = "-" * 50

defaultWaitTimeSecs = 3
pyautogui.FAILSAFE = True

def defaultLoc():
    pyautogui.moveTo(100, 150)

def wait(x):
    for i in range(1, x + 1):
        print(f"waiting... {i} seconds")
        time.sleep(1)

def clickFromLocation(ImagePath):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath, grayscale=True, confidence=0.5)
        pyautogui.click(x, y)
        print(f"clicked on image from {ImagePath}")
        global imgCounter
        imgCounter += 1
    except:
        print(f"SKIPPED! couldn't find image from {ImagePath}")
        global skipCounter
        skipCounter += 1

def scroll(Pixels):
    pyautogui.scroll(Pixels)
    print(f"scrolled down {Pixels} pixels")

def typeMessage(MessageString):
    pyautogui.typewrite(MessageString, interval=0.01)

def loadJokes(filename):
    try:
        with open(filename, 'r') as file:
            jokes = file.read().splitlines()
        return jokes
    except Exception as e:
        print(f"Error reading jokes file: {e}")
        return []

def randomPunGenerator(jokes):
    return random.choice(jokes) if jokes else "No jokes available"

def sequence(jokes):
    defaultLoc()
    clickFromLocation(heartImg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(commentImg)
    wait(defaultWaitTimeSecs)
    msg = randomPunGenerator(jokes)
    print(f"Joke: \n{msg}\n")
    typeMessage(msg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(likeImg)
    wait(defaultWaitTimeSecs)

def logAll():
    try:
        with open("log.txt", "a") as logFile:
            printSkip = f"Skipped Images = {skipCounter} Images"
            printComplete = f"Completed Images = {imgCounter} Images"
            printTotal = f"Total Images = {imgCounter + skipCounter} Images"
            log = (
                f"\n\n{dividerBig}\n{getStartTime()}\n{divider}\n{printSkip}\n{printComplete}\n"
                f"{printTotal}\n{divider}\n{getEndTime()}\n{dividerBig}\n\n"
            )
            logFile.write(log)
            print(log)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def looper():
    global counter
    jokes = loadJokes('jokes.txt')
    while counter < 200:
        try:
            counter += 1
            print(f"Like #{counter}")
            sequence(jokes)
            print(divider)
        except KeyboardInterrupt:
            break
        finally:
            logAll()

looper()
