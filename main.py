import os
import sys
import socket
import time
from bedray_lib.utils import BinaryStream
from bedray_lib.raknet import RakNetPacket

current_dir = os.path.dirname(os.path.abspath(__file__))
# Thêm nó vào danh sách tìm kiếm của Python
sys.path.append(current_dir)

def start_bedray_ai():
    # 1. Cấu hình địa chỉ server
    SERVER_IP = "127.0.0.1"
    PORT = 19132
    
    # 2. Tạo Socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    
    print(f"🚀 Bedray AI đang khởi động...")

    try:
        # BƯỚC 1: Gửi Unconnected Ping để kiểm tra server
        print("🔍 Đang tìm server...")
        ping_packet = b'\x01' + (0).to_bytes(8, 'big') + BinaryStream.MAGIC + (0).to_bytes(8, 'big')
        sock.sendto(ping_packet, (SERVER_IP, PORT))
        
        data, addr = sock.recvfrom(2048)
        if data[0] == 0x1c:
            print("✅ Đã thấy server! Đang bắt đầu quá trình Handshake...")
            
            # BƯỚC 2: Gửi Open Connection Request 1 (Gõ cửa)
            req1 = RakNetPacket.create_open_request_1()
            sock.sendto(req1, (SERVER_IP, PORT))
            print("📤 Đã gửi Open Request 1 (MTU 1200)")
            
            data, addr = sock.recvfrom(2048)
            if data[0] == 0x06: # Open Connection Reply 1
                print("📩 Server đã trả lời (Reply 1). Đang gửi tiếp Request 2...")
                
                # BƯỚC 3: Gửi Open Connection Request 2 (Xin vào)
                req2 = RakNetPacket.create_open_request_2(SERVER_IP, PORT)
                sock.sendto(req2, (SERVER_IP, PORT))
                
                data, addr = sock.recvfrom(2048)
                if data[0] == 0x08: # Open Connection Reply 2
                    print("🎉 THÀNH CÔNG! Server đã chấp nhận kết nối RakNet của Bedray.")
                    print("🤖 Bây giờ AI đã có thể bắt đầu gửi gói tin Login của Minecraft!")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("Hãy chắc chắn rằng bạn đã chạy server bằng lệnh: cd mc_server && ./start.sh")
    finally:
        sock.close()

if __name__ == "__main__":
    start_bedray_ai()

