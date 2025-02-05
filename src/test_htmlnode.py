import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_toHtml(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)
    
    def test_propsToHtml(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_repr(self):
        node = HTMLNode(tag = "a", value = "Google Link", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        expected_str = 'Tag: a\nValue: Google Link\nChildren: None\nProps:  href="https://www.google.com" target="_blank"'
        self.assertEqual(str(node), expected_str)
    

