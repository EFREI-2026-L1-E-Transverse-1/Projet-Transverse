from pygame import *

white = (255,255,255)
black = (0,0,0)
title = "Blob Battle"
ressourceFolder = "Ressource"

init()
display.set_caption(" "*3 + title)
display.set_icon('Ressource/120px-MKDDBananaModel.png')
# display.set_icon(ressourceFolder + '/' + '120px-MKDDBananaModel.png')
screen = display.set_mode((1920, 1080))
imagetest = image.load('Ressource/c7f297523ce57fc.png')
screen.blit(imagetest, (500, 500))
screen.fill(white)