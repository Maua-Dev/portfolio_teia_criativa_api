import json

from src.modules.get_api_docs.app.get_api_docs_presenter import lambda_handler


class Test_GetApiDocsPresenter:
    def test_openapi_json_endpoint(self):
        event = {
            "rawPath": "/portfolioTeiaCriativaApi/public/openapi-json",
            "headers": {"Host": "example.execute-api.sa-east-1.amazonaws.com"},
            "requestContext": {"stage": "dev"},
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert response["headers"]["Content-Type"] == "application/json"
        body = json.loads(response["body"])
        assert "/delete-user" in body["paths"]

    def test_swagger_html_endpoint(self):
        event = {
            "rawPath": "/portfolioTeiaCriativaApi/public/docs",
            "headers": {"Host": "example.execute-api.sa-east-1.amazonaws.com"},
            "requestContext": {"stage": "dev"},
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert "text/html" in response["headers"]["Content-Type"]
        assert "swagger-ui" in response["body"]
        assert "openapi-json" in response["body"]
