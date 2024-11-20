class BasicError(Exception):
    pass


class SecurityError(Exception):
    pass


class EncryptError(SecurityError):
    def __init__(self):
        self.args = ("加密失败",)


class DecryptError(SecurityError):
    def __init__(self):
        self.args = ("解密失败",)
