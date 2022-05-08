import pickle
import socket
import cv2

# setup server parameter
HOST = "192.168.50.248"
PORT = 6000
HEADERSIZE = 10
FORMAT = 'utf-8'

# setup socket server with parameter
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((HOST, PORT))
socketServer.listen()
print(f"[SERVER] Server Address: {HOST}:{PORT}")
print("[SERVER] Start to listen to client connection ...")

# accept the connectio form outside
print("Start to accept connection")
conn, addr = socketServer.accept() # this cmd. will wait until receive next connection
print(f"[SERVER] Receive data from {addr}")

while True:
    data = b""
    
    data_len = conn.recv(HEADERSIZE).decode(FORMAT)
    print(f"[SERVER] Receive data length")
    
    if data_len != None and data_len != "":
        data_len = int(data_len)
        remain_len = data_len
        print(f"[{addr}] data length: {data_len}")
        # check remain data length, and avoid to get data from the other frame
        while len(data) < data_len:
            if remain_len >= 4096:
                data += conn.recv(4096)
                remain_len -= 4096
            else:
                data += conn.recv(remain_len)
            
        # convert byte data to python object by pickle
        origin_data = pickle.loads(data[:data_len])
        cv2.imshow("Receive", origin_data)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()