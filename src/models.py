from tortoise import fields
from tortoise.models import Model


class InSwapper(Model):
    id = fields.IntField(pk=True)
    source_img = fields.BinaryField()
    face_img = fields.BinaryField()
    result_img = fields.BinaryField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "in_swapper"
