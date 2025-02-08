from functools import reduce
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Missing Tag. Tag is Required.")
        if not self.children:
            raise ValueError("No Children. There must be atleast one children.")

        def aggregator(agg, curr):
            agg += curr.to_html()
            return agg
        
        inner_html = reduce(aggregator, self.children, "")

        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"




