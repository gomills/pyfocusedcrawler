from tree_sitter import Language, Parser, Tree
import tree_sitter_javascript as tsjavascript


class JsParser:
    def __init__(self):
        self.language = Language(tsjavascript.language())
        self.parser = Parser(self.language)


js_parser = JsParser()


def get_js_tree(body: str, parser: Parser = js_parser.parser) -> Tree | None:
    if not body:
        return None

    # Parse the code into a syntax tree
    tree = parser.parse(body.encode())

    return tree
