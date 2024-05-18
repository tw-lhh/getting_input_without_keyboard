import cv2
import mediapipe as mp
import time
import keyboard
from cvzone.HandTrackingModule import HandDetector 
import cvzone

cap = cv2.VideoCapture(0) #開啟攝影機
mpHands = mp.solutions.hands # mediapipe 偵測手掌方法
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils # mediapipe 繪圖方法

#點與線的樣式
handLmsStyle =  mpDraw.DrawingSpec(color=(255,100, 50), thickness=4)
handConStyle =  mpDraw.DrawingSpec(color=(20, 255, 20), thickness=2)

pTime = 0 #先前時間
cTime = 0 #目前時間


#建立座標array
Px = [0] * 21
Py = [0] * 21

number = 0

#手指判斷變數
fg1, fg2, fg3, fg4 = False, False, False, False

#開為正，反之
fg00 = False

#正->0，右->1，左->2
palm_directions = 0

#右手正，左手負
rl_hand = True


#手掌開向辨識
def palm_direction(Px, Py):
    global palm_directions
    
    if Px[0] > Px[5] and Px[0] > Px[17]:
        palm_directions = 1 #右彎
    elif Px[5] > Px[0] and Px[17] > Px[0]:
        palm_directions = 2 #左彎
    elif Py[0] > Py[9]:
        palm_directions = 0 #正
        

#左、右手辨識
def right_or_left(Px, Py):
    global rl_hand
    if palm_directions == 1:
        if Py[17] > Py[5]:
            rl_hand = True
        elif Py[5] > Py[17]:
            rl_hand = False
    elif palm_directions == 2:
        if Py[5] > Py[17]:
            rl_hand = True
        elif Py[17] > Py[5]:
            rl_hand = False
    elif palm_directions == 0:
        if Px[5] > Px[17]:
            rl_hand = True#右手
        elif Px[5] < Px[17]:
            rl_hand = False#左手


#"手指開合"辨識:方向編號0
def finger_detecting_0(rl_hand, Px, Py):
    global fg1, fg2, fg3, fg4
    global fg00

    #大拇指(先進行左右手辨識，再辨識大拇指)
    if rl_hand:
        if Px[5] > Px[4]:
            fg00 = False
        elif Px[5] < Px[4]:
            fg00 = True

    elif rl_hand == False:
        if Px[5] < Px[4]:
            fg00 = False
        elif Px[5] > Px[4]:
            fg00 = True


    #食指
    for k in (5,6,7):
        a = Py[k]
        b = Py[k+1]
        if a > b :
            fg1 = True   
        elif a < b :
            fg1 = False


    #中指
    for k in (9,10,11):
        a = Py[k]
        b = Py[k+1]
        if a > b:
            fg2 = True
        elif a < b :
            fg2 = False


    #無名指
    for k in (13,14,15):
        a = Py[k]
        b = Py[k+1]
        if a > b:
            fg3 = True
        elif a < b :
            fg3 = False


    #小拇指 
    for k in (17,18,19):
        a = Py[k]
        b = Py[k+1]
        if a > b:
            fg4 = True
        elif a < b :
            fg4 = False


#"手指開合"辨識:方向編號1(手掌向右)
def finger_detecting_1(rl_hand, Px, Py):
    global fg1, fg2, fg3, fg4
    global fg00

    #大拇指(先進行左右手辨識，再辨識大拇指)
    if rl_hand:
        for k in (1,2,3):
            a = Py[k]
            b = Py[k+1]
            if a > b :
                fg00 = True   
            elif a < b :
                fg00 = False

    elif rl_hand == False:
        for k in (1,2,3):
            a = Py[k]
            b = Py[k+1]
            if a < b :
                fg00 = True   
            elif a > b :
                fg00 = False


    #食指
    for k in (5,6,7):
        a = Px[k]
        b = Px[k+1]
        if a > b :
            fg1 = True   
        elif a < b :
            fg1 = False


    #中指
    for k in (9,10,11):
        a = Px[k]
        b = Px[k+1]
        if a > b:
            fg2 = True
        elif a < b :
            fg2 = False


    #無名指
    for k in (13,14,15):
        a = Px[k]
        b = Px[k+1]
        if a > b:
            fg3 = True
        elif a < b :
            fg3 = False


    #小拇指 
    for k in (17,18,19):
        a = Px[k]
        b = Px[k+1]
        if a > b:
            fg4 = True
        elif a < b :
            fg4 = False


#"手指開合"辨識:方向變號2(手掌向左)
def finger_detecting_2(rl_hand, Px, Py):
    global fg1, fg2, fg3, fg4
    global fg00

    #大拇指(先進行左右手辨識，再辨識大拇指)
    if rl_hand:
        for k in (1,2,3):
            a = Py[k]
            b = Py[k+1]
            if a < b :
                fg00 = True   
            elif a > b :
                fg00= False

    elif rl_hand == False:
        for k in (1,2,3):
            a = Py[k]
            b = Py[k+1]
            if a > b :
                fg00 = True   
            elif a < b :
                fg00= False


    #食指
    for k in (5,6,7):
        a = Px[k]
        b = Px[k+1]
        if a < b :
            fg1 = True   
        elif a > b :
            fg1 = False


    #中指
    for k in (9,10,11):
        a = Px[k]
        b = Px[k+1]
        if a < b:
            fg2 = True
        elif a > b :
            fg2 = False


    #無名指
    for k in (13,14,15):
        a = Px[k]
        b = Px[k+1]
        if a < b:
            fg3 = True
        elif a > b :
            fg3 = False


    #小拇指 
    for k in (17,18,19):
        a = Px[k]
        b = Px[k+1]
        if a < b:
            fg4 = True
        elif a > b :
            fg4 = False


