import pygame
import random
import os
import time

# Khởi tạo Pygame
pygame.init()

# Thiết lập các biến khác
soLuongHang = 4
soLuongCot = 4
doDaiLuoi = 10
doDaiThe = 100

# Thiết lập kích thước màn hình
WIDTH = (doDaiThe + doDaiLuoi)* soLuongHang - doDaiLuoi
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Xếp Hình")

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tạo đường dẫn đến thư mục chứa hình ảnh và âm thanh
IMAGE_DIR = "images"
SOUND_DIR = "sounds"

# Khởi tạo các biến toàn cục
ThoiGianTroChoi = 0  # giây
tgcongthem = 0  

# Tải hình ảnh vào một danh sách
def load_images():
    images = []
    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = pygame.image.load(os.path.join(IMAGE_DIR, filename))
            img = pygame.transform.scale(img, (doDaiThe, doDaiThe))  # Thay đổi kích thước hình ảnh
            images.append(img)
    return images

def XoaTronHinhAnh(array):
    """ Xáo trộn danh sách sử dụng thuật toán Fisher-Yates """
    for i in range(len(array) - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]

def reset_game():
    global images, luoiNganCacThe, theDaThay, theDaLat, theLatDauTien, theLatThuHai, tg1thelat, tgconlai, game_started, lost

    images = load_images()
    images = images * 2  # Nhân đôi số lượng hình ảnh để có 2 hình giống nhau
    XoaTronHinhAnh(images)  # Trộn hình ảnh

    luoiNganCacThe = []
    for i in range(soLuongHang):
        row = []
        for j in range(soLuongCot):
            row.append(images.pop())
        luoiNganCacThe.append(row)

    theDaThay = []
    theDaLat = []
    theLatDauTien = None
    theLatThuHai = None
    tg1thelat = None
    tgconlai = ThoiGianTroChoi
    game_started = False
    lost = False

# Tải âm thanh
def load_sounds():
    sounds = {
        "flip": pygame.mixer.Sound(os.path.join(SOUND_DIR, "flip.wav")),
        "match": pygame.mixer.Sound(os.path.join(SOUND_DIR, "match.wav")),
        "no_match": pygame.mixer.Sound(os.path.join(SOUND_DIR, "no_match.wav")),
        "game_over": pygame.mixer.Sound(os.path.join(SOUND_DIR, "game_over.mp3")),
        "victory": pygame.mixer.Sound(os.path.join(SOUND_DIR, "victory.mp3"))
    }
    return sounds

sounds = load_sounds()



# Khởi tạo trò chơi
reset_game()

# Tạo font cho các nút và thời gian
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock() 
running = True
victory = False  # Biến để kiểm tra trạng thái chiến thắng

# Các biến để lưu trạng thái chế độ
mode = None
show_mode_buttons = False  # Biến để kiểm tra trạng thái hiển thị các nút chọn chế độ

def draw_mode_buttons():
    global mode

    if easy_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            mode = 'easy'
            return True
    elif medium_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            mode = 'medium'
            return True
    elif hard_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            mode = 'hard'
            return True

    return False

