<<<<<<< HEAD
from app.schemas import BaseSchema


class LabelBase(BaseSchema):
	upc_code: str | None = None
	name: str | None = None
	label_number: str | None = None
	label_name: str | None = None
	field_type: str | None = None
	description: str | None = None
	length: int | None = None
	width: int | None = None
	image_url: str | None = None
	background_color: str | None = None
	text_color: str | None = None
	is_active: bool | None = True


class LabelCreate(LabelBase):
	pass


class LabelUpdate(LabelBase):
	pass


class LabelOut(LabelBase):
	id: int
	created_at: str | None = None

=======
from app.schemas import BaseSchema


class LabelBase(BaseSchema):
	upc_code: str | None = None
	name: str | None = None
	label_number: str | None = None
	label_name: str | None = None
	field_type: str | None = None
	description: str | None = None
	length: int | None = None
	width: int | None = None
	image_url: str | None = None
	background_color: str | None = None
	text_color: str | None = None
	is_active: bool | None = True


class LabelCreate(LabelBase):
	pass


class LabelUpdate(LabelBase):
	pass


class LabelOut(LabelBase):
	id: int
	created_at: str | None = None

>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
