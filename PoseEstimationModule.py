import math

import cv2
import mediapipe as mp
import time
import numpy as np


class Detector:
    def __init__(self,mode=False,smooth=True,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose=mp.solutions.pose
        self.mpDraw=mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=1,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.results=None
    def findpos(self,img,draw=True):
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.results=self.pose.process(imgRGB)
            if self.results.pose_landmarks and draw:
                    self.mpDraw.draw_landmarks(img,
                                       self.results.pose_landmarks,
                                       self.mpPose.POSE_CONNECTIONS
                    )
            return img


    def getposition(self,img,draw=False):
            self.lmlist= []
            if self.results.pose_landmarks:
                h, w, c = img.shape
                for id,lm in enumerate(self.results.pose_landmarks.landmark):
                        cx,cy=int(lm.x*w),int(lm.y*h)
                        self.lmlist.append([id,cx,cy])
                        if draw:
                            cv2.circle(img,(cx,cy),3,(0,255,255),4)
            return self.lmlist
    def findangle(self,img,p1,p2,p3,draw=True):
            x1,y1=self.lmlist[p1][1:]
            x2,y2=self.lmlist[p2][1:]
            x3,y3=self.lmlist[p3][1:]



            #calculate the Angle

            angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))

            if angle<0:
                angle=360+angle
            if draw:
                cv2.line(img,(x1,y1),(x2,y2),(255,255,255),4)
                cv2.line(img,(x2,y2),(x3,y3),(255,255,255),4)
                cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
                cv2.circle(img,(x1,y1),14,(255,0,255),4)
                cv2.circle(img,(x2,y2),8,(255,0,255),cv2.FILLED)
                cv2.circle(img,(x2,y2),14,(255,0,255),4)
                cv2.circle(img,(x3,y3),8,(255,0,255),cv2.FILLED)
                cv2.circle(img,(x3,y3),14,(255,0,255),4)
            return angle
if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    ptime = 0
    detector =Detector()
    while True:
        success, img = cap.read()
        img= detector.findpos(img)
        lmlist = detector.getposition(img,draw=False)
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime

        cv2.putText(img,str(int(fps)),(100,200),3,3,(255,0,255),2)

        cv2.imshow("img",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
