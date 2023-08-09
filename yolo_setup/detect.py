import argparse
import sys
import time

import cv2
from ultralytics import YOLO

# import data_process as dt_proc
from database.post import post_pipe as db
import datetime
from dateutil import parser
import speedtest
import threading

import RPi.GPIO as GPIO
from time import sleep
import torch

indicator = (31,33,35)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(indicator, GPIO.OUT)

states = [[0,0,0],
          [1,0,0],
          [0,1,0],
          [0,0,1]]
def bytes_to_mb(bytes):
  KB = 1024 # One Kilobyte is 1024 bytes
  MB = KB * 1024 # One MB is 1024 KB
  return int(bytes/MB)

def speedTest(min_speed):
      
  print("Checking speed")
  
  speed_test = speedtest.Speedtest(secure=True)
  ups = bytes_to_mb(speed_test.upload())
  if ups >= min_speed:
    for i in range (3):
       GPIO.output(indicator[i],states[2][i])
    sleep(3)
    print('Speed: ', ups)
    print('Initiating...')
    for i in range (3):
       GPIO.output(indicator[i],states[0][i])
    return 1
  else:
    
    for i in range (3):
        GPIO.output(indicator[i],states[3][i])
    print('Speed is, ',ups,'MBps, which is lower than ',min_speed,'\nRechecking...')
    ups = bytes_to_mb(speed_test.upload())
    for i in range (3):
       GPIO.output(indicator[i],states[0][i])
    sleep(1)
    return 0
        
def dataProc(det, db_cred, upd, bypass):
    z=[det[0].names[box.cls[0].item()] for box in det[0].boxes]
    if len(z) != 0 or bypass == 1:
        current_date = parser.parse(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        data = {'date':current_date,'aedes': z.count('aedes'),'non_aedes':z.count('non_aedes')}
        print(data)
        #dataSize= sys.getsizeof(data)
        if upd == 1:
            #print(f"Uploading {dataSize} Bytes of data to MongoDB")
            db(data = data, srv = db_cred)
        
def run(model_path: str, 
        camera_id: int, 
        user: str,
        password: str,
        clnt_name: str,
        database: str,
        show: int,
        min_speed: int,
        upd: int,
        bypass: int)-> None:
    
    db_cred = {"user": user,
               "password":password,
               "database": database,
               "clnt": clnt_name}
    
    print(model_path)
    print('Database info: ', db_cred['user'],'\n',db_cred['password'],'\n', db_cred['clnt'],'\n',db_cred['database'])
    print('Display window enabled: ', show)
    print('Upload file: ', upd)
    if upd == 1:
        upd = speedTest(min_speed)
    
    # Load the YOLOv8 model
    model = YOLO(model_path, task='detect')

    # Open the video file
    cap = cv2.VideoCapture(camera_id)

    counter, fps = 0, 0
    start_time = time.time()

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
                
            counter += 1

            # Run YOLOv8 inference on the frame
            results = model(frame, imgsz=224, half=True, verbose=False, device='cpu', vid_stride=True, conf=0.5)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            
            if counter % fps_avg_frame_count == 0:
                    end_time = time.time()
                    fps = fps_avg_frame_count / (end_time - start_time)
                    start_time = time.time()

            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)
            text_location = (left_margin, row_size)
            cv2.putText(annotated_frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

            # Display the annotated frame
            if show == 1:
                cv2.imshow("AIDeM Project", annotated_frame)
                print(fps)
                
            updSTime = time.time()
            dataProc(det=results, db_cred=db_cred, upd=upd, bypass=bypass)
            updETime = time.time()
            
            updTime = updETime - updSTime
            
            print(f"Upload time is {updTime}")
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    
def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      type=str,
      default='/home/aidem/yolo_setup/models/aidem_320/best.onnx')
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--user',
      help='database username',
      required=True,
      type=str)
  parser.add_argument(
      '--password',
      help='Database password',
      required=True,
      type=str)
  parser.add_argument(
      '--database',
      help='Enter database name',
      required=True,
      type=str)
  parser.add_argument(
      '--clnt',
      help='Enter collection name',
      required=True,
      type=str)
  parser.add_argument(
      '--show',
      help='Enable showing of window',
      required=False,
      type=int,
      default=1)
  parser.add_argument(
      '--min_speed',
      help='Enable showing of window',
      required=False,
      type=int,
      default=0)
  parser.add_argument(
      '--upd',
      help='Enable uploading to database',
      required=False,
      type=int,
      default=1)
  parser.add_argument(
      '--bypass',
      help='Bypass uploading to database',
      required=False,
      type=int,
      default=0)
  args = parser.parse_args()

  run(model_path = str(args.model),
      camera_id=int(args.cameraId),
      user=str(args.user),
      password=str(args.password),
      database=str(args.database),
      clnt_name=str(args.clnt),
      show=int(args.show),
      min_speed=int(args.min_speed),
      upd=int(args.upd),
      bypass=int(args.bypass))
  
if __name__ == '__main__':
  main()
