import pygame

chieuCao = 800
chieuNgang = 1200
sizeBox = 100
soCot = 4
soHang = 4
khoangCach = 10

leX = (chieuNgang - ((sizeBox+khoangCach)* soCot)+khoangCach) / 2
leY = (chieuCao - ((sizeBox+khoangCach)*soHang)+khoangCach) / 2

white = (255, 255, 255)
black = (0, 0, 0)

icon = pygame.image.load("images/images0.png") # set icon bằng icon trong đường dẫn
background = pygame.image.load("bg/background.png")
images_dir = "images"

first_box = None
second_box = None
boxDaThay = []
boxDaLat = []

tg_Dung = None

