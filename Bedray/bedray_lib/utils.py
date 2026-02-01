import struct

class BinaryStream:
    def __init__(self, data=b""):
        self.buffer = bytearray(data)
        self.offset = 0

    def write(self, data):
        self.buffer.extend(data)

    def read(self, length):
        data = self.buffer[self.offset : self.offset + length]
        self.offset += length
        return data

    # Ghi số nguyên VarInt (Số nén - Bedrock dùng rất nhiều)
    def write_varint(self, value):
        out = bytearray()
        while True:
            temp = value & 0x7F
            value >>= 7
            if value != 0:
                out.append(temp | 0x80)
            else:
                out.append(temp)
                break
        self.buffer.extend(out)

    def get_buffer(self):
        return bytes(self.buffer)

    # Magic bytes của RakNet để xác định phiên bản
    MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
