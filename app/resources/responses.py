from fastapi.responses import JSONResponse
from http import HTTPStatus

user_not_found = JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": "User not found"})
user_created = JSONResponse( status_code=HTTPStatus.CREATED, content={"detail": "User created"})
user_exists = JSONResponse( status_code=HTTPStatus.CONFLICT, content={"detail": "User email exists"})
user_not_found = JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": "User not found"})
user_not_found_by_id = JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": "User not found by id"})
user_not_found_by_email = JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": "User not found by email"})
user_not_found_by_id_or_email = JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": "User not found by id or email"})

