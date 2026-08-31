#!/usr/bin/env python3
"""Gera docs/openapi.json e a cópia usada pela Lambda (shared/helpers/openapi)."""

from src.shared.helpers.openapi.build_openapi import write_openapi_artifacts


def main() -> None:
    docs_path, layer_path = write_openapi_artifacts()
    print(f"Wrote {docs_path}")
    print(f"Wrote {layer_path}")


if __name__ == "__main__":
    main()
