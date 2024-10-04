import random, pygame, sys
from pygame.locals import *

FPS = 30  # khung hình trên giây, tốc độ chung của chương trình
chieuRong = 640  # kích thước chiều rộng của cửa sổ (pixel)
chieuDai = 480  # kích thước chiều cao của cửa sổ (pixel)
tocDoHienVaAn = 10  # tốc độ trượt khi hiện và che hộp
kichCoBox = 40  # kích thước chiều cao và chiều rộng của hộp (pixel)
khoangCachBox = 10  # kích thước khoảng cách giữa các hộp (pixel)
soCot = 5  # số cột của biểu tượng
soHang = 4  # số hàng của biểu tượng
assert (soCot * soHang) % 2 == 0, 'Bảng cần có số hộp chẵn để ghép cặp.' # Đảm bảo số box là chẵn
XMARGIN = int((chieuRong - (soCot * (kichCoBox + khoangCachBox))) / 2)  # khoảng cách bên trái
YMARGIN = int((chieuDai - (soHang * (kichCoBox + khoangCachBox))) / 2)  # khoảng cách phía trên


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

mauNen = NAVYBLUE
LIGHTBGCOLOR = GRAY
mauBox = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)  # Tất cả các màu sắc
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)  # Tất cả các hình dạng
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= soCot * soHang, "Bảng quá lớn so với số hình dạng/màu sắc đã định nghĩa."

def main():
    global FPSCLOCK, cuaSoHienThi
    pygame.init()  # Khởi tạo Pygame
    FPSCLOCK = pygame.time.Clock()  # Tạo đồng hồ để điều chỉnh FPS
    cuaSoHienThi = pygame.display.set_mode((chieuRong, chieuDai))  # Tạo cửa sổ hiển thị

    mousex = 0  # dùng để lưu tọa độ x của sự kiện chuột
    mousey = 0  # dùng để lưu tọa độ y của sự kiện chuột
    pygame.display.set_caption('Memory Game')  # Đặt tiêu đề cho cửa sổ

    mainBoard = getRandomizedBoard()  # Lấy bảng ngẫu nhiên
    trangThaiBox = TrangThaiBox(False)  # Tạo dữ liệu cho các hộp đã được lật

    hopDauTien = None  # lưu trữ (x, y) của hộp đầu tiên được nhấp.

    cuaSoHienThi.fill(mauNen)  # Điền màu nền cho cửa sổ
    gameStar(mainBoard)  # Bắt đầu hoạt động của trò chơi

    while True:  # vòng lặp chính của trò chơi
        mouseClicked = False  # Biến kiểm tra xem chuột có được nhấp hay không

        cuaSoHienThi.fill(mauNen)  # Vẽ lại cửa sổ
        veBang(mainBoard, trangThaiBox)  # Vẽ bảng

        for event in pygame.event.get():  # Vòng lặp xử lý sự kiện
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()  # Đóng Pygame
                sys.exit()  # Thoát chương trình
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos  # Lấy tọa độ chuột khi di chuyển
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos  # Lấy tọa độ chuột khi nhấp
                mouseClicked = True  # Đánh dấu chuột đã được nhấp

        boxx, boxy = getBoxAtPixel(mousex, mousey)  # Lấy vị trí hộp tại tọa độ chuột
        if boxx != None and boxy != None:
            # Chuột hiện đang ở trên một hộp.
            if not trangThaiBox[boxx][boxy]:  # Nếu hộp chưa được lật
                drawHighlightBox(boxx, boxy)  # Vẽ viền cho hộp

            if not trangThaiBox[boxx][boxy] and mouseClicked:  # Nếu hộp chưa được lật và chuột đã được nhấp
                hienBox(mainBoard, [(boxx, boxy)])  # Lật hộp
                trangThaiBox[boxx][boxy] = True  # Đánh dấu hộp là "đã lật"
                if hopDauTien == None:  # Hộp hiện tại là hộp đầu tiên được nhấp
                    hopDauTien = (boxx, boxy)  # Lưu hộp đầu tiên
                else:  # Hộp hiện tại là hộp thứ hai được nhấp
                    # Kiểm tra xem có khớp giữa hai biểu tượng hay không.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, hopDauTien[0], hopDauTien[1])  # Lấy hình dạng và màu của biểu tượng đầu tiên
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)  # Lấy hình dạng và màu của biểu tượng thứ hai

                    if icon1shape != icon2shape or icon1color != icon2color:  # Biểu tượng không khớp
                        # Không khớp. Đậy lại cả hai lựa chọn.
                        pygame.time.wait(1000)  # Chờ 1 giây
                        anBox(mainBoard, [(hopDauTien[0], hopDauTien[1]), (boxx, boxy)])  # Đậy lại các hộp
                        trangThaiBox[hopDauTien[0]][hopDauTien[1]] = False  # Đánh dấu hộp đầu tiên là "chưa lật"
                        trangThaiBox[boxx][boxy] = False  # Đánh dấu hộp thứ hai là "chưa lật"
                    elif CheckWin(trangThaiBox):  # Kiểm tra xem đã tìm được tất cả cặp chưa
                        gameWin(mainBoard)  # Hiện hoạt động khi thắng
                        pygame.time.wait(2000)  # Chờ 2 giây

                        # Đặt lại bảng
                        mainBoard = getRandomizedBoard()  # Lấy bảng ngẫu nhiên
                        trangThaiBox = TrangThaiBox(False)  # Tạo lại dữ liệu cho các hộp

                        # Hiện bảng chưa lật trong một giây.
                        veBang(mainBoard, trangThaiBox)  # Vẽ lại bảng
                        pygame.display.update()  # Cập nhật cửa sổ
                        pygame.time.wait(1000)  # Chờ 1 giây

                        # Phát lại hoạt động bắt đầu trò chơi.
                        gameStar(mainBoard)  # Bắt đầu hoạt động trò chơi lại
                    hopDauTien = None  # Đặt lại biến firstSelection

        # Vẽ lại màn hình và chờ một tick của đồng hồ.
        pygame.display.update()  # Cập nhật màn hình
        FPSCLOCK.tick(FPS)  # Điều chỉnh tốc độ khung hình


