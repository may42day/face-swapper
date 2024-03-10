from typing import BinaryIO, Union, Any
from insightface.model_zoo.inswapper import INSwapper as InsightFaceSwapper
from insightface.app import FaceAnalysis
import insightface
import numpy as np
import aiohttp
import cv2
import re

from src.exceptions import InvalidDataFormatException, InvalidLinkException


async def handle_image(image_data: Union[Any, str]) -> BinaryIO:
    if hasattr(image_data, "file"):
        return image_data.file.read()

    elif isinstance(image_data, str):
        if await is_valid_url(image_data):
            return await download_image(image_data)
        else:
            raise InvalidLinkException()
    else:
        raise InvalidDataFormatException()


async def is_valid_url(url: str):
    url_pattern = re.compile(r"^https?://\S+$", re.IGNORECASE)
    return bool(url_pattern.match(url))


async def numpy_array_to_bytes(numpy_array: np.ndarray) -> bytes:
    _, result_bytes = cv2.imencode(".jpg", numpy_array)
    return result_bytes.tobytes()


async def download_image(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise ValueError(
                    f"Failed to download image from the specified link. Status code: {response.status}"
                )


def init_detecting_model() -> FaceAnalysis:
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def init_swapper() -> InsightFaceSwapper:
    swapper = insightface.model_zoo.get_model(
        "inswapper_128.onnx", download=True, download_zip=False
    )
    return swapper


def process_uploaded_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
