import pyautogui
import time
import re
import random

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
    pyautogui.typewrite(MessageString, interval=0.01)


punArray = ["Why do fathers take an extra pair of socks when they go golfing?. In case they get a hole in one!",
            "My friend asked me to pick up 6 cans of sprite from the grocery store today. When I got home, I realized I had picked 7up.",
            "You're American when you enter and exit the bathroom. But what are you when you are in the bathroom? Eur-a-peein.",
            "What do cats look for in a significant other? A great purrsonality.",
            "What did Darth Vader’s dog say to Luke’s dog?",
            "What do you call a sweater that was blown away by the wind? A cardi-gone.",
            "What is a penguin's favorite aunt?",
            "What did the sushi say to the bee?",
            "What ends up on tiny beaches?",
            "What did baby corn say to momma corn?",
            "What's the best thing about living in Switzerland?",
            "Why can’t you can’t trust atoms? They make up everything.",
            "What do sea monsters eat for lunch? Fish and ships.",
            "What do mermaids wash their fins with? Tide.",
            "Did you hear Steve Harvey and his wife got into a fight? It was a Family Feud.",
            "Velcro is a complete ripoff.",
            "Why didn't the melons get married? Because they can't-elope.",
            "I've started telling people about the benefits of dried grapes. It's all about raisin awareness."]


def randomPunGenerator(punArray):
    randNum = random.randint(0, len(punArray)-1)
    return punArray[randNum]


def sequence():
    defaultLoc()
    clickFromLocation(heartImg)
    wait(1)
    clickFromLocation(commentImg)
    wait(1.5)
    print("Joke: \n" + randomPunGenerator(punArray) + "\n")
    msg = str(str(randomPunGenerator(punArray)))
    typeMessage(msg)
    wait(1)
    clickFromLocation(likeImg)
    wait(1)


counter = 0
while counter < 500:
    counter += 1
    print("Like #" + str(counter))
    sequence()
    print("--------------------------------------------------")
