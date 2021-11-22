import numpy as np
import cv2
import os
import pygame
import threading
import geocoder
from geopy.geocoders import Nominatim
import datetime
import pyodbc
import requests
import time

#ดึงข้อมูลพิกัดและเวลา ส่งไปเก็บบน Database
def thread_call_API(c):
    date_time = datetime.datetime.now()

    #get geolocation from Public IP
    g = geocoder.ip('me')
    geolocator = Nominatim(user_agent="geoapiExercises")
    lat = g.latlng[0]
    lng = g.latlng[1]

    #convert to address
    location = geolocator.reverse(str(lat)+","+str(lng))
    address = location.raw['address']
  
    # traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    code = address.get('country_code')
    zipcode = address.get('postcode')

 
    #wrtie location to API
    url = 'http://127.0.0.1:5000'+"/add"+"?population="+str(c)+'&city='+str(city)+'&state='+str(state)+'&postcode='+str(zipcode)+'&country='+country+'&time='+str(date_time)
    res = requests.get(url) 
    print(res.text)
    
    #kill thread
    if True:
        pass

#thread สำหรับเปิดเสียงแจ้งเตือน
def thread_callback():
    pygame.init()
    song = pygame.mixer.Sound('sound.wav')
    clock = pygame.time.Clock()
    song.play()
    #terminate thread
    if True:
        pass

#เปิดเสียงแจ้งเตือน+เขียนdatabase เมื่อจำนวนคนเกินที่กำหนด   
def notice_sound(c):
    if(c>=1): 
        #Ex.กำหนด 3 คน
        thr1 = threading.Thread(target=thread_callback)
        thr1.start()


def send_data(c):
    if(c>=1): #กำหนด 3 คน
        #ส่งข้อมูลสถานที่และจำนวนคนขึ้น Database   
        thr2 = threading.Thread(target=thread_call_API(c))
        thr2.start()
        print("thread2 success")
        


#โหลด Pretrain model
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#option1 รับ Video จาก IP ของกล้องโทรศัพท์
#option2 รับ video จาก devide บน host server
# EX. 
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('http://192.168.43.1:8080/video')

#กำหนดความละเอียดภาพที่มาจากกล้อง
cap.set(3,1280) # set Width
cap.set(4,1024) # set Height

#ตั้งเวลาแจ้งเตือน ทุก 5 วินาที
start_time = time.time()
seconds = 5
seconds2 = 5
fixedTIME=0

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
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
        c = c+1

    #โชว์รูปของเฟรมนั้น
    cv2.imshow('video',img)

    #เรียกการแจ้งเตือน
    current_time = time.time()
    elapsed_time = current_time - start_time
    if int(elapsed_time)%seconds==0:
        #print(fixedTIME)
        if(fixedTIME<int(elapsed_time)):
            fixedTIME = int(elapsed_time)
            notice_sound(c)
            send_data(c)
        
    

    #รับค่า input จากปุ่ม esc เพื่อจบการทำงาน
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

#ปิดอุปกรณ์ Input
cap.release()

#คืนทรัพยากร
cv2.destroyAllWindows()
