import json

from src.shared.helpers.openapi.build_openapi import load_generated_openapi


def _wants_openapi_json(event: dict) -> bool:
    raw_path = (event.get("rawPath") or event.get("path") or "").lower()
    resource = (event.get("resource") or "").lower()
    return "openapi" in raw_path or "openapi" in resource


def _swagger_html(openapi_url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Portfolio Teia Criativa API — Docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.ui = SwaggerUIBundle({{
      url: {json.dumps(openapi_url)},
      dom_id: '#swagger-ui',
      presets: [SwaggerUIBundle.presets.apis],
      layout: 'BaseLayout'
    }});
  </script>
</body>
</html>
"""


def _openapi_url_from_event(event: dict) -> str:
    """
    Monta URL relativa estável no mesmo API Gateway.
    Fallback: openapi-json no mesmo nível de public/.
    """
    headers = event.get("headers") or {}
    # API Gateway REST (v1) costuma mandar Host; HTTP API (v2) também.
    host = headers.get("Host") or headers.get("host")
    stage = (event.get("requestContext") or {}).get("stage")
    if host and stage:
        return f"https://{host}/{stage}/portfolioTeiaCriativaApi/public/openapi-json"
    return "./openapi-json"


def lambda_handler(event, context):
    if _wants_openapi_json(event):
        spec = load_generated_openapi()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(spec, ensure_ascii=False),
            "isBase64Encoded": False,
        }

    html = _swagger_html(_openapi_url_from_event(event or {}))
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        },
        "body": html,
        "isBase64Encoded": False,
    }
