import re
from textnode import TextNode, TextType
from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode

def text_to_textnodes(text):
    delimiters = [("`", TextType.CODE_TEXT), ("**", TextType.BOLD_TEXT), ("*", TextType.ITALIC_TEXT)]
    node = [TextNode(text, TextType.NORMAL_TEXT)]
    for delimiter in delimiters:
        node = split_nodes_delimiter(node, delimiter[0], delimiter[1])
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node

def split_nodes_image(old_nodes):
    new_nodes = []
    splitted = True
    while splitted:
        splitted = False
        for node in old_nodes:
            if node.text_type != TextType.NORMAL_TEXT:
                new_nodes.append(node)
                continue

            matches = extract_markdown_images(node.text)
            
            if matches:
                splitted = True
                alt_text, img_url = matches.pop()
                splitted_text = node.text.split(f"![{alt_text}]({img_url})", 1)
                # Since we are splitting on a matched string, we are guaranteed that we have two elements in the array. 
                if splitted_text[0]:
                    new_nodes.append(TextNode(splitted_text[0], TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGES, img_url))
                if splitted_text[1]:
                    new_nodes.append(TextNode(splitted_text[1], TextType.NORMAL_TEXT))
            else:
                new_nodes.append(node)
        old_nodes = new_nodes
        new_nodes = []

    return old_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    splitted = True
    while splitted:
        splitted = False
        for node in old_nodes:
            if node.text_type != TextType.NORMAL_TEXT:
                new_nodes.append(node)
                continue

            matches = extract_markdown_links(node.text)
            
            if matches:
                splitted = True
                alt_text, img_url = matches.pop()
                splitted_text = node.text.split(f"[{alt_text}]({img_url})", 1)
                # Since we are splitting on a matched string, we are guaranteed that we have two elements in the array. 
                if splitted_text[0]:
                    new_nodes.append(TextNode(splitted_text[0], TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINKS, img_url))
                if splitted_text[1]:
                    new_nodes.append(TextNode(splitted_text[1], TextType.NORMAL_TEXT))
            else:
                new_nodes.append(node)
        old_nodes = new_nodes
        new_nodes = []

    return old_nodes



def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    matches = re.findall(r"[^!](\[(.*?)\]\((.*?)\))", text)
    if not matches: return []
    return list(map(lambda x: tuple((x[1], x[2])), matches))

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

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
    # print(extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))

    # node = TextNode(
    #         "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
    #         TextType.NORMAL_TEXT,
    #     )
    
    # print(split_nodes_image([node]))
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))




if __name__ == "__main__":
    main()