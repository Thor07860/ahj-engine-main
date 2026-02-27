from app.schemas import BaseSchema


class FormulaBase(BaseSchema):
	title: str | None = None
	description: str
	formula_link_type_id: int | None = None
	code_id: int


class FormulaCreate(FormulaBase):
	pass


class FormulaUpdate(FormulaBase):
	pass


class FormulaOut(FormulaBase):
	id: int

