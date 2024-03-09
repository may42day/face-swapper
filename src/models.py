from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class InSwapper(Model):
    id = fields.IntField(pk=True)
    source_img = fields.BinaryField()
    face_img = fields.BinaryField()
    result_img = fields.BinaryField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "in_swapper"


InSwapperPydantic = pydantic_model_creator(InSwapper, name="InSwapper")
