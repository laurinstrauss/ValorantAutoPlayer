from PIL import ImageGrab
from win32gui import GetWindowText, GetForegroundWindow
import win32api
import time
import psutil

# overall information:
# - if the program is taking too much of your CPU, change the delay variable to a higher value (delay is in seconds)
# - if the program doesnt detect a game state correctly, consider taking a look at the reference images and coordinates in the functions
#   and adjust the checking coordinates to fit those of the images shown on your computer
# - VALORANT must run on your primary screen with a resolution of 1920x1080 (both screen and VALORANT);
#   should you have other specs, take screenshots, compare the reference images and adjust the coordinates of the getpixel calls
# - the media should be playing before you load into the first buyphase of a game, ideally already in VALORANT home screen
# - to detect and debug a possible error, search "# print(" and replace with "print(", then every state detection method that detects a state is printed

# region state detection methods

# returns True if the current snapshot was taken while the player is ingame
# detect the white lines in the border arround the time and agent icons and arround the abilites and HP
def isIngame():
    result = []
    # white border top middle arround time and agent icons:
    result.append(rgb_im.getpixel((394, 17))) # left white line
    result.append(rgb_im.getpixel((399, 17))) # left white line
    result.append(rgb_im.getpixel((832, 17))) # center left white line
    result.append(rgb_im.getpixel((837, 17))) # center left white line
    result.append(rgb_im.getpixel((944, 110))) # center lower left white line
    result.append(rgb_im.getpixel((977, 110))) # center lower right white line
    result.append(rgb_im.getpixel((1084, 17))) # center right white line
    result.append(rgb_im.getpixel((1089, 17))) # center right white line
    result.append(rgb_im.getpixel((1521, 17))) # right white line
    result.append(rgb_im.getpixel((1526, 17))) # right white line
    # white border bottom middle arround abilities and HP:
    result.append(rgb_im.getpixel((537, 1054))) # left white line
    result.append(rgb_im.getpixel((540, 1054))) # left white line
    result.append(rgb_im.getpixel((640, 1054))) # center left white line
    result.append(rgb_im.getpixel((643, 1054))) # center left white line
    result.append(rgb_im.getpixel((739, 1004))) # center upper left white line
    result.append(rgb_im.getpixel((742, 1004))) # center upper left white line
    result.append(rgb_im.getpixel((1177, 1004))) # center upper right white line
    result.append(rgb_im.getpixel((1180, 1004))) # center upper right white line
    result.append(rgb_im.getpixel((1276, 1054))) # center right white line
    result.append(rgb_im.getpixel((1279, 1054))) # center right white line
    result.append(rgb_im.getpixel((1379, 1054))) # right white line
    result.append(rgb_im.getpixel((1382, 1054))) # right white line

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isIngame == TRUE")
    return True

# returns True if the current snapshot was taken while the announcement for ultimate ready was shown
# detect the white lines on the left and right of the banner with the ultimates name in it
# works for all agents because the banner is a fixed size with the name centered
def isIngameUltReady():
    result = []
    result.append(rgb_im.getpixel((834, 239)))   # left top of line
    result.append(rgb_im.getpixel((834, 255)))   # left center of line
    result.append(rgb_im.getpixel((834, 270)))  # left bottom of line
    result.append(rgb_im.getpixel((1085, 239)))   # right top of line
    result.append(rgb_im.getpixel((1085, 255)))   # right center of line
    result.append(rgb_im.getpixel((1085, 270)))  # right bottom of line

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isIngameUltRead == TRUE")
    return True

# returns True if the current snapshot was taken while the ingame shop was open
# detect the corners of the box with the agent icon and the credits in the top left
def isIngameShopOpen():
    result = []
    result.append(rgb_im.getpixel((30, 118)))   # top left corner of box
    result.append(rgb_im.getpixel((355, 118)))  # top right corner of box
    result.append(rgb_im.getpixel((355, 255)))  # bottom right corner of box
    result.append(rgb_im.getpixel((30, 255)))   # bottom left corner of box

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isIngameShopOpen == TRUE")
    return True

# returns True if the current snapshot was taken while the ingame ESC menu was open 
# detect the dots under the menu pages
def isIngameESCMenuOpen():
    result = []
    result.append(rgb_im.getpixel((659, 51)))   # dot under "MATCH" text
    result.append(rgb_im.getpixel((779, 51)))   # dot under "GENERAL" text
    result.append(rgb_im.getpixel((899, 51)))   # dot under "CONTROLS" text
    result.append(rgb_im.getpixel((1019, 51)))   # dot under "CROSSHAIR" text
    result.append(rgb_im.getpixel((1139, 51)))  # dot under "VIDEO" text
    result.append(rgb_im.getpixel((1259, 51)))  # dot under "AUDIO" text

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isIngameESCMenuOpen == TRUE")
    return True

