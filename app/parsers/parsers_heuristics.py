
""" This dictionary maps HTML element tags to their attributes (in a tuple) that are of interest for URL extraction."""
INTERESTING_ELEMENTS_ATTRIBUTES_MAP: dict[str, tuple[str, ...]] = {
    "a": ("href",),
    "script": ("src", "content", "href", "onclick", "action", "formaction", "codebase"),
    "link": ("href", "src"),
    "form": ("action",),
    "object": ("data",),
    "button": ("onclick", "formaction"),
    "embed": ("src",),
    "iframe": ("src",),
}