#"手指"辨識
def finger_recognizing(fg1, fg2, fg3, fg4, fg00):
    
    '''
    if fg00 and not (fg1 or fg2 or fg3 or fg4):
        print("  0  \n")

    if fg1 and not (fg00 or fg2 or fg3 or fg4):
        print("  1  \n")
        
    if fg2 and not (fg00 or fg1 or fg3 or fg4):
        print("  2  \n")

    if fg3 and not (fg00 or fg2 or fg1 or fg4):
        print("  3  \n")

    if fg4 and not (fg00 or fg2 or fg3 or fg1):6004
    '''


#"手勢數字"辨識
def gesture_recognizing(fg1, fg2, fg3, fg4, fg00):
    global number
    if not (fg1 or fg2 or fg3 or fg4 or fg00):
        number = 0
        print("  0  \n")
        keyboard.press('0')
        keyboard.release('0')

    if fg1 and not (fg2 or fg3 or fg4 or fg00):
        number = 1
        print("  1  \n")
        keyboard.press('1')
        keyboard.release('1')

    if fg1 and fg2 and not (fg3 or fg4 or fg00):
        number = 2
        print("  2  \n")
        keyboard.press('2')
        keyboard.release('2')

    if fg1 and fg2  and fg3 and not (fg4 or fg00):
        number = 3
        print("  3  \n")
        keyboard.press('3')
        keyboard.release('3')

    if fg1 and fg2  and fg3 and fg4 and not (fg00):
        number = 4
        print("  4  \n")
        keyboard.press('4')
        keyboard.release('4')

    if fg1 and fg2  and fg3 and fg4 and fg00:
        number = 5
        print("  5  \n")
        keyboard.press('5')
        keyboard.release('5')

    if fg4 and fg00 and not (fg1 or fg2 or fg3):
        number = 6
        print("  6  \n")
        keyboard.press('6')
        keyboard.release('6')

    if fg1 and fg00 and not (fg2 or fg3 or fg4):
        number = 7
        print("  7  \n")
        keyboard.press('7')
        keyboard.release('7')

    if fg1 and fg2 and fg00 and not (fg3 or fg4):
        number = 8
        print("  8  \n")
        keyboard.press('8')
        keyboard.release('8')

    if fg1 and fg2 and fg00 and fg3 and not (fg4):
        number = 9
        print("  9  \n")
        keyboard.press('9')
        keyboard.release('9')


#執行迴圈
while True:
    
    ret, window = cap.read() #讀取影像
    #cv2.namedWindow('window', cv2.WINDOW_KEEPRATIO)
    if ret:
        imgRGB = cv2.cvtColor(window, cv2.COLOR_BGR2RGB) #cv2轉換為mediapipe的顏色
        result = hands.process(imgRGB)
        
        #print(result.multi_hand_landmarks) #讀取手掌上21點座標

        #設定視窗大小
        imgHeight = window.shape[0]
        imgWidth = window.shape[1]


        #若偵測到手
        if result.multi_hand_landmarks: 
            #show every point(21points) on img
            for handLms in result.multi_hand_landmarks:
                    mpDraw.draw_landmarks(window, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle) #(畫在哪張圖上,傳入手掌的點,點與點連接,點的樣式,線的樣式)
                    for i, lm in enumerate(handLms.landmark): #(第幾個點,每個點的座標)
                        
                        #設定座標
                        xPos = int(lm.x * imgWidth) #寬
                        yPos = int(lm.y * imgHeight) #高
                        
                        #將各點座標輸入到array中
                        Px[i] = xPos
                        Py[i] = yPos

                        #cv2.putText(img, str(i), (xPos-30, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 10, 10), 2) #寫字(給point標號)，(圖,字串,(x,y),字形,大小,顏色,粗度)
                        '''if i == 4: #第四point
                            cv2.circle(img, (xPos, yPos), 20, (100, 100, 200), cv2.FILLED) #畫圈(圖,座標,radius,color,填滿)'''
                        
                        #print(i, xPos ,yPos ) #印出點,X座標,Y座標  *i是0到20(21個point)
                        
                    #手掌開向辨識
                    palm_direction(Px, Py)    
                    
                    #左右手判讀
                    right_or_left(Px, Py)
                    
                    #手指開合判讀
                    if palm_directions == 0:
                        finger_detecting_0(rl_hand, Px, Py)
                    elif palm_directions == 1:
                        finger_detecting_1(rl_hand, Px, Py)
                    elif palm_directions == 2:
                        finger_detecting_2(rl_hand, Px, Py)
                    
                    #手指編號輸出
                    #finger_recognizing(fg1, fg2, fg3, fg4, fg00)
                    
                    #手勢編號輸出
                    gesture_recognizing(fg1, fg2, fg3, fg4, fg00)
            
                    


        #make fps
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(window, 'fps:'+str(int(fps)), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        #顯示辨識到的數字在視窗上
        cv2.putText(window, 'number:' + str(number), (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255228), 3)
        

        cv2.imshow('window', window) 

        


    #按下Q鍵結束程式碼
    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        cap.release()
        cv2.destroyAllWindows()
        break