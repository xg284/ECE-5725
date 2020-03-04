#photodisplayer.py Xinyun Guo xg284 Zhuoheng Li zl764 lab2 10-09-2019
import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import*
import os
import sys
import glob
from PIL import Image

pygame.init()
pygame.mouse.set_visible(True)

size = width, height = 800, 420
black = 0, 0, 0
white = 255, 255, 255
bottom_line=350

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('arial',18)
start = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/start.png")
pause = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/stop.jpg")
restart = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/restart.png")
pre = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/previous.png")
next = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/next.png")
speedup = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/2X.png")
speeddown = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/0.5X.png")
scolldown = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/scolldown.png")
quit = pygame.image.load("/home/pi/final_project/insta_project/logo_pics/quit.png")

quit = pygame.transform.scale(quit, (30, 30))
start = pygame.transform.scale(start, (30, 30))
pause = pygame.transform.scale(pause, (30, 30))
restart = pygame.transform.scale(restart, (30, 30))
pre = pygame.transform.scale(pre, (30, 30))
next = pygame.transform.scale(next, (30, 30))
speedup = pygame.transform.scale(speedup, (30, 30))
speeddown = pygame.transform.scale(speeddown, (30, 30))
scolldown = pygame.transform.scale(scolldown, (100, 40))
scolldownrect = scolldown.get_rect()
scolldownrect.x = 0
scolldownrect.y = 380
startrect = start.get_rect()
startrect.x = 50
startrect.y = bottom_line
quitrect = quit.get_rect()
quitrect.x = 700 
quitrect.y = bottom_line
pauserect = pause.get_rect()
pauserect.x = 100
pauserect.y = bottom_line
restartrect = restart.get_rect()
restartrect.x = 100
restartrect.y = bottom_line
prerect = pre.get_rect()
prerect.x = 220
prerect.y = bottom_line
nextrect = next.get_rect()
nextrect.x = 350
nextrect.y = bottom_line
speeddownrect = speeddown.get_rect()
speeddownrect.x = 500
speeddownrect.y = bottom_line
speeduprect = speedup.get_rect()
speeduprect.x = 600
speeduprect.y = bottom_line

def getImages(): 
    valid_formats = [".png", ".PNG", ".jpeg", ".jpg"]
    path = "/home/pi/final_project/insta_project/media/images/"
    image_list = []
    images_added = set()
    for format in valid_formats:
        for imageName in glob.glob(path + "*" + format):
            if imageName not in images_added:
                images_added.add(imageName)
                image = pygame.image.load(imageName)
                image_list.append(image)
    return image_list

# Get all the images under the directory
picture_list = getImages()
picture_rect_list = []
picture_thumbnail = []
picture_rect_thumbnail=[] 
picture_size = [700, 420]

# Creating an array for all the rects of image
for index in range(len(picture_list)) :
    scaled_picture = pygame.transform.scale(picture_list[index], (800, 420))
    picture_list[index] = scaled_picture
    picture_rect_list.append(scaled_picture.get_rect())
    picture_rect_list[index].x=100
    picture_rect_list[index].y=0
for index in range(len(picture_list)) :
    scaled_picture_new = pygame.transform.scale(picture_list[index], (100, 95))
    picture_thumbnail.append(scaled_picture_new)
    picture_rect_thumbnail.append(scaled_picture_new.get_rect())

picture_rect_thumbnail[0].x=0
picture_rect_thumbnail[0].y=0  
picture_rect_thumbnail[1].x=0
picture_rect_thumbnail[1].y=95     
picture_rect_thumbnail[2].x=0
picture_rect_thumbnail[2].y=190    
picture_rect_thumbnail[3].x=0
picture_rect_thumbnail[3].y=285   

start_time = time.time()
codeRunning = True
aniRunning = True
isPause = False
current_picture_index=0
thumbnail_index=0
thumbnail_list=[0,1,2,3]
arry_size=len(picture_list)

temp_time=0
interval=5    
maxspeed=1
minspeed=15

