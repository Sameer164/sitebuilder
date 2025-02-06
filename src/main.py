import re
from textnode import TextNode, TextType
from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    matches = re.findall(r"[^!](\[(.*?)\]\((.*?)\))", text)
    if not matches: return []
    return list(map(lambda x: tuple((x[1], x[2])), matches))

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        splitted_text = node.text.split(delimiter)
        if not len(splitted_text) % 2:
            raise ValueError("invalid markdown, formatted section not closed")
        i = 0
        while i < len(splitted_text):
            if splitted_text[i] == "":
                continue
            new_node = TextNode(text=splitted_text[i], text_type=text_type if i % 2 else node.text_type)
            new_nodes.append(new_node)
            i += 1
    return new_nodes

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
    print(extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))

if __name__ == "__main__":
    main()