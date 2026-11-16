import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src")
    )
)

from app import lambda_handler


def test_lambda_handler():
    response = lambda_handler({}, None)

    assert response["statusCode"] == 200
    assert response["body"] == "Hello from AWS Lambda CI/CD!"
