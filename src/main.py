from textnode import text_node_to_html_node
from textnode import TextNode, TextType


def main():
    test = TextNode(
        "This is just a dummy text.",
        TextType.LINK,
        "https://github.com/Shaheryarkhalid",
    )
    print(test)


if __name__ == "__main__":
    main()