while running:
    PINK = (255, 192, 203)
    screen.fill(PINK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Kiểm tra nếu nút "Start" được nhấp
            if start_button.collidepoint(event.pos):
                if not game_started:
                    show_mode_buttons = True  # Hiện các nút chọn chế độ khi nhấn "Start"
                else:
                    if mode:
                        if mode == 'easy':
                            ThoiGianTroChoi = 20
                            tgcongthem = 5
                        elif mode == 'medium':
                            ThoiGianTroChoi = 15
                            tgcongthem = 5
                        elif mode == 'hard':
                            ThoiGianTroChoi = 10
                            tgcongthem = 3
                        reset_game()
                        game_started = True
                        tg1thelat = None  # Đặt lại thời điểm lật thẻ
                continue

            # Kiểm tra nếu nút "Restart" được nhấp
            if restart_button.collidepoint(event.pos):
                reset_game()
                victory = False
                lost = False
                mode = None  # Reset chế độ khi nhấn Restart
                show_mode_buttons = False  # Ẩn các nút chọn chế độ
                continue

            if show_mode_buttons:
                if draw_mode_buttons():
                    show_mode_buttons = False  # Ẩn các nút chọn chế độ sau khi chọn chế độ
                    if mode:
                        if mode == 'easy':
                            ThoiGianTroChoi = 20
                            tgcongthem = 5
                        elif mode == 'medium':
                            ThoiGianTroChoi = 15
                            tgcongthem = 4
                        elif mode == 'hard':
                            ThoiGianTroChoi = 10
                            tgcongthem = 3
                        reset_game()
                        game_started = True
                        tg1thelat = None  # Đặt lại thời điểm lật thẻ
                    continue

            if game_started:
                # Xử lý nhấp chuột trên lưới
                cot = x // (100 + doDaiLuoi)
                hang = y // (100 + doDaiLuoi)

                # Kiểm tra chỉ số hợp lệ
                if 0 <= hang < soLuongHang and 0 <= cot < soLuongCot:
                    if (hang, cot) not in theDaThay and (hang, cot) not in theDaLat:
                        if theLatDauTien is None:
                            theLatDauTien = (hang, cot)
                            theDaThay.append(theLatDauTien)
                            sounds["flip"].play()  # Phát âm thanh khi lật thẻ
                        elif theLatThuHai is None:
                            theLatThuHai = (hang, cot)
                            theDaThay.append(theLatThuHai)
                            sounds["flip"].play()  # Phát âm thanh khi lật thẻ

                            # Kiểm tra nếu hai thẻ lật giống nhau
                            if luoiNganCacThe[theLatDauTien[0]][theLatDauTien[1]] == luoiNganCacThe[theLatThuHai[0]][theLatThuHai[1]]:
                                theDaLat.append(theLatDauTien)
                                theDaLat.append(theLatThuHai)
                                tgconlai += tgcongthem  # Thêm thời gian khi tìm đúng
                                sounds["match"].play()  # Phát âm thanh khi tìm thấy cặp giống nhau
                                theLatDauTien = None
                                theLatThuHai = None
                            else:
                                tg1thelat = time.time()  # Ghi lại thời điểm lật hai thẻ
                                sounds["no_match"].play()  # Phát âm thanh khi không tìm thấy cặp giống nhau

    # Kiểm tra thời gian đã trôi qua để lật lại thẻ nếu không khớp
    if tg1thelat is not None and (time.time() - tg1thelat) > 0.5:
        if theLatThuHai is not None:
            theDaThay.remove(theLatDauTien)
            theDaThay.remove(theLatThuHai)
        tg1thelat = None
        theLatDauTien = None
        theLatThuHai = None

    # Cập nhật thời gian còn lại nếu trò chơi đã bắt đầu
    if game_started:
        tgconlai -= clock.get_time() / 1000  # Giảm thời gian theo thời gian đã trôi qua
        if tgconlai <= 0:
            sounds["game_over"].play()  # Phát âm thanh khi hết thời gian
            lost = True
            game_started = False

    # Kiểm tra nếu trò chơi đã chiến thắng
    if game_started and len(theDaLat) == soLuongHang * soLuongCot:
        victory = True
        sounds["victory"].play()  # Phát âm thanh chiến thắng
        game_started = False

    # Vẽ hình ảnh
    for i in range(soLuongHang):
        for j in range(soLuongCot):
            x = j * (doDaiThe + doDaiLuoi)
            y = i * (doDaiThe + doDaiLuoi)
            if (i, j) in theDaThay or (i, j) in theDaLat:
                screen.blit(luoiNganCacThe[i][j], (x, y))
            else:
                pygame.draw.rect(screen, BLACK, (x, y, 100, 100))

    # Vẽ nút "Start" và "Restart"
    start_button = pygame.draw.rect(screen, GREEN, (WIDTH / 2 - 50, HEIGHT -50, 100, 40))
    restart_button = pygame.draw.rect(screen, GREEN, (320 , HEIGHT - 50, 100, 40))
    start_text = font.render('Start', True, WHITE)
    restart_text = font.render('Restart', True, WHITE)
    screen.blit(start_text, (WIDTH / 2 - 30, HEIGHT -40))
    screen.blit(restart_text, (330 , HEIGHT - 40))

    # Nếu chưa chọn chế độ và chưa nhấn Start, không hiển thị nút chế độ
    if not game_started:
        if show_mode_buttons:
            easy_button = pygame.draw.rect(screen, GREEN, (WIDTH / 2 - 180, HEIGHT - 110, 80, 40))
            medium_button = pygame.draw.rect(screen, GREEN, (WIDTH / 2 -60, HEIGHT - 110, 120, 40))
            hard_button = pygame.draw.rect(screen, GREEN, (WIDTH / 2 + 90, HEIGHT - 110, 80, 40))
            
            easy_text = font.render('Easy', True, WHITE)
            medium_text = font.render('Medium', True, WHITE)
            hard_text = font.render('Hard', True, WHITE)
            
            screen.blit(easy_text, (WIDTH / 2 - 170, HEIGHT  - 100))
            screen.blit(medium_text, (WIDTH / 2 - 50, HEIGHT  - 100))
            screen.blit(hard_text, (WIDTH / 2 + 100, HEIGHT  - 100))
        
        # Hiển thị tên chế độ sau khi chọn
        if mode:
            mode_text = font.render(f'Mode: {mode}', True, BLACK)
            screen.blit(mode_text, (10, 500))
    else:
        # Hiển thị tên chế độ sau khi chọn
        if mode:
            mode_text = font.render(f'Mode: {mode}', True, BLACK)
            screen.blit(mode_text, (10, 500))

    # Hiển thị thời gian còn lại nếu trò chơi đã bắt đầu
    if game_started:
        timer_text = font.render(f'Time: {int(tgconlai)}', True, BLACK)
        screen.blit(timer_text, (10, HEIGHT - 50))
    elif victory:
        victory_text = font.render('You Win!', True, GREEN)
        screen.blit(victory_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    elif lost:
        lost_text = font.render('You Lost!', True, RED)
        restart_message = font.render('Click Restart to Try Again', True, RED)
        screen.blit(lost_text, (WIDTH / 2 - 60, HEIGHT -160))
        screen.blit(restart_message, (WIDTH / 2 - 140, HEIGHT -130))
    elif not mode and show_mode_buttons:
        start_message = font.render('Choose Mode and Click Start', True, RED)
        screen.blit(start_message, (WIDTH / 2 - 180, HEIGHT  - 150))


    
    pygame.display.flip()
    clock.tick(120) 

pygame.quit()
