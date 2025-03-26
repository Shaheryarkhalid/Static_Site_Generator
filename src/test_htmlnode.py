import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):

    def test_HTMLNode_initialize(self):
        new_html_node = HTMLNode()
        self.assertTrue(str(new_html_node).__contains__("HTMLNode"))

    def test_HTMLNode_contains_provided_tag(self):
        new_html_node = HTMLNode(tag="h1")
        self.assertTrue(str(new_html_node).__contains__("tag=h1"))

    def test_HTMLNode_contains_provided_value(self):
        new_html_node = HTMLNode(value="Test HTMLNode Heading")
        self.assertTrue(str(new_html_node).__contains__("value=Test HTMLNode Heading"))

    def test_HTMLNode_contains_provided_children(self):
        child_html_node = HTMLNode("b", "Heading")
        new_html_node = HTMLNode("p", "Test HTMLNode", child_html_node)
        self.assertTrue("children=HTMLNode(tag=b, value=Heading" in str(new_html_node))

    def test_HTMLNode_contains_provided_props(self):
        child_html_node = HTMLNode("b", "Heading")
        new_html_node = HTMLNode(
            "p", "Test HTMLNode", child_html_node, {"href": "https://link.in"}
        )
        self.assertTrue("props={'href': 'https://link.in'}" in str(new_html_node))

    def test_HTMLNode_to_html_method(self):
        child_html_node = HTMLNode("b", "Heading")
        new_html_node = HTMLNode(
            "p", "Test HTMLNode", child_html_node, {"href": "https://link.in"}
        )
        try:
            new_html_node.to_html()

        except Exception as e:
            self.assertIsInstance(e, NotImplementedError)
        else:
            self.fail("Exception expected from to_html() method.")

    def test_HTMLNode_props_to_html_method(self):
        child_html_node = HTMLNode("b", "Heading")
        new_html_node = HTMLNode(
            "h1", "HTMLNode ", child_html_node, {"href": "https://link.in"}
        )
        self.assertEqual(new_html_node.props_to_html(), ' href="https://link.in"')


class TestLeafNode(unittest.TestCase):

    def test_leaf_Exception(self):
        try:
            node = LeafNode("p", None)
            node.to_html()
        except Exception as e:
            self.assertIsInstance(e, ValueError)
        else:
            self.fail("ValueError expected but no exception was thrown.")

    def test_leaf_without_tag(self):
        node = LeafNode(None, "Hello World")
        returned_value = node.to_html()
        self.assertEqual(returned_value, "Hello World")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):

    def test_parent_node_tohtml(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node.to_html(), expected_result)

    def test_to_html_without_tag(self):
        try:
            node = ParentNode(
                None,
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            node.to_html()
        except Exception as e:
            self.assertIsInstance(e, ValueError)
            self.assertEqual(str(e), "tag not provided")
        else:
            self.fail(
                "Exception should have been thrown. As this function is trying to access ParentNode without tag."
            )

    def test_to_html_without_children(self):
        try:
            node = ParentNode(
                "p",
                [],
            )
            node.to_html()
        except Exception as e:
            self.assertIsInstance(e, ValueError)
            self.assertEqual(str(e), "children must be provided")
        else:
            self.fail(
                "Exception should have been thrown. As this function is trying to access ParentNode without children."
            )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_nested_children(self):
        child_node1 = LeafNode("bold", "child : 1")
        nested_parent_node1 = ParentNode("p", [child_node1])
        child_node2 = LeafNode("span", "child : 2")
        nested_parent_node2 = ParentNode("p", [child_node2])
        child_node3 = LeafNode("span", "child : 3")
        parent_node = ParentNode(
            "div", [nested_parent_node1, nested_parent_node2, child_node3]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><bold>child : 1</bold></p><p><span>child : 2</span></p><span>child : 3</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
