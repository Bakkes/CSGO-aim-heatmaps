import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from scipy import stats
      
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    xmin = -75
    xmax = 75
    ymin = -75
    ymax = 75
   

    def __init__(self, server_address, RequestHandlerClass, dunno):
        print "Received connection!"
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        plt.ion()
        plt.show()
        
    def handle(self):
        while True:
            print "Waiting for data"
            data = self.request.recv(1024).strip().split("\t")
            
            m0,m1,m2 = data[0], data[1], data[2]
            print "Got data: %f, %f, %f" % (m0,m1,m2)

            if m1.size<2:
                    return 0    
    
            X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
            positions = np.vstack([X.ravel(), Y.ravel()])
            values = np.vstack([m1,m2])
            kernel = stats.gaussian_kde(values)
            Z = np.reshape(kernel.evaluate(positions).T, X.shape)
        
            mean=[np.mean(m1),np.mean(m2)]
            mean=float("{0:.2f}".format(np.linalg.norm(mean)))
            stdX=float("{0:.2f}".format(np.std(m1)))
            stdY=float("{0:.2f}".format(np.std(m2)))
            ax.set_title('Average Offset         : '+str(mean)+'\n'+'Standard Deviation X : '+str(stdX)+'\n'+'Standard Deviation Y : '+str(stdY))
            ax.imshow(np.rot90(Z), cmap=plt.cm.jet,
                      extent=[xmin, xmax, ymin, ymax])
            ax.plot(m1,m2, 'o', markersize=3.5, linewidth='3', markerfacecolor='r',markeredgecolor = 'black')
            ax.set_xlim([xmin, xmax])
            ax.set_ylim([ymin, ymax])
    
            plt.draw()
            ax.cla()
        
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 1337
    print "Initializing socket"
    # Create the server, binding to localhost on port 1337
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    print "Serving..."
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
