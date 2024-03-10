import asyncio
from typing import Any, BinaryIO, List, Union
import numpy as np

from src.models import InSwapper
from src.exceptions import NoFacesFoundException
from src.utils import (
    numpy_array_to_bytes,
    process_uploaded_image,
    init_detecting_model,
    init_swapper,
)


class InSwapperProcessor:
    def __init__(self, in_swapper: InSwapper):
        self.in_swapper = in_swapper
        self.genereated_image = None
        self._app = init_detecting_model()
        self._swapper = init_swapper()

    async def replace_faces(self):
        result = await self._async_process_replace(
            self.in_swapper.face_img, self.in_swapper.source_img
        )
        self.genereated_image = result

    async def save_result(self):
        img = await numpy_array_to_bytes(self.genereated_image)
        self.in_swapper.result_img = img
        await self.in_swapper.save()

    async def _async_process_replace(
        self, face_image: BinaryIO, source_image: BinaryIO
    ):
        result = await asyncio.to_thread(
            self._sync_process_replace, face_image, source_image
        )
        return result

    def _sync_process_replace(self, face_image: BinaryIO, source_image: BinaryIO):
        source_face_img = process_uploaded_image(face_image)
        source_img = process_uploaded_image(source_image)

        faces = self._find_faces(source_img)
        source_face = self._find_faces(source_face_img, return_first=True)

        result = self._replace_faces_on_image(source_img, source_face, faces)
        return result

    def _find_faces(
        self, img: np.ndarray, return_first: bool = False
    ) -> Union[Any, List[Any]]:
        faces = self._app.get(img)
        faces = sorted(faces, key=lambda x: x.bbox[0])
        if not faces:
            raise NoFacesFoundException()
        return faces[0] if return_first else faces

    def _replace_faces_on_image(
        self, source_img: np.ndarray, source_face: np.ndarray, faces
    ) -> np.ndarray:
        result = source_img.copy()
        for face in faces:
            result = self._swapper.get(result, face, source_face, paste_back=True)
        return result
