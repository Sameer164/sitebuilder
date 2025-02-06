from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case(TextType.NORMAL_TEXT):
            return LeafNode(tag=None, value=text_node.text)
        case (TextType.BOLD_TEXT):
            return LeafNode(tag='b', value=text_node.text)
        case (TextType.ITALIC_TEXT):
            return LeafNode(tag='i', value=text_node.text)
        case (TextType.CODE_TEXT):
            return LeafNode(tag='code', value=text_node.text)
        case (TextType.LINKS):
            return LeafNode(tag='a', value=text_node.text, props={"href": text_node.url})
        case (TextType.IMAGES):
            return LeafNode(tag='img', value="", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Text Type is not recognizable")


def main():
    t = TextNode("Hello", TextType.BOLD_TEXT, 'https://')
    print(t)

if __name__ == "__main__":
    main()