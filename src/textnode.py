from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = 1
    BOLD_TEXT = 2
    ITALIC_TEXT = 3
    CODE_TEXT = 4
    LINKS = 5
    IMAGES = 6

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_node):
        return self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url
    
    # This function is called when we call print(obj) if there is no __str__ or when we call __repr__
    # It doesn't go the other way though - we can't call repr() when there is only __str__, we can call str() when there is only __repr__
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"

