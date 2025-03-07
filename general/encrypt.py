import base64

from Crypto.Cipher import AES

from general.common_exceptions import DecryptError, EncryptError
from utils.logger import logger


def encrypt(instr: str, key: str = "frontendencryptx", iv: str = None):
    try:
        iv = str(iv.ljust(16, "x"))  # 补齐 16 位
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        ret = base64.b64encode(cipher.encrypt(pad(str(instr))))

    except Exception as e:
        logger.error(e)
        raise EncryptError()

    return ret.decode()


def decrypt(instr, key="frontendencryptx", iv: str = None):
    try:
        iv = str(iv.ljust(16, "x"))  # 补齐 16 位
        b64str = base64.b64decode(format_instr(str(instr)))
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        ret = un_pad(cipher.decrypt(b64str))
        ret = ret.decode()
    except Exception as e:
        logger.error(e)
        raise DecryptError()
    return ret


def format_instr(instr) -> str:
    return instr.replace(" ", "+")


def pad(s) -> bytes:
    """
    填充字符串
    """
    bs = AES.block_size
    s = s.encode()
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode()


def un_pad(s) -> str:
    """
    去除填充
    """
    return s[: -ord(s[len(s) - 1 :])]
