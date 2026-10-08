# Prompts
`system.txt` is loaded by `claude_client.py` at runtime. `few_shots.json` is a versioned evaluation/reference set, not automatically inserted into every prompt. Tool schemas live in `claude_client.py`. Do not place secrets or raw customer data in prompt files.
