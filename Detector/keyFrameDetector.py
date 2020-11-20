import os
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from moviepy import editor
import random

'''
videoToSub: String that represents the name of the video to be subbed, must be in the same directory
fps: frames per second of the video
manualInputFlag: True if you would like to make a custom template to better crop your images. If this option is
set to true try to make the bounding box as small as possible to ensure good cropping
frameDivision: Decides how many frames are recorded, total frames in video/frameDivison
parentDirectory: string representing the the drive to current directory. give a value if you want to see the produced 
frames
'''
def translateASLVideo(videoToSub, fps, manualInputFlag = False, frameDivision = 10, parentDirectory='default'):
    videoToFrame = cv2.VideoCapture(videoToSub)
    frameTimes = []
    ret, frame = videoToFrame.read()
    path = ''
    path2 = ''
    if parentDirectory != 'default':
        directory = "frames"
        '''parentDirectory = "C:/users/blazi/downloads/template-asl"'''
        path = os.path.join(parentDirectory, directory)
        os.mkdir(path)
        os.chdir(path)
    flag = True
    frameSelect = 0
    count = 0
    while flag:
        if frameSelect % frameDivision == 0:
            cv2.imwrite("frame%d.jpg" % count, frame)
            frameTimes.append((frame, count))
        count += 1
        frameSelect += 1
        flag, frame = videoToFrame.read()

    croppedImages = []
    if parentDirectory != 'default':
        os.chdir(parentDirectory)
        directory2 = "framesCropped"
        path2 = os.path.join(parentDirectory, directory2)
        os.mkdir(path2)
    templates = []
    if manualInputFlag:
        img1, time1 = frameTimes[0]
        plt.imshow(img1)
        coordinates = plt.ginput(4, 30)
        maxx = 0
        maxy = 0
        minx = np.Inf
        miny = np.Inf
        for x, y in coordinates:
            if int(x) < minx:
                minx = int(x)
            if int(x) > maxx:
                maxx = int(x)
            if int(y) < miny:
                miny = int(y)
            if int(y) > maxy:
                maxy = int(y)
        grayImage = cv2.cvtColor(img1.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        templates.append(grayImage[miny:maxy, minx:maxx])
    else:
        templates.append(cv2.imread('asl5.jpg', 0))
    for img, time in frameTimes:
        if manualInputFlag:
            print(templates[0].shape)
            w, h = templates[0].shape
        else:
            w, h = templates[0].shape[::-1]
        grayImage = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        temp = cv2.matchTemplate(grayImage, templates[0], 4)
        minCal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(temp)
        corner1 = maxLoc
        if parentDirectory != 'default':
            os.chdir(path)
            string = "frame%d.jpg" % time
            im = Image.open(string)
            image2 = im.crop((corner1[0], corner1[1], corner1[0] + w, corner1[1] + h))
            cv2.rectangle(img, corner1, (corner1[0]+w, corner1[1]+h), 2)
            os.chdir(path2)
            cv2.imwrite("croppedFrame%d.jpg" % time, np.float32(image2))
        else:
            croppedimage = img[corner1[1]:corner1[1]+h, corner1[0]:corner1[0]+w]
            croppedImages.append(croppedimage)

    videoname = videoToSub
    if parentDirectory != 'default':
        video = editor.VideoFileClip(os.path.join(parentDirectory, videoname))
    else:
        video = editor.VideoFileClip(videoToSub)
    letters = []
    letters.append('A')
    letters.append('B')
    letters.append('C')
    letters.append('D')
    letters.append('E')
    letters.append('F')
    letters.append('G')
    letters.append('H')
    letters.append('I')
    letters.append('J')
    letters.append('K')
    letters.append('L')
    letters.append('M')
    letters.append('N')
    letters.append('O')
    letters.append('P')
    letters.append('Q')
    letters.append('R')
    letters.append('S')
    letters.append('T')
    letters.append('U')
    letters.append('V')
    letters.append('W')
    letters.append('X')
    letters.append('Y')
    letters.append('Z')
    subs = []
    num = 0



    '''determines sub for given frame(to be replaced with function from mod)'''
    for i in range(frameTimes[len(frameTimes)-1][1]):
        if i % 600 == 0:
            num = random.randint(0, 25)
        if i == frameDivision:
            subs.append(((0, i), letters[num]))
        if i % frameDivision == 0 and i != 0 and i != frameDivision:
            subs.append(((i - frameDivision, i), letters[num]))



    '''creates new clips based on chosen subs above'''
    print(len(subs))
    print(frameTimes[len(frameTimes)-1][1])
    cutClips = []
    newSubs = []
    lastSub = 'Wierd'
    startT = 0
    for (t1, t2), subtitle in subs:
        if t1 == 0:
            lastSub = subtitle
        else:
            if lastSub != subtitle:
                newSubs.append(((startT/fps, t1/fps), lastSub))
                lastSub = subtitle
                startT = t1
    print(len(newSubs))
    for (t1, t2), subtitle in newSubs:
        print('ok:)')
        subClip = video.subclip(t1, t2)
        addClip = editor.TextClip(subtitle, fontsize=40, font='Xolonium-Bold', color='Black')
        textPlacer = editor.CompositeVideoClip([subClip, addClip.set_position(('center', 'bottom'))])
        cutClips.append(textPlacer.set_duration(subClip.duration))
    newVideo = editor.concatenate_videoclips(cutClips)
    if parentDirectory != 'default':
        newVideo.write_videofile(os.path.join(parentDirectory, 'newASLVid.mp4'))
        return newVideo
    else:
        return newVideo


parentDirectory = "C:/users/blazi/downloads/template-asl"
fps = 29.97
framedivision = 10
videoSub = "ASLvideo.mp4"
vid = translateASLVideo(videoSub, manualInputFlag=True, frameDivision=framedivision, fps=fps, parentDirectory=parentDirectory)