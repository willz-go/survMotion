import os 
from dotenv import load_dotenv
import cv2





if __name__ == "__main__":
    load_dotenv()
    RTSP_URL=   os.environ.get("RTSP_URL")
    print(f'URL  = {RTSP_URL}')

 


    #RTSP_URL = 'rtsp://user:pass@192.168.0.189:554/h264Preview_01_main'

    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print('Cannot open RTSP stream')
        exit(-1)

    while True:
        _, frame = cap.read()
        downscale_percent = 70
        width = frame.shape[1] 
        height = frame.shape[0]
        dim = (int(width*(downscale_percent/100)), int(height*(downscale_percent/100)))

        resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        print('Resized dims are :', resized_frame.shape)
        
        cv2.imshow('RTSP stream', resized_frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()