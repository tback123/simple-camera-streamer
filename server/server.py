import asyncio
import cv2
from websockets.server import serve
import numpy as np

BINDING_IP = "localhost"
BINDING_PORT = 8765

ESC_KEY = 27
WINDOW = "Server"

async def get_feed(websocket):

    cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)

    async for frame in websocket:
        
        nparr = np.frombuffer(frame, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        cv2.imshow(WINDOW, img)

        if cv2.waitKey(1) == ESC_KEY: 
            break;
    
    cv2.destroyAllWindows()

async def main():
    async with serve(get_feed, BINDING_IP, BINDING_PORT):
        await asyncio.Future() 

if __name__ == '__main__':
    asyncio.run(main())