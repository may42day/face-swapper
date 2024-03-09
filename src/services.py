from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
import asyncio

from src.utils import (
    numpy_array_to_bytes,
    process_uploaded_image,
    init_detecting_model,
    init_swapper,
)


class InSwapperProcessor:
    def __init__(self, in_swapper):
        self.in_swapper = in_swapper
        self.genereated_image = None

    async def replace_faces(self):
        result = await self._async_process_replace(
            self.in_swapper.face_img, self.in_swapper.source_img
        )
        self.genereated_image = result

    async def save_result(self):
        img = await numpy_array_to_bytes(self.genereated_image)
        self.in_swapper.result_img = img
        await self.in_swapper.save()

    async def _async_process_replace(self, face_image, source_image):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, self._sync_process_replace, face_image, source_image
            )
        return result

    def _sync_process_replace(self, face_image, source_image):
        source_face_img = process_uploaded_image(face_image)
        source_img = process_uploaded_image(source_image)

        app = init_detecting_model()
        swapper = init_swapper()

        faces = self._find_faces(app, source_img)
        source_face = self._find_faces(app, source_face_img, return_first=True)

        result = self._replace_faces_on_image(source_img, source_face, faces, swapper)
        return result

    def _find_faces(self, app, img, return_first=False):
        faces = app.get(img)
        faces = sorted(faces, key=lambda x: x.bbox[0])
        if not faces:
            raise HTTPException(status_code=400, detail="No faces detected on picture")
        return faces[0] if return_first else faces

    def _replace_faces_on_image(self, source_img, source_face, faces, swapper):
        result = source_img.copy()
        for face in faces:
            result = swapper.get(result, face, source_face, paste_back=True)
        return result
