from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()

class Film(BaseModel):
    id: str
    title: str

# Inject FilmService using Depends(get_film_service)
@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)):
    film = await film_service.get_by_id(film_id)
    if not film:
# If the film is not found, return a 404 status
# It is desirable to use already defined HTTP statuses that contain an enum
# Such code will be more maintainable
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
# Transfer data from models.Film to Film
# Note that the business logic model has a description field,
# which is missing in the API response model.
# If a common model were used for business logic and forming API responses,
# you would provide clients with data they don't need
# and, possibly, data that is dangerous to return
    return Film(id=film.id, title=film.title) 