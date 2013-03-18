import struct

class Buffer(bytearray):
    index = 0

    def __init__(self, message=""):
        self[:] = bytearray(message)

    def get_readpos(self):
        return self.index

    def set_readpos(self, i):
        self.index = i

    def clear(self):
        self.index = 0
        self[:] = ""
        
    def load(self, message=""):
        self[:] = bytearray(message)
        self.index = 0

    def read_ubyte(self):
        ubyte = self[self.index:self.index+1]
        self.index += 1
        return struct.unpack("!B", str(ubyte))[0]

    def read_byte(self):
        byte = self[self.index:self.index+1]
        self.index += 1
        return struct.unpack("!b", str(byte))[0]

    def read_ushort(self):
        ushort = self[self.index:self.index+2]
        self.index += 2
        return struct.unpack("!H", str(ushort))[0]

    def read_short(self):
        short = self[self.index:self.index+2]
        self.index += 2
        return struct.unpack("!h", str(short))[0]

    def read_uint(self):
        uint = self[self.index:self.index+4]
        self.index += 4
        return struct.unpack("!I", str(uint))[0]

    def read_int(self):
        integer = self[self.index:self.index+4]
        self.index += 4
        return struct.unpack("!i", str(integer))[0]

    def read_float(self):
        fl = self[self.index:self.index+4]
        self.index += 4
        return struct.unpack("!f", str(fl))[0]

    def read_double(self):
        db = self[self.index:self.index+8]
        self.index += 8
        return struct.unpack("!d", str(db))[0]

    def read_string(self, length):
        string = self[self.index:self.index+length]
        self.index += length
        return struct.unpack("!"+str(length)+"s", str(string))[0]

    def read_bstring(self):
        length = struct.unpack("!B",str(self[self.index:self.index+1]))[0]
        self.index += 1
        string = self[self.index:self.index+length]
        self.index += length
        return struct.unpack("!"+str(length)+"s", str(string))[0]

    def read_sstring(self):
        length = struct.unpack("!H",str(self[self.index:self.index+2]))[0]
        self.index += 2
        string = self[self.index:self.index+length]
        self.index += length
        return struct.unpack("!"+str(length)+"s", str(string))[0]

    def read_istring(self):
        length = struct.unpack("!I",str(self[self.index:self.index+4]))[0]
        self.index += 4
        string = self[self.index:self.index+length]
        self.index += length
        return struct.unpack("!"+str(length)+"s", str(string))[0]

    def write_ubyte(self, ubyte):
        self += struct.pack("=B", ubyte)
        return len(self)

    def write_byte(self, byte):
        self += struct.pack("=b", byte)
        return len(self)

    def write_ushort(self, ushort):
        self += struct.pack("=H", ushort)
        return len(self)

    def write_short(self, short):
        self += struct.pack("=h", short)
        return len(self)

    def write_uint(self, uint):
        self += struct.pack("=I", uint)
        return len(self)

    def write_int(self, integer):
        self += struct.pack("=i", integer)
        return len(self)

    def write_float(self, fl):
        self += struct.pack("=f", fl)
        return len(self)

    def write_double(self, db):
        self += struct.pack("=d", db)
        return len(self)

    def write_string(self, string):
        self += struct.pack("="+str(len(string))+"s", str(string))
        return len(self)

    def write_bstring(self, string):
        self += struct.pack("=B", len(string))
        self += struct.pack("="+str(len(string))+"s", str(string))
        return len(self)

    def write_sstring(self, string):
        self += struct.pack("=H", len(string))
        self += struct.pack("="+str(len(string))+"s", str(string))
        return len(self)

    def write_istring(self, string):
        self += struct.pack("=I", len(string))
        self += struct.pack("="+str(len(string))+"s", str(string))
        return len(self)
