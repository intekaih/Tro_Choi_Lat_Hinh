import pygame  # thư viện pygame
import os  # thư viện xử lý file và dir
import random  # thư viện random
import time

# Thư viện của tôi 
from define import *

pygame.init()

# Hàm nhập hình ảnh
def input_images():
    images = []  # khởi tạo mảng
    for filename in os.listdir(images_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # check png or jpg
            img = pygame.image.load(os.path.join(images_dir, filename))  # load hình ảnh "images_dir/filename"
            img = pygame.transform.scale(img, (sizeBox, sizeBox))  # thay đổi tỷ lệ ảnh
            images.append(img)
    return images

# Hàm load hình ảnh vào bảng hình ảnh
def load_images(images):
    images_table = []
    for i in range(soHang):  # range: hàm tạo 1 dãy số từ 0 đến soHang
        hang = []
        for j in range(soCot):
            hang.append(images.pop())  # Lấy hình ảnh từ danh sách
        images_table.append(hang)
    return images_table

# Hàm trộn images
def random_images(images):
    random.shuffle(images)

# Khai báo biến
screen = pygame.display.set_caption("Trò Chơi Lật Hình")
screen = pygame.display.set_icon(icon) #define
screen = pygame.display.set_mode((chieuNgang, chieuCao))  # define

images = input_images()
images = images * 2
random_images(images)

images_table = load_images(images) # bảng hình ảnh

# Chạy chương trình 
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra sự kiện nhấn chuột
            x, y = pygame.mouse.get_pos()  # Lấy tọa độ chuột
            print(f'Mouse clicked at: {x}, {y}, {x - leX}')  # In ra tọa độ chuột
            
           

            cot = int(x - leX) // (sizeBox + khoangCach)
            hang = int(y - leY) // (sizeBox + khoangCach)

            if (0 <= hang < soHang and 0 <= cot < soCot):
                if (hang, cot) not in boxDaLat and (hang, cot) not in boxDaThay:
                    if first_box is None:
                        first_box = (hang, cot)
                        boxDaThay.append(first_box)

                    elif second_box is None:
                        second_box = (hang, cot)
                        boxDaThay.append(second_box)

                        if images_table[first_box[0]][first_box[1]] == images_table[second_box[0]][second_box[1]]:  
                            boxDaLat.append(first_box)
                            boxDaLat.append(second_box)
                            first_box = None
                            second_box = None
                        else:
                            tg_Dung = time.time() # lấy thời gian hiện tại

    screen.blit(background, (0, 0)) # hiển thị bg

    if tg_Dung is not None and (time.time() - tg_Dung > 1):
        if second_box is not None:
            boxDaThay.remove(first_box)
            boxDaThay.remove(second_box)
        first_box = None
        second_box = None
        tg_Dung = None

    for i in range(soHang):
        for j in range(soCot):  
            x = j * (sizeBox + khoangCach)  + leX
            y = i * (sizeBox + khoangCach) + leY
            if (i, j) in boxDaThay or (i, j) in boxDaLat:
                screen.blit(images_table[i][j], (x, y)) # blit hiển thị hình ảnh có sẵn
            else:
                pygame.draw.rect(screen, white, (x, y, sizeBox, sizeBox), width=0)  #rect: hình chữ nhật, draw vẽ hình chưa có

    pygame.display.flip()

pygame.quit()