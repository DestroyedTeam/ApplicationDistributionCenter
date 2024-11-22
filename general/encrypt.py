import base64

from Crypto.Cipher import AES

from general.common_exceptions import DecryptError, EncryptError


def encrypt(instr, key=b"frontendencryptx", iv=b"frontendencryptx"):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ret = base64.b64encode(cipher.encrypt(pad(instr)))
    except Exception:
        raise EncryptError()
    return ret


def decrypt(instr, key=b"frontendencryptx", iv=b"frontendencryptx"):
    try:
        b64str = base64.b64decode(format_instr(instr))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ret = un_pad(cipher.decrypt(b64str))
        ret = ret.decode(encoding="utf-8")
    except Exception:
        raise DecryptError()
    return ret


def format_instr(instr) -> str:
    return instr.replace(" ", "+")


def pad(s) -> bytes:
    """
    填充字符串
    """
    bs = AES.block_size
    s = s.encode("utf-8")
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode("utf-8")


def un_pad(s) -> str:
    """
    去除填充
    """
    return s[: -ord(s[len(s) - 1 :])]
