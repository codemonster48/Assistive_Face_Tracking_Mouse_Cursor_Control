import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec =  mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)
diff_mouth_length = 0
diff_mouth_width = 0
diff_eyebrows = 0
diff_nose_up = 0
diff_nose_down = 0
diff_nose_left = 0
diff_nose_right = 0
diff_eye = 0 # check if the face is straight
detected_mouth = 0
detected_eyebrows = 0
detected_nose_up = 0
detected_nose_down = 0
detected_nose_left = 0
detected_nose_right = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                #print(id,x,y)
                #print('size:' + str(len(faceLms.landmark)))
            #diff_mouth = float(faceLms.landmark[16].y) - float(faceLms.landmark[13].y)
            diff_mouth_length = float(faceLms.landmark[308].x) - float(faceLms.landmark[61].x)
            diff_eyebrows = float(faceLms.landmark[257].y) - float(faceLms.landmark[443].y)
            diff_mouth_width = float(faceLms.landmark[16].y) - float(faceLms.landmark[13].y)
            #correct cordinates eye
            diff_nose_up = float(faceLms.landmark[1].y) - float(faceLms.landmark[4].y)
            diff_eye = float(faceLms.landmark[145].y) - float(faceLms.landmark[159].y)
    #print(diff_eyebrows)
    
    if(diff_mouth_length > 0.17 and diff_mouth_width > 0.05):
        print('mouth detected')
        detected_mouth = 1
    
    if(diff_eyebrows > 0.018 and diff_eye > 0.030):
        print('eyebrow detected')
        detected_eyebrows = 1
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,70), cv2.FONT_HERSHEY_DUPLEX, 3, (0,255,0),3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if(key==27):
        break
