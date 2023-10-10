from ..tools.string_tools import urlsafe_encoding


def run(source, subargs=None, common=None):
    return {
        "stem_suffix": "_url",
        "text": f"https://www.mocodo.net/?mcd={urlsafe_encoding(source)}",
        "extension": "url",
        "to_defer": True,
        "highlight": "url",
    }
