from typing import Any, Tuple, Union

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from kaiba.process import Process
from kaiba.schema import SCHEMA
from pydantic import BaseModel

app = FastAPI()

origins = [
    'http://localhost:5000',
    'http://localhost',
    'http://localhost:8080',
    'https://app.kaiba.tech',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


def create_success_response(
    body, *args, **kwargs,
) -> Tuple[Any, int]:
    """Return success response."""
    return (body, status.HTTP_200_OK)


def create_failure_response(failure: Exception) -> Tuple[Any, int]:
    """Return failure response."""
    error_message = '{failure}'.format(
        failure=failure,
    )
    return ({'error': error_message}, status.HTTP_400_BAD_REQUEST)


@app.get('/')
async def read_schema():
    """Provide Kaiba schema for validation."""
    return SCHEMA


class MapperRequest(BaseModel):
    """Dataclass for our request params."""

    data: Union[dict, list]  # noqa: WPS110 - allow as input
    configuration: dict


@app.post('/')
def mapper(
    request: MapperRequest,
    response: Response,
):
    """Maps incoming data with provided Kaiba config."""
    body, code = Process()(
        request.data,
        request.configuration,
    ).map(
        create_success_response,
    ).alt(
        create_failure_response,
    ).unwrap()

    response.status_code = code
    return body
