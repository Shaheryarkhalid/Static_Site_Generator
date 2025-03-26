from typing import Text
import unittest
from htmlnode import LeafNode
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_with_bold(self):
        text_nodes = [TextNode("This is just a **bold** text.", TextType.TEXT)]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="**", text_type=TextType.BOLD
        )
        expected_value = [
            TextNode("This is just a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(leaf_nodes, expected_value)

    def test_with_italic(self):
        text_nodes = [TextNode("This is just a _italic_ text.", TextType.TEXT)]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="_", text_type=TextType.ITALIC
        )
        expected_value = [
            TextNode("This is just a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(leaf_nodes, expected_value)

    def test_with_code(self):
        text_nodes = [TextNode("This is just a `code` text.", TextType.TEXT)]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="`", text_type=TextType.CODE
        )
        expected_value = [
            TextNode("This is just a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(leaf_nodes, expected_value)

    def test_with_multiple_inline_textnodes(self):
        text_nodes = [
            TextNode(
                "This is just a **bold** text.**And** its not a test.", TextType.TEXT
            )
        ]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="**", text_type=TextType.BOLD
        )
        expected_value = [
            TextNode("This is just a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("And", TextType.BOLD),
            TextNode(" its not a test.", TextType.TEXT),
        ]
        self.assertEqual(leaf_nodes, expected_value)

    def test_with_inline_textnodes_in_start(self):
        text_nodes = [
            TextNode(
                "**This** is just a **bold** text.**And** its not a test.",
                TextType.TEXT,
            )
        ]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="**", text_type=TextType.BOLD
        )
        expected_value = [
            TextNode("This", TextType.BOLD),
            TextNode(" is just a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("And", TextType.BOLD),
            TextNode(" its not a test.", TextType.TEXT),
        ]
        self.assertEqual(leaf_nodes, expected_value)

    def test_with_invalid_textnode_texttype(self):
        text_nodes = [TextNode("This is just a **bold** text.", TextType.CODE)]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="**", text_type=TextType.BOLD
        )
        expected_value = text_nodes
        self.assertEqual(expected_value, leaf_nodes)

    def test_with_invalid_markdown_syntax(self):
        text_nodes = [TextNode("This is just a **bold text.", TextType.TEXT)]
        try:
            split_nodes_delimiter(text_nodes, delimiter="**", text_type=TextType.BOLD)
        except Exception as e:
            self.assertIsInstance(e, ValueError)
            self.assertEqual(str(e), "Invalid markdown syntax.")
        else:
            self.fail("Invalid markdown syntax.")

    def test_with_multiple_textNodes(self):
        text_nodes = [
            TextNode(
                "**This** is just a **bold** text.**And** its not a test.",
                TextType.TEXT,
            ),
            TextNode(
                "**This** is just a **bold** text.**And** its not a test.",
                TextType.TEXT,
            ),
        ]
        leaf_nodes = split_nodes_delimiter(
            text_nodes, delimiter="**", text_type=TextType.BOLD
        )
        expected_value = [
            TextNode("This", TextType.BOLD),
            TextNode(" is just a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("And", TextType.BOLD),
            TextNode(" its not a test.", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" is just a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("And", TextType.BOLD),
            TextNode(" its not a test.", TextType.TEXT),
        ]
        self.assertEqual(leaf_nodes, expected_value)


class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_if_parsing_images_with_alt_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)

    def test_if_parsing_images_without_image_differeniator(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)

    def test_if_parsing_images_without_alt_text(self):
        text = "This is text with a  and "
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_if_parsing_link_with_href_text(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)

    def test_if_parsing_links_with_image_differeniator(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)

    def test_if_parsing_links_without_href_text_and_link(self):
        text = "This is text with a  and "
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)


class TestSplitLinks(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_without_any_links(self):
        node = TextNode(
            "This is text with an  and another ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_image_marker(self):
        node = TextNode(
            "This is text with an  ![image](https://i.imgur.com/zjjcJKZ.png) and another ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_without_any_image(self):
        node = TextNode(
            "This is text with an  and another ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_with_link_marker(self):
        node = TextNode(
            "This is text with an  [image](https://i.imgur.com/zjjcJKZ.png) and another ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


class TestTextToTextnodes(unittest.TestCase):

    def test_with_simple_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
