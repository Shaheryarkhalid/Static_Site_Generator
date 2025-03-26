import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_link_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://lnode")
        node2 = TextNode("This is a text node", TextType.LINK, "https://lnode")
        self.assertEqual(node, node2)

    def test_not_eq_link_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://lnode")
        node2 = TextNode("This is a text node", TextType.LINK, "https://lnode")
        self.assertNotEqual(node, node2)

    def test_eq_texttype(self):
        node = TextNode("This is a text node", TextType.LINK, "https://lnode")
        node2 = TextNode("This is a text node", TextType.LINK, "https://lnode")
        self.assertEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.LINK, "https://lnode")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://lnode")
        self.assertNotEqual(node, node2)


class TestFunctionTextNodeToHtml(unittest.TestCase):

    def test_with_just_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_with_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_with_italic_text(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_with_code_text(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_with_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://link.in")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://link.in")
        self.assertEqual(html_node.value, "This is a link text node")

    def test_with_image(self):
        node = TextNode("This is a image text node", TextType.IMAGE, "https://link.in")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "This is a image text node")
        self.assertEqual(html_node.props["src"], "https://link.in")

    def test_with_quotes_text(self):
        node = TextNode("This is a Quotes text node", TextType.QUOTES)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "q")
        self.assertEqual(html_node.value, "This is a Quotes text node")


if __name__ == "__main__":
    unittest.main()
