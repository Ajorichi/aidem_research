import cv2
from ultralytics import YOLO
import data_process as dt_proc

model_path='yolov5s.pt'
database='research'
server={"user":"artriguer100304",
        "password":"100304Jcd&Art",
        "client_name":"mosquito_systems"}
# Load the YOLOv8 model
model = YOLO(model_path)

# Open the video file
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:

        # Run YOLOv8 inference on the frame
        results = model(frame, imgsz=320)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        dt_proc.upload(results=results, srv=server, database = database)

        # Display the annotated frame
        cv2.imshow("AIDeM Project", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()