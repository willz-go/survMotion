import os 
from dotenv import load_dotenv
import cv2
import numpy as np
from numpy import integer

GRID_SIZE = 100
GRID_COLOR = (0, 0, 0)

class CamMonitor: 
     grid_size: int  = GRID_SIZE
     grid_color: (int, int, int) = GRID_COLOR
     img_width: int = 0
     img_height: int = 0
     current_grid_m: int = -1
     current_grid_n: int = -1
     threshold: int = 50 #this translates into the diference level between frames or images

     def __init__(self) -> None:
            self.grid_color = GRID_COLOR
            self.grid_size = GRID_SIZE
            return
     
     def grid_diff(self, grid_m: int, grid_n: int, frame: cv2.Mat, old_frame: cv2.Mat)-> [cv2.Mat, int]:
         x_pos = grid_m*GRID_SIZE
         y_pos = grid_n*GRID_SIZE #both gives the actual pixel position to start comparing
         x_pos_max = x_pos + GRID_SIZE if x_pos + GRID_SIZE <= frame.shape[1] else frame.shape[1]  #
         y_pos_max = y_pos + GRID_SIZE if y_pos + GRID_SIZE <= frame.shape[0] else frame.shape[0]  # both will ensure x_max and y_max are withing image boundaries
         print(f'{x_pos} {x_pos_max} - {y_pos} {y_pos_max}')

        #  grid1 = frame[x_pos:x_pos_max][y_pos:y_pos_max]
         grid1 = frame[y_pos:y_pos_max, x_pos:x_pos_max]
         grid2 = old_frame[y_pos:y_pos_max, x_pos:x_pos_max]

         result = cv2.absdiff(grid1, grid2)
         print(result.shape)

         sum = np.sum(result) / (3*(y_pos_max-y_pos)*(x_pos_max - x_pos))
         

         print(f'Grid1 width = {grid1.shape[1]} heihgt  = {grid1.shape[0]}')

         #gotta remove result as a returned value, because it won't be used later. Must return only SUM. Also update return type in function declaration after said alterations
         return [result, sum]
         
     
     def get_grid_position(self, x: int, y: int, width: int, height: int)->[int, int]:
         pos_x = int (x/self.grid_size)
         pos_y = int (y/self.grid_size)
         return [pos_x, pos_y]
     
     def paint_grid_area(self, grid_m: int, grid_n: int, img: cv2.Mat, color: (int, int, int)):
         print(f'grid m = {grid_m} grid n = {grid_n} ')
         cv2.rectangle(img, (grid_m*self.grid_size, grid_n*self.grid_size), (grid_m*self.grid_size + self.grid_size, grid_n*self.grid_size + self.grid_size), color, 2)
         return img

     
     def calculate_grid_params(self, grid_size: int, img: cv2.Mat):
        width = img.shape[1]
        height = img.shape[0]
        if grid_size > width or grid_size > height:
            return [-1, -1]

        num_cols = int(width/grid_size)
        num_rows = int(height/grid_size)
        return [num_rows, num_cols]

     def handle_mouseclicks(self, event, x, y, flags, params):
        print(f'Mouse event is {event} x = {x}; y = {y}; flasg are {flags} and params are {params}')
        [grid_x, grid_y] = self.get_grid_position(x, y, self.img_width, self.img_height)
        self.current_grid_m = grid_x
        self.current_grid_n = grid_y
        print(f'Grid M is {grid_x} and Grid N is  {grid_y}')
        pass

    
     def drawGrid(self, grid_size: int, img: cv2.Mat)->None:
        grid_size = int(grid_size)
        if not isinstance(grid_size, int):
                    grid_size = 8
    
        
        [num_rows, num_cols] = self.calculate_grid_params(GRID_SIZE, img) 
        print(num_rows)
        print(num_cols)
        height = img.shape[0]
        width = img.shape[1]
        self.img_height = height
        self.img_width = width
        if num_cols == -1: 
            return img

        for col in range(1, num_cols+1):
            print(col)
            for column_pixel in range(0, height):
                
                new_rgb = (0, 0, 0)
                img[column_pixel][col*grid_size] = new_rgb

        for row in range(1, num_rows +1):
            for row_pixel in range(0, width-1):
               
                new_rgb = GRID_COLOR
                img[row*grid_size][row_pixel] = new_rgb
        return img

    
     def capture_rtsp(self):
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
        cv2.setMouseCallback("RTSP stream" , self.handle_mouseclicks)

        while True:
            
            _, frame = cap.read()
            downscale_percent = 70
            width = frame.shape[1] 
            height = frame.shape[0]
            dim = (int(width*(downscale_percent/100)), int(height*(downscale_percent/100)))

            resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

            print('Resized dims are :', resized_frame.shape)

            grid_frame = self.drawGrid(GRID_SIZE, resized_frame)
            
            cv2.imshow('RTSP stream', grid_frame)
        

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        return
     
     def capture_img_only(self):
        load_dotenv()
        IMG_URL =  "./image/example_img.jpg"
        IMG_URL2 =  "./image/example_img2.jpg"
        #print(f'URL  = {RTSP_URL}')
       
        

        cv2.namedWindow("IMG show only")
        cv2.setMouseCallback("IMG show only" , self.handle_mouseclicks)

        while True:
            
            img = cv2.imread(IMG_URL)
            img2 = cv2.imread(IMG_URL2)
            downscale_percent = 90
            width = img.shape[1] 
            height = img.shape[0]
            dim = (int(width*(downscale_percent/100)), int(height*(downscale_percent/100)))

            resized_frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            resized_frame2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)

            print('Resized dims are :', resized_frame.shape)

            grid_frame = self.drawGrid(GRID_SIZE, resized_frame)
            grid_frame2 = self.drawGrid(GRID_SIZE, resized_frame2)

            if (self.current_grid_m >= 0 and self.current_grid_n >= 0):
                grid_frame = self.paint_grid_area(self.current_grid_m, self.current_grid_n, grid_frame, (0, 255, 0))
                grid_frame2 = self.paint_grid_area(self.current_grid_m, self.current_grid_n, grid_frame2, (0, 255, 0))
                [grid1, diff] = self.grid_diff(self.current_grid_m, self.current_grid_n, grid_frame, grid_frame2)
                print(f'The diff is {diff}')
                cv2.imshow('IMG 2', grid1)
                
            
            cv2.imshow('IMG show only', grid_frame)
            cv2.imshow('IMG2 show only', grid_frame2)

            

            if cv2.waitKey(500) == 27:
                break

        
        cv2.destroyAllWindows()
        return


            


if __name__ == "__main__":
    monitor = CamMonitor()
    print('grid size')
    print(monitor.grid_size)
    monitor.capture_img_only()

    pass