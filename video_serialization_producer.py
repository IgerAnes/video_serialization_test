import socket
import cv2
import pickle
import time

# this is server ip and port
HOST = '192.168.50.248' 
PORT = 6000
FORMAT = 'utf-8' 
HEADERSIZE = 10

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.connect((HOST, PORT))
cam = cv2.VideoCapture(0)
if cam.isOpened():
    print("[Camera] Succeed to get webcam data.")

counter = 0

while cam.isOpened():
    ret, frame = cam.read()
    
    # # send raw frame
    # # transfer frame data to byte
    # data = pickle.dumps(frame)
    # # left-align and add space to remain char space, that header will match the haedersize
    # header = bytes(f"{len(data):<{HEADERSIZE}}", FORMAT)
    # # send data will consist of header and data 
    # send_data  = header + data
    
    
    # send frame with counter
    counter += 1
    current_time = time.time()
    cv2.putText(frame, f"Counter: {counter}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 100, 50), 1 , cv2.LINE_AA)
        
    # transfer frame data to byte
    data = pickle.dumps(frame)
    # left-align and add space to remain char space, that header will match the haedersize
    header = bytes(f"{len(data):<{HEADERSIZE}}", FORMAT)
    # send data will consist of header and data 
    send_data  = header + data
    
    socketClient.send(send_data)
    print(f"[CLIENT] finish sending {counter} frame data")
    
    # show image
    cv2.imshow('Webcam', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()