import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "10.0.2.101"   # socket.gethostname() # Get local machine name, will not work remotely
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   msg = 'Thank you for connecting'
   c.send(msg.encode())
   c.close()                # Close the connection

