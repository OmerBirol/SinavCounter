import cv2
import numpy as np
import mediapipe as mp
import math
def findAngle(img,p1,p2,p3,lmList,draw=True):
    x1,y1=lmList[p1][1:]#p1 noktası bize 3 nokta verir biz bunların zxyden 1den başlayarak 2ye kadar yani x ve yyi alıyourz
    x2,y2=lmList[p2][1:]
    x3,y3=lmList[p3][1:]

    #açı hesabı
    angle=math.degrees(math.atan2(y3 - y2 , x3 - x2)-(math.atan2(y1 - y2 , x1 - x2)))
    
    if angle < 0 : angle+=360
    
    if draw:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),3)                      
        cv2.line(img,(x3,y3),(x2,y2),(0,255,255),3)
        
        cv2.circle(img,(x1,y1),10,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x3,y3),10,(0,255,255),cv2.FILLED)
        
        cv2.circle(img,(x1,y1),15,(0,255,255))
        cv2.circle(img,(x2,y2),15,(0,255,255))
        cv2.circle(img,(x3,y3),15,(0,255,255))            
        
        cv2.putText(img,str(int(angle)),(x2-40,y2+40),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
    return angle

cap=cv2.VideoCapture(0)
mpPose=mp.solutions.pose

pose=mpPose.Pose()

mpDraw=mp.solutions.drawing_utils
dir=0#hareketi bitirp bitirmediğini kontrol edicez
count=0#şınav sayısını sayıcaz
while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)
    
    lmList=[]
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,_=img.shape
            cx,cy=int(lm.x*w),int(lm.y*h)
            lmList.append([id,cx,cy])
        #print(lmList)
        
        if len(lmList)!=0:
            
            angle=findAngle(img,11,13,15,lmList)
            per=np.interp(angle,(185,245),(0,100))
            print(angle)
            
            if per==100:#245 derece gibi
                if dir==0:
                    count+=0.5
                    dir=1
            if per==0:#185 derece gibi
                if dir==1:
                    count+=0.5
                    dir=0
            print(count)
            
            cv2.putText(img,str(int(count)),(45,125),cv2.FONT_HERSHEY_PLAIN,10,(0,255,0),10)
                
                
        
        
    
    
    
    cv2.imshow("image",img)
    cv2.waitKey(10)