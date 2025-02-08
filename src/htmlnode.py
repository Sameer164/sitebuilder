from functools import reduce
"""
Perhaps counterintuitively, every data member should be optional and default to None:
An HTMLNode without a tag will just render as raw text
An HTMLNode without a value will be assumed to have children
An HTMLNode without children will be assumed to have a value
An HTMLNode without props simply won't have any attributes
"""

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props: return ""
        def aggregator(agg, curr):
            agg += f' {curr[0]}="{curr[1]}"'
            return agg
        return reduce(aggregator, self.props.items(), "")
    
    def __repr__(self):
        return f'Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props_to_html()}'

    

        