def TrangThaiBox(val):
    trangThaiBox = []  # Danh sách để lưu trữ trạng thái các hộp
    for i in range(soCot):
        trangThaiBox.append([val] * soHang)  # Thêm một hàng mới với tất cả các hộp đều có giá trị 'val'
    return trangThaiBox  # Trả về danh sách trạng thái các hộp


def getRandomizedBoard():
    # Lấy danh sách tất cả các hình dạng với tất cả các màu sắc có thể.
    icons = []  # Danh sách để lưu trữ các biểu tượng
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))  # Thêm cặp (hình dạng, màu sắc) vào danh sách

    random.shuffle(icons)  # Xáo trộn thứ tự của danh sách biểu tượng
    numIconsUsed = int(soCot * soHang / 2)  # Tính số lượng biểu tượng cần thiết
    icons = icons[:numIconsUsed] * 2  # Tạo ra hai biểu tượng cho mỗi biểu tượng đã chọn
    random.shuffle(icons)  # Xáo trộn lại danh sách biểu tượng

    # Tạo cấu trúc dữ liệu cho bảng, với các biểu tượng được đặt ngẫu nhiên.
    board = []  # Danh sách để lưu trữ bảng
    for x in range(soCot):
        column = []  # Danh sách để lưu trữ một cột của bảng
        for y in range(soHang):
            column.append(icons[0])  # Thêm biểu tượng đầu tiên vào cột
            del icons[0]  # Xóa biểu tượng khỏi danh sách khi đã gán
        board.append(column)  # Thêm cột vào bảng
    return board  # Trả về bảng với các biểu tượng được sắp xếp ngẫu nhiên


def ChiaNhom(sizeNhom, danhSach):
    # Chia một danh sách thành các danh sách con, 
    # trong đó các danh sách con có tối đa groupSize số mục.
    ketQua = []  # Danh sách để lưu trữ kết quả
    for i in range(0, len(danhSach), sizeNhom):
        ketQua.append(danhSach[i:i + sizeNhom])  # Thêm các nhóm vào danh sách kết quả
    return ketQua  # Trả về danh sách các nhóm


