import os 
from dotenv import load_dotenv
import cv2
from numpy import integer

GRID_SIZE = 100
GRID_COLOR = (0, 0, 0)

def calculate_grid_params(grid_size: int, img: cv2.Mat):
    width = img.shape[1]
    height = img.shape[0]

    if grid_size > width or grid_size > height:
         return [-1, -1]

    num_cols = int(width/grid_size)
    num_rows = int(height/grid_size)
    return [num_rows, num_cols]

def handle_mouseclicks(event, x, y, flags, params):
    print(f'Mouse event is {event} x = {x}; y = {y}; flasg are {flags} and params are {params}')
    pass

def drawGrid(grid_size: int, img: cv2.Mat)->None:
    grid_size = int(grid_size)
    if not isinstance(grid_size, int):
                grid_size = 8
 
    
    [num_rows, num_cols] = calculate_grid_params(GRID_SIZE, img) 
    print(num_rows)
    print(num_cols)
    height = img.shape[0]
    width = img.shape[1]
    if num_cols == -1: 
         return img

    for col in range(1, num_cols +1):
        for column_pixel in range(0, height):
            #rgb = img[column_pixel][grid_size-1]
            new_rgb = (0, 0, 0)
            img[column_pixel][col*grid_size] = new_rgb

    for row in range(1, num_rows +1):
        for row_pixel in range(0, width-1):
            #rgb = img[column_pixel][grid_size-1]
            new_rgb = GRID_COLOR
            img[row*grid_size][row_pixel] = new_rgb



    return img

    


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

    cv2.namedWindow("RTSP stream")
    cv2.setMouseCallback("RTSP stream" , handle_mouseclicks)

    while True:
        
        _, frame = cap.read()
        downscale_percent = 70
        width = frame.shape[1] 
        height = frame.shape[0]
        dim = (int(width*(downscale_percent/100)), int(height*(downscale_percent/100)))

        resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        print('Resized dims are :', resized_frame.shape)

        grid_frame = drawGrid(GRID_SIZE, resized_frame)
        
        cv2.imshow('RTSP stream', grid_frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()