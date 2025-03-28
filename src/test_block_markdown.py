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
                print("expected :")
                print(test_case["expected"])
                print("actual :")
                print(actual)
                self.fail("Test failed for test_text_to_leaf_html_nodes.")


class TestTextNodeToParentHtmlNode(unittest.TestCase):
    test_cases = [
        {
            "input": TextNode(text="", text_type=BlockType.PARAGRAPH),
            "expected": ParentNode(
                "p",
                children=[],
            ),
        },
        {
            "input": TextNode(text="This", text_type=BlockType.PARAGRAPH),
            "expected": ParentNode(
                "p",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(
                text="This is a **nested** _italic_ string with `code` block.",
                text_type=BlockType.PARAGRAPH,
            ),
            "expected": ParentNode(
                "p",
                children=[
                    LeafNode(None, value="This is a "),
                    LeafNode("b", value="nested"),
                    LeafNode(None, value=" "),
                    LeafNode("i", value="italic"),
                    LeafNode(None, value=" string with "),
                    LeafNode("code", value="code"),
                    LeafNode(None, value=" block."),
                ],
            ),
        },
        {
            "input": TextNode(
                text="This is a **nested** _italic_ string\n with `code` block.",
                text_type=BlockType.PARAGRAPH,
            ),
            "expected": ParentNode(
                "p",
                children=[
                    LeafNode(None, value="This is a "),
                    LeafNode("b", value="nested"),
                    LeafNode(None, value=" "),
                    LeafNode("i", value="italic"),
                    LeafNode(None, value=" string  with "),
                    LeafNode("code", value="code"),
                    LeafNode(None, value=" block."),
                ],
            ),
        },
        {
            "input": TextNode(text="```This```", text_type=BlockType.CODE),
            "expected": ParentNode(
                "code",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(
                text="```This is a **nested** _italic_ string with `code` block.```",
                text_type=BlockType.CODE,
            ),
            "expected": ParentNode(
                "code",
                children=[
                    LeafNode(None, value="This is a "),
                    LeafNode("b", value="nested"),
                    LeafNode(None, value=" "),
                    LeafNode("i", value="italic"),
                    LeafNode(None, value=" string with "),
                    LeafNode("code", value="code"),
                    LeafNode(None, value=" block."),
                ],
            ),
        },
        {
            "input": TextNode(text="# This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h1",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(
                text="# This is a **nested** _italic_ string with `code` block.",
                text_type=BlockType.HEADING,
            ),
            "expected": ParentNode(
                "h1",
                children=[
                    LeafNode(None, value="This is a "),
                    LeafNode("b", value="nested"),
                    LeafNode(None, value=" "),
                    LeafNode("i", value="italic"),
                    LeafNode(None, value=" string with "),
                    LeafNode("code", value="code"),
                    LeafNode(None, value=" block."),
                ],
            ),
        },
        {
            "input": TextNode(text="## This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h2",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(
                text="## This is a **nested** _italic_ string with `code` block.",
                text_type=BlockType.HEADING,
            ),
            "expected": ParentNode(
                "h2",
                children=[
                    LeafNode(None, value="This is a "),
                    LeafNode("b", value="nested"),
                    LeafNode(None, value=" "),
                    LeafNode("i", value="italic"),
                    LeafNode(None, value=" string with "),
                    LeafNode("code", value="code"),
                    LeafNode(None, value=" block."),
                ],
            ),
        },
        {
            "input": TextNode(text="### This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h3",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(text="#### This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h4",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(text="##### This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h5",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(text="###### This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h6",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(text="####### This", text_type=BlockType.HEADING),
            "expected": ParentNode(
                "h6",
                children=[LeafNode(None, value="This")],
            ),
        },
        {
            "input": TextNode(text="- This", text_type=BlockType.ULIST),
            "expected": ParentNode(
                "ul",
                children=[LeafNode("li", value="This")],
            ),
        },
        {
            "input": TextNode(
                text="- apple\n- bannana\n- orange\n- mango.", text_type=BlockType.ULIST
            ),
            "expected": ParentNode(
                "ul",
                children=[
                    LeafNode("li", value="apple"),
                    LeafNode("li", value="bannana"),
                    LeafNode("li", value="orange"),
                    LeafNode("li", value="mango."),
                ],
            ),
        },
        {
            "input": TextNode(
                text="1. apple",
                text_type=BlockType.OLIST,
            ),
            "expected": ParentNode(
                "ol",
                children=[
                    LeafNode("li", value="apple"),
                ],
            ),
        },
        {
            "input": TextNode(
                text="1. apple\n2. bannana\n3. orange\n4. mango.",
                text_type=BlockType.OLIST,
            ),
            "expected": ParentNode(
                "ol",
                children=[
                    LeafNode("li", value="apple"),
                    LeafNode("li", value="bannana"),
                    LeafNode("li", value="orange"),
                    LeafNode("li", value="mango."),
                ],
            ),
        },
    ]

    def test_output(self):
        for test_case in TestTextNodeToParentHtmlNode.test_cases:
            actual = text_node_to_parent_html_node(test_case["input"])
            if "print" in test_case:
                print(test_case["print"])
            try:
                self.assertEqual(actual, test_case["expected"])
            except Exception as _:
                print(
                    "Error happened while testing TextNode To Parent HTML Node. \n Function name : text_node_to_parent_html_node \n Testing class name : TestTextNodeToParentHtmlNode"
                )
                print("Test Failed")
                print("expected :")
                print(test_case["expected"])
                print("actual :")
                print(actual)
                self.fail("Test failed for text_node_to_parent_Html_node.")


class TestMarkdownToHtmlNode(unittest.TestCase):
    test_cases = [
        {
            "input": """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

        """,
            "expected": "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
```This is **bolded** paragraph
text in a p
tag here```

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><code>This is <b>bolded</b> paragraph text in a p tag here</code><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
# This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><h1>This is <b>bolded</b> paragraph text in a p tag here</h1><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
## This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><h2>This is <b>bolded</b> paragraph text in a p tag here</h2><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><h3>This is <b>bolded</b> paragraph text in a p tag here</h3><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
#### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><h4>This is <b>bolded</b> paragraph text in a p tag here</h4><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
##### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><h5>This is <b>bolded</b> paragraph text in a p tag here</h5><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
###### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><h6>This is <b>bolded</b> paragraph text in a p tag here</h6><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
####### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><p>####### This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
- apple
- bannana
- orange

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><ul><li>apple</li><li>bannana</li><li>orange</li></ul><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """
1. apple
2. bannana
3. orange

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><ol><li>apple</li><li>bannana</li><li>orange</li></ol><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """

This is text with an [anchor](https://i.imgur.com/zjjcJKZ.png)

###### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><p>This is text with an <a href='https://i.imgur.com/zjjcJKZ.png'>anchor</a></p><h6>This is <b>bolded</b> paragraph text in a p tag here</h6><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
        {
            "input": """

This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)

###### This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""",
            "expected": "<div><p>This is text with an <img src='https://i.imgur.com/zjjcJKZ.png' alt='image'></img></p><h6>This is <b>bolded</b> paragraph text in a p tag here</h6><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        },
    ]

    def test_output(self):
        for test_case in TestMarkdownToHtmlNode.test_cases:
            actual = markdown_to_html_node(test_case["input"]).to_html()
            if "print" in test_case:
                print(test_case["print"])
            try:
                self.assertEqual(actual, test_case["expected"])
            except Exception as _:
                print(
                    "Error happened while testing Markdown To HTML Node.\n Function name : markdown_to_html_node \n Testing class name :TestMarkdownToHtmlNode "
                )
                print("Test Failed")
                print("expected :")
                print(test_case["expected"])
                print("actual :")
                print(actual)
                self.fail("Test failed for text_node_to_parent_Html_node.")