# returns True if the current snapshot was taken while the ingame chat was open
# detect the white scroll bar
# for simplicity reasons: does not work if the chat is scrolled back
def isIngameChatOpen():
    result = []
    result.append(rgb_im.getpixel((460, 963)))  # top left corner of scrollbar
    result.append(rgb_im.getpixel((466, 963)))  # top right corner of scrollbar
    result.append(rgb_im.getpixel((463, 988)))  # middle of scrollbar

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isIngameChatOpen == TRUE")
    return True

# returns True if the current snapshot was taken while the scoreboard was open
# detect the the white pixels on each side of the player list
def isIngameScoreboardOpen():
    result = []
    result.append(rgb_im.getpixel((572, 338)))  # top left corner of list
    result.append(rgb_im.getpixel((1345, 338))) # top right corner of box
    result.append(rgb_im.getpixel((1345, 739))) # bottom right corner of box
    result.append(rgb_im.getpixel((572, 739)))  # bottom left corner of box

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isScoreboardOpen == TRUE")
    return True

# returns True if the current snapshot was taken while the report player dialogue was open
# detect the the "REPORT PLAYER" text
def isIngameReportPlayerOpen():
    result = []
    result.append(rgb_im.getpixel((795, 258)))  # 1st R
    result.append(rgb_im.getpixel((811, 283)))  # 1st R
    result.append(rgb_im.getpixel((907, 272)))  # 2nd R
    result.append(rgb_im.getpixel((924, 264)))  # 2nd R
    result.append(rgb_im.getpixel((1054, 258)))  # Y
    result.append(rgb_im.getpixel((1063, 284)))  # Y
    result.append(rgb_im.getpixel((1125, 285)))  # 3rd R
    result.append(rgb_im.getpixel((1114, 272)))  # 3rd R

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isReportPlayerOpen == TRUE")
    return True

# returns True if the current snapshot was taken while "THRIFTY"/"ACE"/"CLUTCH"/"TEAM ACE" round end was shown
# detect the corners of the box where the "THRIFTY"/"ACE"/"CLUTCH"/"TEAM ACE" text is inside
# works for all "THRIFTY"/"ACE"/"CLUTCH"/"TEAM ACE" because the box is a fixed size with the text centered
def isIngameAceOrThriftyOrClutchOrTeamAceRoundEnd():
    result = []
    result.append(rgb_im.getpixel((710, 137)))  # top left corner of box
    result.append(rgb_im.getpixel((710, 282)))  # top right corner of box
    result.append(rgb_im.getpixel((1210, 282))) # bottom right corner of box
    result.append(rgb_im.getpixel((1210, 137))) # bottom left corner of box

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isAceOrThriftyOrClutchOrTeamAceRoundEnd == TRUE")
    return True

# returns True if the current snapshot was taken while "WON"/"LOST" round end was shown
# detect the corners of the box where "WON"/"LOST" text is inside
# works for both "WON"/"LOST" because the box is a fixed size with the text centered
def isIngameWonOrLostRoundEnd():
    result = []
    result.append(rgb_im.getpixel((837, 137)))  # top left corner of box
    result.append(rgb_im.getpixel((1081, 137))) # top right corner of box
    result.append(rgb_im.getpixel((1081, 275))) # bottom right corner of box
    result.append(rgb_im.getpixel((837, 275)))  # bottom left corner of box

    # the corners of "WON" and "LOST" are for some reason not 100% white, therefore <= 250
    for x in result:
        if(x[0] <= 250 or x[1] <= 250 or x[2] <= 250):
            return False
    # print("isWonOrLostScreen == TRUE")
    return True

# returns True if the current snapshot was taken while the player picked up the spike
# detect the spike icon in the top middle
def isIngameSpikePickedUp():
    result = []
    result.append(rgb_im.getpixel((948, 193)))  # top left part of spike icon
    result.append(rgb_im.getpixel((979, 204)))  # top right part of spike icon
    result.append(rgb_im.getpixel((960, 236)))  # bottom middle part of spike icon

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isSpikePickedUp == TRUE")
    return True

