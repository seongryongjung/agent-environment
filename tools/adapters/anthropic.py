"""Anthropic tool use 형식으로 변환"""


def convert(schemas: list[dict]) -> list[dict]:
    """
    공용 schema → Anthropic tools 형식

    공용:      {"name": ..., "description": ..., "parameters": {...}}
    Anthropic: {"name": ..., "description": ..., "input_schema": {...}}
    """
    return [
        {
            "name":         s["name"],
            "description":  s["description"],
            "input_schema": s["parameters"],
        }
        for s in schemas
    ]
