pyfaucet-networking
===================

Python library for working with the Faucet Networking Extension for Game Maker.

Has preliminary bindings for Faucet Networking buffer functions.

Quick Tutorial
==============
While there is a rather feature-full server example, it may be too much for quick learning, so here are the steps to get pyfaucet up and running:

    import pyfaucet, socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM is a UDP datagram.
    sock.bind( ("", 12345) ) # This binds the socket to localhost on port 12345
    buffer = pyfaucet.buffer() # Create our very own pyfaucet buffer!
    buffer.write_ubyte(255) # Writes a unsigned byte, 255 (Which is th maximum allowed by ubyte)
    buffer.write_bstring("Hello World!") # bstring is a helper buffer write
    sock.sendto( buffer, ("other.ip.address", 54321) ) # Sends this UDP packet to the IP specified on port 54321

The above demonstrates a very easy way for pyfaucet to send a datagram to a GM client.

Helper Functions
================
Due to the nature of datagrams and the way Faucet Networking handles strings, there is no way to know ahead of time how long a string is (Faucet Networking, unlike 39dll, does not use null byte delimiters). To make it easier to send and receive strings, there are 3 helper functions to write strings:

    buffer.write_bstring("Writes a string that can be up to 255 (1 byte) characters long")
    buffer.write_sstring("Writes a string that can be up to 65536 (2 bytes) characters long")
    buffer.write_istring("Writes a string that can be up to 4294967296 (4 bytes) characters long")

    # write_string() is for completeness' sake. It is very doubtful any packet can be that large and still be successfully sent

They are equivalent to:

    # buffer.write_bstring(string) is equivalent to:
    buffer.write_ubyte(len(string))
    buffer.write_string(string)

    # buffer.write_sstring(string) is equivalent to:
    buffer.write_ushort(len(string))
    buffer.write_string(string)

    # buffer.write_istring(string) is equivalent to:
    buffer.write_uint(len(string))
    buffer.write_string(string)
