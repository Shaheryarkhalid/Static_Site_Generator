import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    text_node_to_parent_html_node,
    text_to_leaf_html_nodes,
)
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_with_empty_string(self):
        md = ""

        expected = []
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_with_single_line(self):
        md = "This is **bolded** paragraph"
        expected = ["This is **bolded** paragraph"]
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected)


class TestBlockToBlockType(unittest.TestCase):

    def test_with_heading1_block(self):
        input = "# Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.HEADING)

    def test_with_heading2_block(self):
        input = "## Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.HEADING)

    def test_with_heading3_block(self):
        input = "### Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.HEADING)

    def test_with_heading4_block(self):
        input = "#### Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.HEADING)

    def test_with_heading5_block(self):
        input = "##### Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.HEADING)

    def test_with_heading6_block(self):
        input = "###### Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.HEADING)

    def test_with_heading7_block(self):
        input = "####### Heading"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_with_code_block(self):
        input = "```Code```"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.CODE)

    def test_with_wrong_code_block(self):
        input = "```Code"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_with_quotes_block(self):
        input = "> Quote"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.QUOTES)

    def test_with_Unordered_list_block(self):
        input = "- Unordered List"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.ULIST)

    def test_with_Unordered_list_in_the_middle_of_block(self):
        input = "This is a - Unordered List"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_with_ordered_list_block(self):
        input = "1. Quote"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.OLIST)

    def test_with_ordered_list_in_the_middle_of_block(self):
        input = "This is a 1. Unordered List"
        actual = block_to_block_type(input)
        self.assertEqual(actual, BlockType.PARAGRAPH)


class TestTextToLeafHtmlNodes(unittest.TestCase):

    test_cases = [
        {"input": "", "expected": []},
        {"input": None, "expected": []},
        {
            "input": "This is a test",
            "expected": [LeafNode(None, value="This is a test")],
        },
        {
            "input": "This is just a **Bold**",
            "expected": [
                LeafNode(None, "This is just a "),
                LeafNode("b", "Bold"),
            ],
        },
        {
            "input": "_This_ is just a **Bold**",
            "expected": [
                LeafNode("i", "This"),
                LeafNode(None, " is just a "),
                LeafNode("b", "Bold"),
            ],
        },
    ]

    def test_output(self):
        for test_case in TestTextToLeafHtmlNodes.test_cases:
            actual = text_to_leaf_html_nodes(test_case["input"])
            if "print" in test_case:
                print(test_case["print"])
            try:
                self.assertEqual(actual, test_case["expected"])
            except Exception:
                print("Test Failed")
                print("input :")
                print(test_case["expected"])
                print("expected :")
                print(actual)
                self.fail("Test failed for test_text_to_leaf_html_nodes.")


class TestTextNodeToParentHtmlNode(unittest.TestCase):
    test_cases = [
        {
            "input": TextNode(text=None, text_type=TextType.PARAGRAPH),
            "expected": ParentNode(
                "p",
                children=[],
            ),
            "print": "Testing with None as text",
        },
        {
            "input": TextNode(text="", text_type=TextType.PARAGRAPH),
            "expected": ParentNode(
                "p",
                children=[],
            ),
            "print": "Testing with empty string",
        },
        {
            "input": TextNode(text="This", text_type=TextType.PARAGRAPH),
            "expected": ParentNode(
                "p",
                children=[LeafNode(None, value="This")],
            ),
            "print": "Testing with only one word",
        },
    ]

    def test_output(self):
        for test_case in TestTextNodeToParentHtmlNode.test_cases:
            actual = text_node_to_parent_html_node(test_case["input"])
            if "print" in test_case:
                print(test_case["print"])
            try:
                self.assertEqual(actual, test_case["expected"])
            except Exception:
                print("Test Failed")
                print("input :")
                print(test_case["expected"])
                print("expected :")
                print(actual)
                self.fail("Test failed for text_node_to_parent_Html_node.")
