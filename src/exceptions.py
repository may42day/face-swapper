class InvalidLinkException(Exception):
    def __init__(self, detail: str = "Invalid URL format"):
        super().__init__(detail)
        self.detail = detail


class NoFacesFoundException(Exception):
    def __init__(self, detail: str = "No faces found on the image"):
        super().__init__(detail)
        self.detail = detail


class InvalidDataFormatException(Exception):
    def __init__(self, detail: str = "Invalid image data format"):
        super().__init__(detail)
        self.detail = detail
