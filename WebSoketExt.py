import hashlib
import base64


def decodeMessage(bytesArr):
    if (bytesArr[0] & 0xF == 0x1):
        unmasked = bytearray(b"\x00" * len(bytesArr))
        for i in range(6, len(bytesArr)):
            j = ((i - 6) % 4)
            unmasked[i] = bytesArr[i] ^ bytesArr[2 + j]
        return unmasked[6:].decode()

def Sec_Key_gen(Key):
    magic_key = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    Key = Key + magic_key
    magic = base64.b64encode(hashlib.sha1(Key.encode('utf-8')).digest())
    return magic.decode()

def UpgradeConnection(client,Magic_Key):
    client.send(bytes(
        "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + Magic_Key + "\r\n\r\n",
        "UTF-8"))

def SendData(client,data):
    client.send((b"\x81\x02".replace(b"\x02",bytes([len(data)])) + data.encode()))

def ReceiveData(client):
    return decodeMessage(client.recv(1024))
