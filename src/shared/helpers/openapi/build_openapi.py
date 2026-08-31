from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from src.shared.helpers.openapi.route_doc import ApiRouteDoc

_ERROR_DESCRIPTIONS = {
    400: "Bad Request — parâmetros inválidos ou ausentes",
    404: "Not Found — recurso não encontrado",
    500: "Internal Server Error",
}


def _repo_root() -> Path:
    # .../src/shared/helpers/openapi/build_openapi.py → repo root
    return Path(__file__).resolve().parents[4]


def _modules_app_dir() -> Path:
    return _repo_root() / "src" / "modules"


def discover_route_docs(modules_dir: Path | None = None) -> list[ApiRouteDoc]:
    """
    Encontra `src/modules/*/app/*_doc.py` que exportam `DOC: ApiRouteDoc`.
    """
    base = modules_dir or _modules_app_dir()
    docs: list[ApiRouteDoc] = []

    if not base.exists():
        return docs

    for doc_path in sorted(base.glob("*/app/*_doc.py")):
        module_name = f"_openapi_doc_{doc_path.stem}_{doc_path.parent.parent.name}"
        spec = importlib.util.spec_from_file_location(module_name, doc_path)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        doc = getattr(module, "DOC", None)
        if isinstance(doc, ApiRouteDoc):
            docs.append(doc)

    return docs


def _schema_ref_name(model: type) -> str:
    return model.__name__


def _model_schema(model: type) -> dict[str, Any]:
    schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
    # Pydantic may nest $defs; flatten into components later
    return schema


def build_openapi(
    docs: list[ApiRouteDoc] | None = None,
    *,
    title: str = "Portfolio Teia Criativa API",
    version: str = "1.0.0",
    description: str = (
        "Documentação OpenAPI gerada a partir dos arquivos `*_doc.py` de cada rota. "
        "Para documentar uma rota nova, crie apenas `src/modules/<rota>/app/<rota>_doc.py`."
    ),
) -> dict[str, Any]:
    route_docs = docs if docs is not None else discover_route_docs()

    components_schemas: dict[str, Any] = {}
    paths: dict[str, Any] = {}

    def register_model(model: type) -> str:
        name = _schema_ref_name(model)
        if name in components_schemas:
            return name

        raw = _model_schema(model)
        defs = raw.pop("$defs", None) or raw.pop("definitions", None)
        if defs:
            for def_name, def_schema in defs.items():
                components_schemas.setdefault(def_name, def_schema)
        components_schemas[name] = raw
        return name

    for doc in route_docs:
        method = doc.method.lower()
        path_item = paths.setdefault(doc.path, {})

        operation: dict[str, Any] = {
            "summary": doc.summary,
            "description": doc.description,
            "tags": doc.tags or ["default"],
            "responses": {},
        }

        if doc.request_model is not None:
            req_name = register_model(doc.request_model)
            operation["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{req_name}"}
                    }
                },
            }

        if doc.response_model is not None:
            res_name = register_model(doc.response_model)
            operation["responses"]["200"] = {
                "description": "Sucesso",
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{res_name}"}
                    }
                },
            }
        else:
            operation["responses"]["200"] = {"description": "Sucesso"}

        err_name = register_model(doc.error_model)
        for status in doc.error_statuses:
            operation["responses"][str(status)] = {
                "description": _ERROR_DESCRIPTIONS.get(status, f"HTTP {status}"),
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{err_name}"}
                    }
                },
            }

        path_item[method] = operation

    return {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": version,
            "description": description,
        },
        "paths": paths,
        "components": {"schemas": components_schemas},
    }


def write_openapi_artifacts(spec: dict[str, Any] | None = None) -> tuple[Path, Path]:
    """
    Grava a spec em:
    - docs/openapi.json (visão no repo / front)
    - src/shared/helpers/openapi/generated_openapi.json (layer da Lambda)
    """
    document = spec if spec is not None else build_openapi()
    root = _repo_root()

    docs_path = root / "docs" / "openapi.json"
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    layer_path = Path(__file__).resolve().parent / "generated_openapi.json"

    payload = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    docs_path.write_text(payload, encoding="utf-8")
    layer_path.write_text(payload, encoding="utf-8")
    return docs_path, layer_path


def load_generated_openapi() -> dict[str, Any]:
    """Carrega a spec gerada (uso na Lambda de docs)."""
    layer_path = Path(__file__).resolve().parent / "generated_openapi.json"
    if layer_path.exists():
        return json.loads(layer_path.read_text(encoding="utf-8"))
    return build_openapi()
