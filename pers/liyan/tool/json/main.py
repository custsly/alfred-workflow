import json
import pyperclip
from pygments import highlight, lexers, formatters

if __name__ == '__main__':
    formatted_json = json.dumps(json.loads(pyperclip.paste()), indent=4, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)
