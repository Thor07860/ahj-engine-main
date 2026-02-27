from app.schemas import BaseSchema


class CombinationMapperBase(BaseSchema):
	category_id: int | None = None
	equipment_id: int | None = None
	code_id: int
	label_id: int


class CombinationMapperCreate(CombinationMapperBase):
	pass


class CombinationMapperUpdate(CombinationMapperBase):
	pass


class CombinationMapperOut(CombinationMapperBase):
	id: int

