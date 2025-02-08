import re, os, shutil
from pathlib import Path
from textnode import TextNode, TextType
from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    mds_and_dirs = os.listdir(dir_path_content)
    for entry in mds_and_dirs:
        if os.path.isfile(os.path.join(dir_path_content, entry)):
            generate_page(os.path.join(dir_path_content, entry), template_path, os.path.join(dest_dir_path, "index.html"))
        else:
            generate_pages_recursive(os.path.join(dir_path_content, entry), template_path, os.path.join(dest_dir_path, entry))
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_node = markdown_to_html_node(markdown)

    html = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(exist_ok=True, parents=True)
    f = open(dest_path, "w+")
    f.write(template)
    f.close()


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith('# '):
            return line[2:].lstrip().rstrip()
    return  ""


def copy_all(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        raise NotADirectoryError()

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    
    file_and_dirs = os.listdir(src_dir)
    for entry in file_and_dirs:
        if os.path.isfile(os.path.join(src_dir, entry)):
            print(f"copying {os.path.join(src_dir, entry)} to {dest_dir}")
            shutil.copy(os.path.join(src_dir, entry), dest_dir)
        else:
            copy_all(os.path.join(src_dir, entry), os.path.join(dest_dir, entry))
    


def create_heading(block):
    tag_level = len(block.split(" ")[0])
    tag = f"h{tag_level}"
    node = ParentNode(tag=tag, children=[], props=None)
    text = " ".join(block.split(" ")[1:])
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    node.children = html_nodes
    return node

def create_code(block):
    pre_tag = "pre"
    code_tag = "code"
    code_node = ParentNode(tag=code_tag, children=[], props=None)
    pre_node = ParentNode(tag=pre_tag, children=[code_node], props=None)
    text = block[3:-3]
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    code_node.children = html_nodes
    return pre_node

def create_quote(block):
    tag = "blockquote"
    node = ParentNode(tag=tag, children=[], props=None)
    text = block[1:].lstrip().rstrip()
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    node.children = html_nodes
    return node

def create_unordered_list(block):
    top_tag = "ul"
    top_node = ParentNode(tag=top_tag, children = [], props = None)
    lines = block.split('\n')
    for line in lines:
        node = ParentNode(tag = "li", children = [], props=None)
        text = line[2:]
        text_nodes = text_to_textnodes(text)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        node.children = html_nodes
        top_node.children.append(node)
    return top_node

def create_ordered_list(block):
    top_tag = "ol"
    top_node = ParentNode(tag=top_tag, children = [], props = None)
    lines = block.split('\n')
    for line in lines:
        node = ParentNode(tag = "li", children = [], props=None)
        text = line[3:]
        text_nodes = text_to_textnodes(text)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        node.children = html_nodes
        top_node.children.append(node)
    return top_node

def create_paragraph(block):
    top_tag = "p"
    top_node = ParentNode(tag=top_tag, children = [], props = None)
    text = block
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    top_node.children = html_nodes
    return top_node






def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    types = [block_to_block_type(block) for block in blocks]
    html_nodes = []
    for i in range(len(blocks)):
        block, type = blocks[i], types[i]
        match type:
            case "heading":
                html_nodes.append(create_heading(block))
            case "code":
                html_nodes.append(create_code(block))
            case "quote":
                html_nodes.append(create_quote(block))
            case "unordered_list":
                html_nodes.append(create_unordered_list(block))
            case "ordered_list":
                html_nodes.append(create_ordered_list(block))
            case "paragraph":
                html_nodes.append(create_paragraph(block))
            case _:
                pass
    top_tag = "div"
    return ParentNode(tag=top_tag, children=html_nodes, props=None)



def block_to_block_type(block):

    def is_ordered_list(block):
        lines = block.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return False
        return True

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif block.startswith(">"):
        return "quote"
    elif block.startswith(("* ", "- ")):
        return "unordered_list"
    elif is_ordered_list(block):
        return "ordered_list"
    else:
        return "paragraph"


def markdown_to_blocks(markdown):
    return list(filter(lambda x: x,  map(lambda x: x.lstrip().rstrip(), markdown.split("\n\n"))))

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
                i += 1
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
    shutil.rmtree(os.path.abspath('./public'))
    copy_all(os.path.abspath('./static'), os.path.abspath('./public'))
    generate_pages_recursive(os.path.abspath('./content/'), os.path.join('./template.html'), os.path.abspath('./public/'))

if __name__ == "__main__":
    main()