def xyBangToxyPixel(boxx, boxy):
    # Chuyển đổi tọa độ trên bảng thành tọa độ pixel
    left = boxx * (kichCoBox + khoangCachBox) + XMARGIN  # Tính tọa độ bên trái
    top = boxy * (kichCoBox + khoangCachBox) + YMARGIN  # Tính tọa độ trên
    return (left, top)  # Trả về tọa độ (left, top)


def getBoxAtPixel(x, y):
    # Tìm hộp tương ứng với tọa độ pixel (x, y)
    for boxx in range(soCot):
        for boxy in range(soHang):
            left, top = xyBangToxyPixel(boxx, boxy)  # Lấy tọa độ pixel từ tọa độ trên bảng
            boxRect = pygame.Rect(left, top, kichCoBox, kichCoBox)  # Tạo hình chữ nhật cho hộp
            if boxRect.collidepoint(x, y):  # Kiểm tra xem pixel có nằm trong hộp không
                return (boxx, boxy)  # Trả về tọa độ trên bảng của hộp
    return (None, None)  # Nếu không tìm thấy hộp, trả về None


def drawIcon(shape, color, boxx, boxy):
    # Vẽ biểu tượng với hình dạng và màu sắc đã cho ở tọa độ (boxx, boxy)
    quarter = int(kichCoBox * 0.25)  # Một phần tư kích thước hộp
    half = int(kichCoBox * 0.5)  # Một nửa kích thước hộp

    left, top = xyBangToxyPixel(boxx, boxy)  # Lấy tọa độ pixel từ tọa độ trên bảng
    # Vẽ các hình dạng
    if shape == DONUT:
        pygame.draw.circle(cuaSoHienThi, color, (left + half, top + half), half - 5)  # Vẽ hình tròn ngoài
        pygame.draw.circle(cuaSoHienThi, mauNen, (left + half, top + half), quarter - 5)  # Vẽ hình tròn trong
    elif shape == SQUARE:
        pygame.draw.rect(cuaSoHienThi, color, (left + quarter, top + quarter, kichCoBox - half, kichCoBox - half))  # Vẽ hình vuông
    elif shape == DIAMOND:
        pygame.draw.polygon(cuaSoHienThi, color, ((left + half, top), (left + kichCoBox - 1, top + half), (left + half, top + kichCoBox - 1), (left, top + half)))  # Vẽ hình thoi
    elif shape == LINES:
        for i in range(0, kichCoBox, 4):  # Vẽ các đường chéo
            pygame.draw.line(cuaSoHienThi, color, (left, top + i), (left + i, top))
            pygame.draw.line(cuaSoHienThi, color, (left + i, top + kichCoBox - 1), (left + kichCoBox - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(cuaSoHienThi, color, (left, top + quarter, kichCoBox, half))  # Vẽ hình elip


def getShapeAndColor(board, boxx, boxy):
    # Giá trị hình dạng cho vị trí x, y được lưu trong board[x][y][0]
    # Giá trị màu sắc cho vị trí x, y được lưu trong board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]  # Trả về hình dạng và màu sắc của hộp


def veBox(board, boxes, coverage):
    # Vẽ các hộp đang bị che phủ/tiết lộ. "boxes" là danh sách
    # của các danh sách hai mục, mỗi mục có vị trí x & y của hộp.
    for box in boxes:
        left, top = xyBangToxyPixel(box[0], box[1])  # Lấy tọa độ pixel của hộp
        pygame.draw.rect(cuaSoHienThi, mauNen, (left, top, kichCoBox, kichCoBox))  # Vẽ hộp với màu nền
        shape, color = getShapeAndColor(board, box[0], box[1])  # Lấy hình dạng và màu sắc của hộp
        drawIcon(shape, color, box[0], box[1])  # Vẽ biểu tượng trên hộp
        if coverage > 0:  # Chỉ vẽ lớp che nếu có độ che phủ
            pygame.draw.rect(cuaSoHienThi, mauBox, (left, top, coverage, kichCoBox))  # Vẽ lớp che
    pygame.display.update()  # Cập nhật màn hình
    FPSCLOCK.tick(FPS)  # Giới hạn tốc độ khung hình


def hienBox(board, boxesToReveal):
    # Thực hiện hoạt ảnh "tiết lộ hộp".
    for coverage in range(kichCoBox, (-tocDoHienVaAn) - 1, -tocDoHienVaAn):
        veBox(board, boxesToReveal, coverage)  # Vẽ các hộp đang được tiết lộ


def anBox(board, boxesToCover):
    # Thực hiện hoạt ảnh "che hộp".
    for coverage in range(0, kichCoBox + tocDoHienVaAn, tocDoHienVaAn):
        veBox(board, boxesToCover, coverage)  # Vẽ các hộp đang bị che


def veBang(board, revealed):
    # Vẽ tất cả các hộp trong trạng thái bị che hoặc đã được tiết lộ.
    for boxx in range(soCot):
        for boxy in range(soHang):
            left, top = xyBangToxyPixel(boxx, boxy)  # Lấy tọa độ pixel của hộp
            if not revealed[boxx][boxy]:
                # Vẽ một hộp bị che.
                pygame.draw.rect(cuaSoHienThi, mauBox, (left, top, kichCoBox, kichCoBox))  # Vẽ hộp với màu che
            else:
                # Vẽ biểu tượng (đã tiết lộ).
                shape, color = getShapeAndColor(board, boxx, boxy)  # Lấy hình dạng và màu sắc
                drawIcon(shape, color, boxx, boxy)  # Vẽ biểu tượng


def drawHighlightBox(boxx, boxy):
    # Vẽ hộp nổi bật để chỉ ra vị trí đang được chọn.
    left, top = xyBangToxyPixel(boxx, boxy)  # Lấy tọa độ pixel
    pygame.draw.rect(cuaSoHienThi, HIGHLIGHTCOLOR, (left - 5, top - 5, kichCoBox + 10, kichCoBox + 10), 4)  # Vẽ hình chữ nhật nổi bật


def gameStar(board):
    # Tiết lộ ngẫu nhiên các hộp 8 cái một lần.
    boxDaLat = TrangThaiBox(False)  # Tạo dữ liệu hộp đã che
    listBox = []
    for x in range(soCot):
        for y in range(soHang):
            listBox.append((x, y))  # Thêm tất cả các hộp vào danh sách
    random.shuffle(listBox)  # Xáo trộn danh sách các hộp
    nhomBox = ChiaNhom(2, listBox)  # Chia danh sách thành các nhóm 8 hộp

    veBang(board, boxDaLat)  # Vẽ bảng với các hộp bị che
    for boxGroup in nhomBox:
        hienBox(board, boxGroup)  # Tiết lộ nhóm hộp
        anBox(board, boxGroup)  # Che nhóm hộp lại


def gameWin(board):
    # Nháy màu nền khi người chơi chiến thắng
    BoDaLat = TrangThaiBox(True)  # Tạo dữ liệu hộp đã được tiết lộ
    color1 = LIGHTBGCOLOR  # Màu nền đầu tiên
    color2 = mauNen  # Màu nền thứ hai

    for i in range(3):
        color1, color2 = color2, color1  # Hoán đổi màu
        cuaSoHienThi.fill(color1)  # Điền màu nền
        veBang(board, BoDaLat)  # Vẽ bảng
        pygame.display.update()  # Cập nhật màn hình
        pygame.time.wait(300)  # Đợi 300 milliseconds


def CheckWin(boxDaLat):
    # Trả về True nếu tất cả các hộp đã được tiết lộ, nếu không thì False
    for i in boxDaLat:
        if False in i:
            return False  # Trả về False nếu có bất kỳ hộp nào bị che
    return True  # Nếu không, trả về True


if __name__ == '__main__':
    main()  # Bắt đầu chương trình chính
