from fastapi import APIRouter, Response, UploadFile
from typing import Union
from src.services import InSwapperProcessor
from src.models import InSwapper

from src.utils import handle_image

router = APIRouter(prefix="/api/v1/swapper")


@router.post(
    "/in-swapping",
    responses={
        200: {"description": "Success", "content": {"image/jpeg": {}}},
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {"example": {"detail": "No faces detected on picture"}},
                "application/json": {"example": {"detail": "Invalid URL format"}},
                "application/json": {
                    "example": {"detail": "Invalid image data format"}
                },
            },
        },
        500: {"description": "Internal Server Error"},
    },
    response_class=Response,
)
async def in_swapping_faces(
    face_image: Union[UploadFile, str], source_image: Union[UploadFile, str]
):

    face_image = await handle_image(face_image)
    source_image = await handle_image(source_image)

    in_swapper = await InSwapper.create(source_img=source_image, face_img=face_image)
    processor = InSwapperProcessor(in_swapper)
    await processor.replace_faces()
    await processor.save_result()
    in_swapper = await InSwapper.filter(id__gt=0).first()

    return Response(content=in_swapper.result_img, media_type="image/png")
