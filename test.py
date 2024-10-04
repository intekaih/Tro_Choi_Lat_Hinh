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
screen = pygame.display.set_icon(icon)  # define
screen = pygame.display.set_mode((chieuNgang, chieuCao))  # define

images = input_images()
images = images * 2
random_images(images)

images_table = load_images(images)  # bảng hình ảnh

# Khai báo biến hoạt ảnh
current_x = 0  # Vị trí hiện tại để vẽ hình ảnh
speed = 1  # Tốc độ vẽ hình ảnh
last_update_time = pygame.time.get_ticks()  # Thời gian cập nhật lần cuối

# Danh sách để lưu ô đã lật
boxDaLat = []
boxDaThay = []

# Chạy chương trình 
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Kiểm tra sự kiện nhấn chuột (nếu cần)

    # Cập nhật vị trí vẽ hình ảnh
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > 50:  # Thay đổi giá trị này để điều chỉnh tốc độ
        current_x += speed
        last_update_time = current_time

    # Reset vị trí khi đã vẽ hết màn hình
    if current_x > chieuNgang:
        current_x = 0  # Hoặc có thể dừng lại, tùy theo yêu cầu

    screen.blit(background, (0, 0))  # hiển thị bg

    # Vẽ hình ảnh ở vị trí hiện tại
    for i in range(soHang):
        for j in range(soCot):
            x = j * (sizeBox + khoangCach) + leX
            y = i * (sizeBox + khoangCach) + leY

            # Nếu hình ảnh chưa được vẽ, vẽ hình ảnh từ trái sang phải
            if x < current_x:
                screen.blit(images_table[i][j], (x, y))
            else:
                # Vẽ hình chữ nhật màu trắng để che
                pygame.draw.rect(screen, white, (x, y, sizeBox, sizeBox))

    pygame.display.flip()  # Cập nhật màn hình

pygame.quit()