# returns True if the current snapshot was taken in buyphase
# detect the border of the B in "PRESS B TO BUY" text in the "BUYPHASE" box
# also works for special rounds like "LAST ROUND BEFORE SWAP", "MATCHPOINT" or "OVERTIME"
def isIngameInBuyphase():
    result = []
    result.append(rgb_im.getpixel((946, 253)))   # top left corner of border
    result.append(rgb_im.getpixel((968, 253)))   # top right corner of border
    result.append(rgb_im.getpixel((968, 275)))   # bottom right corner of border
    result.append(rgb_im.getpixel((946, 275)))   # bottom left corner of border

    for x in result:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isBuyphase == TRUE")
    return True

# Image Required
# returns True if the current snapshot was taken when the player was dead
# detect the line next to the agent image in the bottom left
def isIngamePlayerDead():
    resultmouse = []
    resultline = []
    # green/turqouise (left click button) part of mouse icon:
    resultmouse.append(rgb_im.getpixel((138, 853)))
    resultmouse.append(rgb_im.getpixel((135, 859)))
    resultmouse.append(rgb_im.getpixel((139, 865)))
    # line on left of current agent watched:
    resultline.append(rgb_im.getpixel((30, 871)))
    resultline.append(rgb_im.getpixel((30, 797)))

    for x in resultmouse:
        if(x[0] != 170 or x[1] != 237 or x[2] != 225):
            return False
    for x in resultline:
        if(x[0] != 255 or x[1] != 255 or x[2] != 255):
            return False
    # print("isPlayerDead == TRUE")
    return True

# endregion

# region media, screenshot and I/O methods

# sends the play/pause key to the win32api when isMediaPlaying is not set
def play():
    global isMediaPlaying
    if (isMediaPlaying == False):
        win32api.keybd_event(0xB3, win32api.MapVirtualKey(0xB3, 0))
        # print("isMediaPlaying == TRUE")
        isMediaPlaying = True

# sends the play/pause key to the win32api when isMediaPlaying is set
def pause():
    global isMediaPlaying
    if (isMediaPlaying == True):
        win32api.keybd_event(0xB3, win32api.MapVirtualKey(0xB3, 0))
        # print("isMediaPlaying == FALSE")
        isMediaPlaying = False

# grabs a screenshot of the primary screen and converts it to RGB format
def grabScreenshot():
    global rgb_im
    snapshot = ImageGrab.grab()
    rgb_im = snapshot.convert('RGB')

# system output with requirement information
def printInfo():
    print("ValorantAutoPlayer started!")
    print("ValorantAutoPlayer works by periodically screenshotting the game and detecting the games state by scanning these.")
    print("Requirements for ValorantAutoPlayer to work as intended:")
    print("\t- the application (Spotify, AppleMusic, YouTube in Browser, etc.) that is playing your media is opened")
    print("\t- VALORANT Resolution is \"1920 x 1080 16:9\" (Framerate / Refreshrate does not matter)")
    print("\t- VALORANT is running on the systems primary monitor")
    print("\t- VALORANT language is to english")
    print("\t- VALORANT Display Mode is \"Fullscreen\" or \"Windowed Fullscreen\"")
    print("\t- Start ValorantAutoPlayer while not ingame and make sure the media is playing before you queue up for a game")

# endregion

# global variable to keep track if media is playing (there is no simple way to extract that system information)
isMediaPlaying = True

# global variable for delay (in seconds) between snapshots, change if ValorantAutoPlayer is using too much system resources
delay = 0.2

printInfo()
while(True):
    currentProgram = GetWindowText(GetForegroundWindow())
    if(currentProgram == "VALORANT  "):
        # VALORANT is the currently active application in the foreground, so a statecheck is performed
        grabScreenshot()
        if(isIngame()):
            if(isIngameChatOpen() or isIngameScoreboardOpen() or isIngameSpikePickedUp()):
                # do nothing, these cases dont change the gamestate but interfere with buyphase detection
                time.sleep(delay)
            elif(isIngameInBuyphase() 
                 or isIngamePlayerDead() 
                 or isIngameWonOrLostRoundEnd() 
                 or isIngameAceOrThriftyOrClutchOrTeamAceRoundEnd()
                 or isIngameUltReady()):
                # ingame and currently in buyphase, the media should be paused
                play()
                time.sleep(delay)
            else:
                # ingame and in an active round with the player alive, the media should be playing
                pause()
                time.sleep(delay)
        else:
            # not ingame, the media should be playing
            play()
            time.sleep(delay)
    else:
        # VALORANT is not currently active, delay
        if("VALORANT.exe" not in (i.name() for i in psutil.process_iter())):
            print("VALORANT is not running, shutting ValorantAutoPlayerDown.")
            time.sleep(1)
            exit()
        else:
            time.sleep(1)