import cv2 , socketserver , numpy
import argparse

parser = argparse.ArgumentParser(description='Start a TCP server.')
parser.add_argument('--port', default=7110, type=int,
                    help='The port on which to listen.')
parser.add_argument('--length', default=100000, type=int,
                    help='The size of the data to send over the connection.')
args = parser.parse_args()

#DATA = "F" * args.length
capture = cv2.VideoCapture("/home/seed/Desktop/test2.mp4")
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
_,img = capture.read()
DATA = img.tostring()
DATA2 = DATA.hex()
#DATA3 = bytes.fromhex(DATA2).decode('utf-8')
#print(len(DATA3))
DATA = str.encode(DATA2)
print(len(DATA))

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print ("Connection opened from %s:%d. Sending data." % self.client_address)
        self.request.sendall(DATA)
        print ("Data sent. Closing connection to %s:%d." % self.client_address)

if __name__ == "__main__":
    server = socketserver.TCPServer(('0.0.0.0', args.port), TCPHandler)
    try:
        print ("Starting TCP server on port", args.port, "...")
        server.serve_forever()
    except KeyboardInterrupt as e: server.shutdown()
