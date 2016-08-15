import sys
import chilkat

socket = chilkat.CkSocket()

success = socket.UnlockComponent("Anything for 30-day trial")
if (success != True):
    print(socket.lastErrorText())
    sys.exit()

#  To use a SOCKS4 or SOCKS5 proxy, simply set the following
#  properties prior to calling Connect.  The connection may be SSL/TLS or
#  non-secure - both will work with a SOCKS proxy.
#  The SOCKS hostname may be a domain name or
#  IP address:
socket.put_SocksHostname("www.mysocksproxyserver.com")
socket.put_SocksPort(1080)
socket.put_SocksUsername("myProxyLogin")
socket.put_SocksPassword("myProxyPassword")
#  Set the SOCKS version to 4 or 5 based on the version
#  of the SOCKS proxy server:
socket.put_SocksVersion(5)
#  Note: SOCKS4 servers only support usernames without passwords.
#  SOCKS5 servers support full login/password authentication.

#  Connect to port 5555 of 192.168.1.108.
#  hostname may be a domain name or IP address.
hostname = "192.168.1.108"
ssl = False
maxWaitMillisec = 20000
success = socket.Connect(hostname,5555,ssl,maxWaitMillisec)
if (success != True):
    print(socket.lastErrorText())
    sys.exit()

#  Set maximum timeouts for reading an writing (in millisec)
socket.put_MaxReadIdleMs(10000)
socket.put_MaxSendIdleMs(10000)

#  The server (in this example) is going to send a "Hello World!"
#  message.  Read it:

receivedMsg = socket.receiveString()
if (receivedMsg == None ):
    print(socket.lastErrorText())
    sys.exit()

#  Close the connection with the server
#  Wait a max of 20 seconds (20000 millsec)
socket.Close(20000)

print(receivedMsg)