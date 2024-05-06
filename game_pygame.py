import pygame
import random
import sys
import os
import time

FPS = 60
clock = pygame.time.Clock()

# 初始化 Pygame
pygame.init()

# 設置視窗
WIDTH, HEIGHT = 1536, 864
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("高中選擇題遊戲")

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#載入音樂
pygame.mixer.music.load(os.path.join("music", "Lobby-Time.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#載入圖片
background_image = pygame.image.load(os.path.join("image", "background.png")).convert()
mini_image = pygame.image.load(os.path.join("image", "python.webp")).convert()

#設定視窗圖片
pygame.display.set_icon(mini_image)  

# 定義題目和選項
'''
問題,
選項,
答案
'''
# 定義每個題目
question_1 = {
    "question": "設一方程式為f(x)=x²+3x-1，求f(2)時的切線斜率?",
    "options": ["(1). 3", "(2). 5", "(3). 7", "(4). 6"],
    "correct_answer": 3,
    "used": False
}
question_2 = {
    "question": "What is the largest planet in our solar system?",
    "options": ["(1). Earth", "(2). Jupiter", "(3). Saturn", "(4). Mars"],
    "correct_answer": 2,
    "used": False
}
question_3 = {
    "question": "Who painted the Mona Lisa?",
    "options": ["(1). Leonardo da Vinci", "(2). Vincent van Gogh", "(3). Pablo Picasso", "(4). Michelangelo"],
    "correct_answer": 1,
    "used": False
}
question_4 = {
    "question": "What is the chemical symbol for water?",
    "options": ["(1). H2O", "(2). CO2", "(3). NaCl", "(4). O2"],
    "correct_answer": 1,
    "used": False
}
question_5 = {
    "question": "Which planet is known as the Red Planet?",
    "options": ["(1). Mars", "(2). Venus", "(3). Jupiter", "(4). Saturn"],
    "correct_answer": 1,
    "used": False
}

#包含題目的陣列
questions = [question_1, question_2, question_3, question_4, question_5]

#引用字體
font_name = os.path.join("Iansui-Regular.ttf")   

#顯示字串(靠左)
def draw_text_left(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size) #設定字體和大小
    text_surface = font.render(text, True, color)
    surf.blit(text_surface, (x, y))  #畫出(圖片,位置)

#顯示字串(置中)
def draw_text_center(surf, text, size, x, y, color):   #畫出字體(表面,文字,大小,x座標,y座標)
    font = pygame.font.Font(font_name, size) #設定字體和大小
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()  #定位
    text_rect.centerx = x  #訂出位置
    text_rect.centery = y #訂出位置
    surf.blit(text_surface, text_rect)  #畫出(圖片,位置)

#初始介面
def Initial_interface():
    draw_text_center(screen, '*手勢辨識*', 64, WIDTH/2, HEIGHT/2 - 100, BLACK)  #引用draw_text函式
    draw_text_center(screen, '選擇題遊戲', 64, WIDTH/2, HEIGHT/2, BLACK) 
    draw_text_center(screen, '按下任意鍵開始遊戲', 50, WIDTH/2, HEIGHT/2 + 100, BLACK) 
    pygame.display.update()  #更新畫面
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #若關閉式窗
                pygame.quit()     #停止運行
                return True
            elif event.type == pygame.KEYUP:  #若按下鍵盤鍵
                waiting = False
                return False

#結束畫面
def final_interface():
    global show_init, show_final
    draw_text_center(screen, '遊戲結束', 64, WIDTH/2, HEIGHT/4, BLACK)
    draw_text_center(screen, '總分:'+str(score), 64, WIDTH/2, HEIGHT/4+100, BLACK)
    pygame.display.update()
    time.sleep(5)
    show_final = False
    show_init = True

#畫出紅色框
def red_frame(surf, x, frame_y):
    Bar_Length = 800  #長度
    Bar_Height = 80   #高度
    outline_rect = pygame.Rect(x, frame_y, Bar_Length, Bar_Height)  #外框
    pygame.draw.rect(surf, RED, outline_rect, 5)  #畫出(在甚麼平面, 顏色, outline_rect, 像素)

# 隨機選擇一個題目
def Q_random(questions):
    global current_question, question_text, options, correct_answer, show_init, show_final
    red_frame(screen, 0, 1000)
    if not questions:  # 如果所有題目都已經使用完畢，重新加入所有題目
        show_final = True
        questions.extend([question_1, question_2, question_3, question_4, question_5])
    current_question = random.choice(questions) #隨機選擇一個未使用過的題目
    questions.remove(current_question)  # 從列表中移除已選擇的題目
    question_text = current_question["question"] #放入字串
    options = current_question["options"] #選項 = 選到題目之選項
    correct_answer = current_question["correct_answer"] #答案 = 選到題目之答案
    
#顯示問題
def display_question(question, options):
    screen.fill(WHITE)
    screen.blit(background_image, (0,0))
    draw_text_left(screen, question, 42, 150, 120, BLACK)
    y = 250
    for option in options:
        draw_text_left(screen, option, 42, 180, y, BLACK)
        y += 100
    draw_text_left(screen, '得分:'+str(score)+'/100', 42, 1200, 120, RED)
    if selected_answer != None:
        red_frame(screen, 180 - 5, frame_y)
    else:
        red_frame(screen, 0, 1000)
    pygame.display.flip()
    
#按鍵函式
def keydown():
    global selected_answer, frame_y
    if event.key == pygame.K_1:
        selected_answer = 1
        print(1)
    elif event.key == pygame.K_2:
        selected_answer = 2
        print(2)
    elif event.key == pygame.K_3:
        selected_answer = 3
        print(3)
    elif event.key == pygame.K_4:
        selected_answer = 4
        print(4)
    if selected_answer != None:
        frame_y = 250 + (selected_answer - 1) * 100 -20
    
#確認答案&顯示
def ans_checking():
    global selected_answer, score
    if event.key == pygame.K_0:
        if selected_answer is not None:
            if selected_answer == correct_answer:
                print("Correct!")
                score += 20
                draw_text_center(screen, 'well done! 答對了 :> !', 64, WIDTH/2, HEIGHT/2, RED)
                pygame.display.flip()  #更新畫面
                time.sleep(1.5)
            else:
                print("Incorrect!")
                score += 0
                draw_text_center(screen, 'too sad 答錯了 :<', 64 , WIDTH/2, HEIGHT/2, RED)        
                pygame.display.flip()  #更新畫面
                time.sleep(1.5)
            selected_answer = None
            #選擇完答案後，再次隨機選擇一個題目並顯示
            Q_random(questions)
            display_question(question_text, options)
        else:
            print("Please select an answer first!")
        


# 主遊戲迴圈
show_init = True
show_final = False
running = True
selected_answer = None
score = 0
frame_y = 0

while running:
    screen.fill(WHITE)
    screen.blit(background_image, (0,0))
    if show_init:
        score = 0
        close = Initial_interface()
        if Initial_interface():
            break
        Initial_interface()
        show_init = False
        # 顯示題目
        Q_random(questions)
        display_question(question_text, options)
    if show_final:
        final_interface()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keydown()
            ans_checking()
            display_question(question_text, options)
    
pygame.quit()
sys.exit()