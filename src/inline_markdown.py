import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    leaf_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            leaf_nodes.append(old_node)
            continue
        string_chunks = old_node.text.split(delimiter)
        if not len(string_chunks) % 2:
            raise ValueError("Invalid markdown syntax.")
        is_plain_text = True
        if old_node.text.startswith(delimiter):
            is_plain_text = False
            string_chunks.pop(0)
        for value in string_chunks:
            node_type = TextType.TEXT if is_plain_text else text_type
            leaf_nodes.append(TextNode(value, node_type))
            is_plain_text = not is_plain_text
    return leaf_nodes


def split_nodes_image(old_nodes):
    return split_nodes(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, TextType.LINK)


def split_nodes(old_nodes, text_type):
    new_nodes = []
    for old_node in old_nodes:
        links_with_alt = (
            extract_markdown_links(old_node.text)
            if text_type == TextType.LINK
            else extract_markdown_images(old_node.text)
        )
        if not len(links_with_alt):
            new_nodes.append(old_node)
            continue
        for item in links_with_alt:
            new_nodes.extend(
                [
                    TextNode(
                        old_node.text.split(
                            f"[{item[0]}]({item[1]})"
                            if text_type == TextType.LINK
                            else f"![{item[0]}]({item[1]})"
                        )[0],
                        text_type=TextType.TEXT,
                    ),
                    TextNode(
                        text=item[0],
                        text_type=(
                            TextType.LINK
                            if text_type == TextType.LINK
                            else TextType.IMAGE
                        ),
                        url=item[1],
                    ),
                ]
            )

            old_node.text = old_node.text.split(
                f"[{item[0]}]({item[1]})"
                if text_type == TextType.LINK
                else f"![{item[0]}]({item[1]})"
            )[1]
        if old_node.text:
            new_nodes.extend(
                [
                    TextNode(
                        old_node.text,
                        text_type=TextType.TEXT,
                    )
                ]
            )

    return new_nodes


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
