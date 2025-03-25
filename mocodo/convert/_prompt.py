from ..parse_mcd import Visitor
from ..tools.parser_tools import parse_source, reconstruct_source, first_child
from pathlib import Path

class CreateLegNotePlaceholder(Visitor):
    def assoc_leg(self, tree):
        """ Create or replace the leg note with a placeholder. """
        leg_note = first_child(tree, "leg_note")
        if leg_note:
            leg_note.value = "?"
        else:
            box_name = first_child(tree, "box_name")
            box_name.value = f"[?] {box_name.value}"

    def comment(self, tree):
        """ Suppress the comment line. """
        tree.children = []


class CreateTypePlaceholder(Visitor):
    def typed_attr(self, tree):
        if len(tree.children) == 1:
            tree.children[0].children[0].value += f" [?]"

def CreatePlaceholder(subarg):
    if subarg == "cards":
        return CreateLegNotePlaceholder()
    elif subarg == "types":
        return CreateTypePlaceholder()
    else:
        raise ValueError(f"Unknown subarg: {subarg}")


def get_prompt(source, chat_dir, subarg):
    prompt = Path(chat_dir, f"{subarg}_fr.md").read_text(encoding="utf8")
    examples = []
    for path in sorted(Path(chat_dir, f"{subarg}_examples").glob("*.mcd")):
        (i, name) = path.stem.split("_", 1)
        example_source = path.read_text(encoding="utf8")
        if name == "input":
            examples.append(f"## Example {i}\n\n### Question\n\n{backticks(example_source)}")
        elif name == "output":
            examples.append(f"### Answer\n\n{backticks(example_source)}")
    examples = "\n".join(examples)
    tree = parse_source(source)
    visitor = CreatePlaceholder(subarg)
    visitor.visit(tree)
    question = backticks(reconstruct_source(tree))
    return prompt.format(examples=examples, question=question)

def backticks(text):
    text = text.strip('\n')
    return f"```mocodo\n{text}\n```\n"

def run(source, subargs, common):
    chat_dir = Path(common.params["script_directory"], "resources", "prompts", "chat")
    prompt = ""
    for subarg in subargs:
        if subarg in ("cards", "types"):
            prompt = get_prompt(source, chat_dir, subarg)
            break
    return {
        "stem_suffix": f"_prompt_for_{subarg}",
        "text": prompt,
        "extension": "md",
        "to_defer": False,
        "highlight": "md",
    }
