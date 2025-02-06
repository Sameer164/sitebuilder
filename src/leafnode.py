from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if not (self.tag and self.value):
            raise ValueError()
        prop_html = ""
        if self.props:
            prop_html = self.props_to_html()
        return f"<{self.tag}{prop_html}>{self.value}</{self.tag}>"

    
