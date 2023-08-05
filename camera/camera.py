import http.server as http
from time import sleep
import cv2

from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect

SERVER_URL = "ws://localhost:8765"

ESC_KEY = 27
WINDOW = "Transmitter"

def log(msg):
    print("[LOG]: " + msg)

def camera():
    
    # Connect to camera and open debug window
    running = True
    websocket = None
    cam = cv2.VideoCapture(0)
    cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)

    while running:
        # Keep trying to connect to server
        while websocket is None:
            try:
                websocket = connect(SERVER_URL)
            except:
                log("Couldn't connect to server!")
                sleep(1)

        # Keep trying to send frames
        while True:
            try: 
                valid, frame = cam.read()
                cv2.imshow(WINDOW, frame)
                img_str = cv2.imencode('.jpg', frame)[1].tobytes()
                
                websocket.send(img_str)

            except ConnectionClosed:
                websocket = None
                log("The server closed the connection!")
                break
            except RuntimeError:
                log("Connection was busy")
                sleep(1)
            except TypeError:
                log("Type Error")
            except:
                log("Unknown error!")
                sleep(1)

            # Must have key between rendering frame
            if cv2.waitKey(1) == ESC_KEY: 
                running = False 
                break
    
    websocket.close()
    cv2.destroyAllWindows()

def main():
    camera()

if __name__ == '__main__':
    main()