import numpy as np
import cv2
import os
import pygame
import threading

#thread สำหรับเปิดเสียงแจ้งเตือน
def thread_callback():
    pygame.init()
    song = pygame.mixer.Sound('sound.wav')
    clock = pygame.time.Clock()
    song.play()
    while True:
        clock.tick(60)
    pygame.quit()

#เปิดเสียงแจ้งเตือน เมื่อจำนวนคนเกิน 20    
def notice(c):
    if(c>=20):
        thr = threading.Thread(target=thread_callback)
        thr.start()


#โหลด Pretrain model
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#รับ Video จาก IP ของกล้องโทรศัพท์
cap = cv2.VideoCapture('http://192.168.43.1:8080/video')

#กำหนดความละเอียดภาพที่มาจากกล้อง
cap.set(3,1280) # set Width
cap.set(4,1024) # set Height

#loop ประมวลผลทีละเฟรม
while True:
    #รับภาพ 1 เฟรม
    ret, img = cap.read()

    #ืทำเป็นภาพเป็น gray เพื่อเข้า haar classifier
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #สร้าง array faces และเก็บพิกัดที่พบหน้า
    # scaleFactor คือความละเอียดภาพ ยิ่งค่ามากยิ่งละเอียดน้อย
    # minNeighbors จำนวนจุดบนภาพที่ต้องการตรวจจับใน 1 feature ยิ่งค่ามากความละเอียดยิ่งต่ำ ถ้าค่าน้อยเกินก็อาจจะหา feature ไม่พบ
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )

    c=0
    for (x,y,w,h) in faces:
        #วาดสี่เหลี่ยม ตามพิกัดใน array faces
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        c = c+1

    #โชว์รูปของเฟรมนั้น
    cv2.imshow('video',img)

    #เรียกการแจ้งเตือน
    notice(c)
    

    #รับค่า input จากปุ่ม esc เพื่อจบการทำงาน
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

#ปิดอุปกรณ์ Input
cap.release()

#คืนทรัพยากร
cv2.destroyAllWindows()
