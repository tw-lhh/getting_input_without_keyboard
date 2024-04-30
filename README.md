import cv2
import mediapipe as mp
import time
import random
import pyautogui

cap = cv2.VideoCapture(0) #開啟攝影機

mpHands = mp.solutions.hands # mediapipe 偵測手掌方法
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils # mediapipe 繪圖方法

#點與線的樣式
handLmsStyle =  mpDraw.DrawingSpec(color=(255,100, 50), thickness=4)
handConStyle =  mpDraw.DrawingSpec(color=(20, 255, 20), thickness=2)

pTime = 0 #先前時間
cTime = 0 #目前時間

#建立座標array
Px = [0] * 21
Py = [0] * 21

#手指判斷變數
fg1, fg2, fg3, fg4 = False, False, False, False

#開為正，反之
fg00 = False

#右手正，左手負
rl_hand = True



#左、右手辨識
def right_or_left(Px):
    global rl_hand
    
    if Px[5] > Px[17]:
        rl_hand = True#右手

    elif Px[5] < Px[17]:
        rl_hand = False#左手   




#"手指開合"辨識
def finger_detecting(rl_hand, Px, Py):
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
        #print(k, Py[k])
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

    if fg4 and not (fg00 or fg2 or fg3 or fg1):
        print("  4  \n")
    '''




#"手勢數字"辨識
def gesture_recognizing(fg1, fg2, fg3, fg4, fg00):
    
    if not (fg1 or fg2 or fg3 or fg4 or fg00):
        print("  0  \n")
        pyautogui.press('0')

    if fg1 and not (fg2 or fg3 or fg4 or fg00):
        print("  1  \n")
        pyautogui.press('1')

    if fg1 and fg2 and not (fg3 or fg4 or fg00):
        print("  2  \n")
        pyautogui.press('2')

    if fg1 and fg2  and fg3 and not (fg4 or fg00):
        print("  3  \n")
        pyautogui.press('3')

    if fg1 and fg2  and fg3 and fg4 and not (fg00):
        print("  4  \n")
        pyautogui.press('4')

    if fg1 and fg2  and fg3 and fg4 and fg00:
        print("  5  \n")
        pyautogui.press('5')

    if fg4 and fg00 and not (fg1 or fg2 or fg3):
        print("  6  \n")
        pyautogui.press('6')

    if fg1 and fg00 and not (fg2 or fg3 or fg4):
        print("  7  \n")
        pyautogui.press('7')

    if fg1 and fg2 and fg00 and not (fg3 or fg4):
        print("  8  \n")
        pyautogui.press('8')

    if fg1 and fg2 and fg00 and fg3 and not (fg4):
        print("  9  \n")
        pyautogui.press('9')

    




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
                        
                        

                    #左右手判讀
                    right_or_left(Px)

                    #手指開合判讀
                    finger_detecting(rl_hand, Px, Py)

                    #手指編號輸出
                    #finger_recognizing(fg1, fg2, fg3, fg4, fg00)
                    
                    #手勢編號輸出
                    gesture_recognizing(fg1, fg2, fg3, fg4, fg00)
                    


        #make fps
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(window, 'fps:'+str(int(fps)), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

        
        cv2.imshow('window', window) 

    #按下Q鍵結束程式碼
    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        cap.release()
        cv2.destroyAllWindows()
        break
