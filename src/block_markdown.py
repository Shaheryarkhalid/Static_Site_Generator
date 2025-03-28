import re
from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTES = "quotes"
    ULIST = "ulist"
    OLIST = "olist"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        if not block or block in ("",):
            continue
        html_nodes.append(
            text_node_to_parent_html_node(TextNode(block, block_to_block_type(block)))
        )
    return ParentNode("div", children=html_nodes)


def text_node_to_parent_html_node(text_node):

    match text_node.text_type:
        case BlockType.PARAGRAPH:
            return ParentNode(
                "p", children=text_to_leaf_html_nodes(text_node.text.replace("\n", " "))
            )
        case BlockType.CODE:
            text_node.text = text_node.text.replace("```", "")
            return ParentNode(
                "code",
                children=text_to_leaf_html_nodes(text_node.text.replace("\n", " ")),
            )
        case BlockType.QUOTES:
            text_node.text = text_node.text.replace("> ", "")
            return ParentNode(
                "blockquote",
                children=text_to_leaf_html_nodes(text_node.text.replace("\n", " ")),
            )

        case BlockType.HEADING:
            length_of_heading_markers = (
                len(re.findall(r"^\#*\ ", text_node.text)[0]) - 1
            )
            return ParentNode(
                f"h{ length_of_heading_markers  if  length_of_heading_markers<=6 else  6}",
                children=text_to_leaf_html_nodes(
                    text_node.text.replace(
                        re.findall(r"^\#*\ ", text_node.text)[0], ""
                    ).replace("\n", " ")
                ),
            )
        case BlockType.ULIST:
            splited_list_text = text_node.text.split("\n")
            children = []
            for list_text in splited_list_text:
                children.append(
                    ParentNode(
                        "li",
                        children=text_to_leaf_html_nodes(list_text.replace("- ", "")),
                    )
                )
            return ParentNode("ul", children=children)
        case BlockType.OLIST:
            splited_list_text = text_node.text.split("\n")
            children = []
            for list_text in splited_list_text:
                children.append(
                    ParentNode(
                        "li",
                        children=text_to_leaf_html_nodes(
                            re.sub(
                                r"^\d*\.\ ",
                                "",
                                list_text,
                            ),
                        ),
                    )
                )
            return ParentNode("ol", children=children)

        case _:
            return ParentNode(
                "p",
                children=text_to_leaf_html_nodes(text_node.text.replace("\n", " ")),
            )


def text_to_leaf_html_nodes(text):
    if not text:
        return []
    child_text_nodes = text_to_textnodes(text)
    children = []
    for child_text_node in child_text_nodes:
        if child_text_node.text == "":
            continue
        children.append(text_node_to_html_node(child_text_node))
    return children


def block_to_block_type(block):

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        return BlockType.QUOTES
    if block.startswith("- "):
        return BlockType.ULIST
    if re.findall(r"^\d*\.\ ", block):
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    new_blocks = filter(lambda x: x not in ("", "\n"), new_blocks)
    new_blocks = list(map(lambda x: x.strip(), new_blocks))
    return new_blocks
