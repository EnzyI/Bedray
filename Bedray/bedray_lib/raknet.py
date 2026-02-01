from .utils import BinaryStream

class RakNetPacket:
    # Gói tin đầu tiên: Open Connection Request 1
    @staticmethod
    def create_open_request_1(protocol_version=11):
        stream = BinaryStream()
        stream.write(b'\x05') # ID gói tin
        stream.write(BinaryStream.MAGIC)
        stream.write(bytes([protocol_version]))
        # Đệm thêm dữ liệu để đạt kích thước MTU (tối thiểu 1200 bytes cho Bedrock)
        stream.write(b'\x00' * 1200) 
        return stream.get_buffer()

    # Gói tin thứ hai: Open Connection Request 2
    @staticmethod
    def create_open_request_2(server_address, port):
        stream = BinaryStream()
        stream.write(b'\x07') # ID gói tin
        stream.write(BinaryStream.MAGIC)
        # Ghi địa chỉ server (đơn giản hóa cho localhost)
        stream.write(b'\x04\x7f\x00\x00\x01') # 127.0.0.1
        stream.write(port.to_bytes(2, 'big'))
        stream.write((1200).to_bytes(2, 'big')) # MTU Size
        stream.write(b'\x00\x01\x02\x03\x04\x05\x06\x07') # Client GUID
        return stream.get_buffer()
