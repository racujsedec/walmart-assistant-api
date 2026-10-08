def sanitize_tool_text(text:str)->str:
 # Demonstrates output-length control; not a complete prompt-injection defense.
 return text[:4000]
