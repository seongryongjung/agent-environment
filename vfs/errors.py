class VFSError(Exception):
    """VFS 기본 예외"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class VFSFileNotFoundError(VFSError):
    def __init__(self, path: str):
        super().__init__(f"파일 또는 디렉토리를 찾을 수 없습니다: {path}")
        self.path = path


class VFSNotADirectoryError(VFSError):
    def __init__(self, path: str):
        super().__init__(f"디렉토리가 아닙니다: {path}")
        self.path = path


class VFSIsADirectoryError(VFSError):
    def __init__(self, path: str):
        super().__init__(f"파일이 아닌 디렉토리입니다: {path}")
        self.path = path


class VFSFileExistsError(VFSError):
    def __init__(self, path: str):
        super().__init__(f"이미 존재합니다: {path}")
        self.path = path
