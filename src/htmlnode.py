class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # return ""
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_text = ""
        for key, value in self.props.items():
            html_text += f' {key}="{value}"'
        return html_text

    def __eq__(self, htmlnode):
        if (
            self.tag == htmlnode.tag
            and self.value == htmlnode.value
            and self.children == htmlnode.children
            and self.props == htmlnode.props
        ):
            return True
        return False

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag not provided")
        if not self.children:
            raise ValueError("children must be provided")
        value = ""
        for child in self.children:
            value += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"
