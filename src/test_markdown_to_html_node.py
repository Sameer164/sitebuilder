import unittest
from parentnode import ParentNode
from leafnode import LeafNode
from main import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_eq_just_heading(self):
        markdown = "## Hello"
        expected_html = "<div><h2>Hello</h2></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)
    
    def test_quote(self):
        markdown = "> All that is gold does not glitter"
        expected_html = "<div><blockquote>All that is gold does not glitter</blockquote></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)
    
    def test_code(self):
        markdown = '```\nfunc main(){\n    fmt.Println("Hello, World!")\n}\n```'
        expected_html = '<div><pre><code>\nfunc main(){\n    fmt.Println("Hello, World!")\n}\n</code></pre></div>'
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)