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
WIDTH, HEIGHT = 1920, 1080
#WIDTH, HEIGHT = 1536, 864
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("微積分選擇題遊戲")


# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DEEP_BLUE = (30, 30, 100)


#重製等待時間
waiting_time = 5


#載入音樂
pygame.mixer.music.load(os.path.join("music", "Lobby-Time.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


#載入圖片
background_image = pygame.image.load(os.path.join("image", "background-1920x1080.png")).convert()
#background_image = pygame.image.load(os.path.join("image", "background-1536x864.png")).convert()
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
    "questions": ["設f(x)=x[x]，求f'(0)?"],
    "options": ["(1). -3", "(2). 0", "(3). 不存在", "(4). 3"],
    "correct_answer": 3,
    "used": False
}
question_2 = {
    "questions": ["設一方程式f(x)=2x+4，求其與x=0，x=4，y=0所圍成的", "區域面積R為何?"],
    "options": ["(1). 12", "(2). 16", "(3). 48", "(4). 32"],
    "correct_answer": 4,
    "used": False
}
question_3 = {
    "questions": ["設f(x)=|x²-4|，求f'(2)為?"],
    "options": ["(1). 不存在", "(2). 4", "(3). 9", "(4). 0"],
    "correct_answer": 1,
    "used": False
}
question_4 = {
    "questions": ["設一方程式f(x)=x³+9x+25，求f(3)的二階導數?"],
    "options": ["(1). 45", "(2). 18", "(3). 25", "(4). 9"],
    "correct_answer": 2,
    "used": False
}
question_5 = {
    "questions": ["求(1²+2²+...+n² / 2n³+3n-1)，且n極限趨近於→∞之值?"],
    "options": ["(1). 1/6", "(2). ∞", "(3). 1/n", "(4). n²"],
    "correct_answer": 1,
    "used": False
}


#包含題目的陣列
all_questions = [question_1, question_2, question_3, question_4, question_5]


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
    draw_text_center(screen, '*手勢辨識*', 70, WIDTH/2, HEIGHT/2-200, BLACK)  #引用draw_text函式
    draw_text_center(screen, '選擇題遊戲', 70, WIDTH/2, HEIGHT/2 -100, BLACK) 
    draw_text_center(screen, '按下任意鍵開始遊戲', 50, WIDTH/2, HEIGHT/2 -10, BLACK) 
    draw_text_center(screen, '<遊戲說明>', 36, WIDTH/2, HEIGHT/2 + 50, DEEP_BLUE)
    draw_text_center(screen, '手比出數字可以選擇選項；確定選項後再比*0*作為確認答案', 36, WIDTH/2, HEIGHT/2 + 100, DEEP_BLUE)  
    draw_text_center(screen, '*小提醒：手掌要對著鏡頭喔:D*', 36, WIDTH/2, HEIGHT/2 + 150, DEEP_BLUE)
    pygame.display.flip()  #更新畫面
    waiting = True
    while waiting and not show_final:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #停止運行
                return True
            elif event.type == pygame.KEYUP: #若按下鍵盤鍵
                waiting = False
                return False


#結束畫面
def final_interface():
    global show_init, show_final, waiting_time
    draw_text_center(screen, '遊戲結束', 64, WIDTH/2, HEIGHT/4, BLACK)
    draw_text_center(screen, '總分:'+str(score), 64, WIDTH/2, HEIGHT/4+100, RED) 
    #是否及格
    if score >= 60:
        draw_text_center(screen, '":D 及格了，真棒"', 50, WIDTH/2, HEIGHT/4 + 260, BLUE)
    elif score < 60:
        draw_text_center(screen, '"x0 可惜了，沒及格"', 50, WIDTH/2, HEIGHT/4 + 260, BLUE)
    draw_text_center(screen, str(waiting_time)+'秒後回到首頁', 50, WIDTH/2, HEIGHT/4 + 340, DEEP_BLUE)
    pygame.display.flip()
    time.sleep(1) #停滯1秒
    waiting_time -= 1
    if waiting_time == 0:
        show_final = False
        show_init = True
        all_questions.extend([question_1, question_2, question_3, question_4, question_5])


#畫出紅色框
def red_frame(surf, x, frame_y):
    Bar_Length = 800  #長度
    Bar_Height = 80   #高度
    outline_rect = pygame.Rect(x, frame_y, Bar_Length, Bar_Height)  #外框
    pygame.draw.rect(surf, RED, outline_rect, 5)  #畫出(在甚麼平面, 顏色, outline_rect, 像素)


# 隨機選擇一個題目
def Q_random(all_questions):
    global current_question, question_text, options, correct_answer, show_init, show_final, waiting_time
    red_frame(screen, 0, 10000)
    if not all_questions:  
        #開啟總結畫面
        show_final = True 
        waiting_time = 5
        return
    current_question = random.choice(all_questions) #隨機選擇一個未使用過的題目
    all_questions.remove(current_question)  # 從列表中移除已選擇的題目
    question_text = current_question["questions"] #題目 = 選到之題目
    options = current_question["options"] #選項 = 選到題目之選項
    correct_answer = current_question["correct_answer"] #答案 = 選到題目之答案
    

#顯示問題
def display_question(question_text, options):
    screen.fill(WHITE)
    screen.blit(background_image, (0,0))

    #題目
    #y = 120
    y = 180
    for question in question_text: #可換行
        draw_text_left(screen, question, 42, 250, y, BLACK)
        y += 60

    #選項
    #y = 280
    y = 340
    for option in options:
        draw_text_left(screen, option, 42, 280, y, BLACK)
        y += 100

    #紀錄
    draw_text_left(screen, '得分:'+str(score)+'/100', 42, 1500, 180, RED)
    draw_text_left(screen, '已作答:'+str(4 - len(all_questions))+'/5', 42, 1500, 240, RED)
    if selected_answer != None:
        #red_frame(screen, 180 - 5, frame_y)
        red_frame(screen, 280 - 5, frame_y)
    else:
        red_frame(screen, 0, 10000)
    pygame.display.flip()

'''
def display_question(question_text, options):
    screen.fill(WHITE)
    screen.blit(background_image, (0,0))

    y = 120
    for question in question_text:
        draw_text_left(screen, question, 42, 150, y, BLACK)
        y += 60

    y = 280
    for option in options:
        draw_text_left(screen, option, 42, 180, y, BLACK)
        y += 100

    draw_text_left(screen, '得分:'+str(score)+'/100', 42, 1200, 120, RED)
    draw_text_left(screen, '已作答:'+str(4 - len(all_questions))+'/5', 42, 1200, 180, RED)
    if selected_answer != None:
        red_frame(screen, 180 - 5, frame_y)
    else:
        red_frame(screen, 0, 10000)
    pygame.display.flip()
'''


#按鍵函式
def keydown():
    global selected_answer, frame_y
    if not show_final:
        #若1234其中之一被按下
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
            frame_y = 340 + (selected_answer - 1) * 100 -20
            #frame_y = 280 + (selected_answer - 1) * 100 -20 


#確認答案&顯示
def ans_checking():
    global selected_answer, score
    if event.key == pygame.K_0:
        if selected_answer is not None:
            #答對
            if selected_answer == correct_answer:
                #print("Correct!")
                score += 20
                draw_text_center(screen, 'well done! 答對了 :> !', 64, WIDTH/2, HEIGHT/2, RED)
                pygame.display.flip()  #更新畫面
                time.sleep(1)
            #答錯
            else:
                #print("Incorrect!")
                score += 0
                draw_text_center(screen, 'too sad 答錯了 :<', 64 , WIDTH/2, HEIGHT/2, RED)        
                pygame.display.flip()  #更新畫面
                time.sleep(1)
            selected_answer = None
            #選擇完答案後，再次隨機選擇一個題目並顯示
            Q_random(all_questions)
            display_question(question_text, options)
        #else:
            #print("Please select an answer first!")
        


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
        if close:
            break
        Initial_interface()
        show_init = False
        # 顯示題目
        Q_random(all_questions)
        display_question(question_text, options)

    if show_final:
        final_interface()

    if not show_final:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keydown()
                ans_checking()
                display_question(question_text, options)

    clock.tick(FPS)
pygame.quit()
sys.exit()