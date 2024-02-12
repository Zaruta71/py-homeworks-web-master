import pydantic


class PersonModel(pydantic.BaseModel):
    id: int
    birth_year: str
    eye_color: str
    films: str
    gender: str
    hair_color: str
    height: str
    homeworld: str
    mass: str
    name: str
    skin_color: str
    species: str
    starships: str
    vehicles: str


def validator_model(data: dict, model):
    try:
        return model(**data).dict()
    except pydantic.ValidationError as error:
        return error.errors()
