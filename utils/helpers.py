
def extract_text_content(content) -> str:
    """
    Extract string text from LLM response content.
    Handles plain strings, lists of message blocks/dicts, and objects with .text.
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                parts.append(part["text"])
            elif hasattr(part, "text"):
                parts.append(str(part.text))
        return "\n".join(parts)
    elif hasattr(content, "text"):
        return str(content.text)
    return str(content)

