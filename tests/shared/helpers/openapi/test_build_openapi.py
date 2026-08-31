import json

from src.shared.helpers.openapi.build_openapi import (
    build_openapi,
    discover_route_docs,
    load_generated_openapi,
)
from src.shared.helpers.openapi.route_doc import ApiRouteDoc


class Test_OpenApiBuilder:
    def test_discover_includes_delete_user_doc(self):
        docs = discover_route_docs()
        assert any(
            isinstance(doc, ApiRouteDoc)
            and doc.path == "/delete-user"
            and doc.method.upper() == "DELETE"
            for doc in docs
        )

    def test_build_openapi_has_delete_user_contract(self):
        spec = build_openapi()
        assert spec["openapi"].startswith("3.")
        delete_op = spec["paths"]["/delete-user"]["delete"]
        assert delete_op["summary"] == "Deleta um usuário"
        assert "requestBody" in delete_op
        assert "200" in delete_op["responses"]
        assert "400" in delete_op["responses"]
        schemas = spec["components"]["schemas"]
        assert "DeleteUserRequest" in schemas
        assert "DeleteUserResponse" in schemas
        assert "ErrorResponse" in schemas
        assert "user_id" in schemas["DeleteUserRequest"]["properties"]

    def test_generated_artifact_matches_builder(self):
        generated = load_generated_openapi()
        assert "/delete-user" in generated["paths"]
        assert generated["paths"]["/delete-user"]["delete"]["tags"] == ["users"]