while time.time()-start_time <300 and codeRunning:
    screen.fill(black)
    screen.blit(start,startrect)
    screen.blit(quit,quitrect)
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONDOWN):
            mouse = pygame.mouse.get_pos()
            if(quitrect.x-15 < mouse[0] < quitrect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30):
                codeRunning = False
            elif (startrect.x-15 < mouse[0] < startrect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30):
                temp_time=time.time()
                while aniRunning:
                    if(time.time()-temp_time >= interval and not isPause ):
                        temp_time=time.time()
                        if(current_picture_index!=arry_size-1):
                            current_picture_index += 1
                        else:
                            current_picture_index=0 
                    screen.fill(black)
                    screen.blit(picture_list[current_picture_index],picture_rect_list[current_picture_index])
                    for index in range(4):
                        screen.blit(picture_thumbnail[thumbnail_list[index]],picture_rect_thumbnail[index])
                    screen.blit(scolldown,scolldownrect)
                    for event in pygame.event.get():
                        if (event.type is MOUSEBUTTONDOWN):
                            mouse = pygame.mouse.get_pos()
                            if quitrect.x-15 < mouse[0] < quitrect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30: 
                                aniRunning = False
                                codeRunning = False
                            if pauserect.x-15 < mouse[0] < pauserect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30:
                                if isPause:
                                    isPause = False
                                    #temp_time=time.time()
                                else:
                                    isPause = True
                                    temp_time=time.time()
                            if prerect.x-15 < mouse[0] < prerect.x+45 and bottom_line-30 < mouse[1] < bottom_line+30:
                                if(current_picture_index != 0):
                                  current_picture_index = current_picture_index - 1
                                else:
                                  current_picture_index = arry_size-1
                            if nextrect.x-15 < mouse[0] < nextrect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30: 
                                if(current_picture_index != arry_size-1):
                                  current_picture_index = current_picture_index + 1
                                else:
                                  current_picture_index = 0
                            if speeduprect.x-15 < mouse[0] < speeduprect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30: 
                                interval=interval/2
                                if interval < maxspeed:
                                    interval=maxspeed
                            if speeddownrect.x-15 < mouse[0] < speeddownrect.x+40 and bottom_line-30 < mouse[1] < bottom_line+30: 
                                interval=interval*2
                                if interval > minspeed:
                                    interval=minspeed
                            #thumbnail function    
                            if 0 < mouse[0] < 95:
                                if 0 < mouse[1] < 100: 
                                    current_picture_index=thumbnail_list[0]
                                if 95 < mouse[1] < 190: 
                                    current_picture_index=thumbnail_list[1]
                                if 190 < mouse[1] < 285: 
                                    current_picture_index=thumbnail_list[2]
                                if 285 < mouse[1] < 380: 
                                    current_picture_index=thumbnail_list[3]
                                if 380 < mouse[1] < 420: 
                                    if thumbnail_index+1 < len(picture_thumbnail):
                                        thumbnail_index=thumbnail_index+1
                                        for index in range (3): 
                                            thumbnail_list[index]=thumbnail_list[index+1]
                                        if thumbnail_index+3 < len(picture_thumbnail):
                                            thumbnail_list[3]=thumbnail_index+3
                                        else:
                                            thumbnail_list[3]=thumbnail_index+3-len(picture_thumbnail)
                                    else:
                                        thumbnail_index=0 
                                        thumbnail_list=[0,1,2,3]
                            
                    if isPause:
                        screen.blit(restart, restartrect)
                    else :
                        screen.blit(pause, pauserect)
                    
                    speed = font.render(str(float(5/interval)),True,white,black)
                    speedrect = speed.get_rect()
                    speedrect.x = 700
                    speedrect.y = bottom_line+30
                    screen.blit(speed,speedrect)
                    screen.blit(pre,prerect)
                    screen.blit(next,nextrect)
                    screen.blit(speedup,speeduprect)
                    screen.blit(speeddown,speeddownrect)
                    screen.blit(quit,quitrect)
                    pygame.display.flip()

        elif(event.type is MOUSEBUTTONUP):
            mouse = pygame.mouse.get_pos()
          
    pygame.display.flip()         
