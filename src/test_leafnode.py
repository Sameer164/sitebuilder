import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        paragraph = LeafNode(tag="p", value="This is a paragraph of text.")
        link = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})

        self.assertEqual(paragraph.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(link.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
if __name__ == "__main__":
    unittest.main()
