from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTES = "quotes"
    ULIST = "ulist"
    OLIST = "olist"


##################################################################


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(
            text_node_to_parent_html_node(TextNode(block, block_to_block_type(block)))
        )
    return ParentNode("div", children=html_nodes)


def text_node_to_parent_html_node(text_node):
    match text_node.text_type:
        case TextType.PARAGRAPH:
            return ParentNode("p", children=text_to_leaf_html_nodes(text_node.text))
        case TextType.CODE:
            return ParentNode(
                "code",
                children=text_to_leaf_html_nodes(text_node.text.replace("```", "")),
            )
        case TextType.HEADING:
            return ParentNode(
                f"h{len(re.findall(r"^\#*\ ",text_node.text)[0])}",
                children=text_to_leaf_html_nodes(
                    text_node.text.replace(re.findall(r"^\#*\ ", text_node.text)[0], "")
                ),
            )
        case TextType.ULIST:
            splited_list_text = text_node.text.split("\n")
            children = []
            for list_text in splited_list_text:
                children.append(LeafNode("li", value=list_text.replace("- ", "")))
            return ParentNode("ul", children=children)
        case TextType.OLIST:
            splited_list_text = text_node.text.split("\n")
            children = []
            for list_text in splited_list_text:
                children.append(
                    LeafNode(
                        "li",
                        value=re.sub(
                            r"^\d*\.\ ",
                            "",
                            list_text,
                        ),
                    )
                )
            return ParentNode("ol", children=children)

        case _:
            return ParentNode(
                "p",
                children=text_to_leaf_html_nodes(text_node.text),
            )


###############################################################


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
