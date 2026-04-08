"""OpenAI function calling 형식으로 변환"""


def convert(schemas: list[dict]) -> list[dict]:
    """
    공용 schema → OpenAI tools 형식

    공용:   {"name": ..., "description": ..., "parameters": {...}}
    OpenAI: {"type": "function", "function": {"name": ..., "description": ..., "parameters": {...}}}
    """
    return [{"type": "function", "function": s} for s in schemas]
