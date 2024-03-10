from fastapi import APIRouter, Response, UploadFile, HTTPException
from typing import Union
from src.exceptions import (
    InvalidDataFormatException,
    InvalidLinkException,
    NoFacesFoundException,
)
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
                "application/json": {
                    "example": {"detail": "No faces detected on picture"}
                },
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
    try:
        face_image = await handle_image(face_image)
        source_image = await handle_image(source_image)
    except InvalidLinkException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except InvalidDataFormatException as e:
        raise HTTPException(status_code=400, detail=e.detail)

    in_swapper = await InSwapper.create(source_img=source_image, face_img=face_image)
    processor = InSwapperProcessor(in_swapper)
    try:
        await processor.replace_faces()
    except NoFacesFoundException as e:
        raise HTTPException(status_code=400, detail=e.detail)

    await processor.save_result()
    return Response(content=in_swapper.result_img, media_type="image/png")
