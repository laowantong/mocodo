

from collections import Counter
import contextlib
from importlib import import_module
import re
from pathlib import Path

from .tools.parser_tools import parse_source
from .tools.string_tools import rstrip_digit_or_underline

BLACKLIST = {
    "fr": ["date", "calendrier", "période"],
    "en": ["date", "calendar", "period"]
}

def guess_title(source, language):
    """
    Find the name of the most referenced entity in the MCD
    and pluralize it.
    """
    blacklist = BLACKLIST.get(language, [])
    tree = parse_source(source)
    names = []
    for node in tree.find_data("entity_name_ref"):
        name = rstrip_digit_or_underline(node.children[0].children[0])
        if name.lower() not in blacklist:
            names.append(name)
    counter = Counter(names)
    if not counter:
        return ""
    title = counter.most_common(1)[0][0]
    title = re.sub(r"[^\w '\._-]", "-", title)
    with contextlib.suppress(ModuleNotFoundError):
        pluralize = import_module(f"tools.pluralize_{language}").pluralize
        title = " ".join(map(pluralize, title.split()))
    return title.capitalize()


def may_update_params_with_guessed_title(source, params):
    if not params.get("guess_title"):
        return
    language = params["language"][:2]
    title = guess_title(source, language)
    if not title:
        return
    Path(f"{params['output_name']}_new_title.txt").write_text(title, encoding="utf8")
    params["title"] = title
    params["output_name"] = str(Path(params["output_dir"], title))
