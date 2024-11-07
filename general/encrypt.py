import base64
from Crypto.Cipher import AES


def encrypt(instr, key=b'frontendencryptx', iv=b'frontendencryptx'):
    temp_str = pad(instr)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = base64.b64encode(cipher.encrypt(temp_str))
    return ret


def decrypt(instr, key=b'frontendencryptx', iv=b'frontendencryptx'):
    instr = base64.b64decode(instr)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = un_pad(cipher.decrypt(instr))
    ret = ret.decode(encoding="utf-8")
    return ret


def pad(s):
    bs = AES.block_size
    s = s.encode("utf-8")
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode("utf-8")


def un_pad(s):
    return s[:-ord(s[len(s) - 1:])]
