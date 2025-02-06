import unittest
from main import extract_markdown_images, extract_markdown_links

class TestExtractImagesAndLinks(unittest.TestCase):
    def test_twoimage_eq(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_no_image(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_just_sq_bracket(self):
        text = "This is text with a ![rick roll]"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_empty_alt_and_text(self):
        text = "This is text with a ![]()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_twolinks_eq(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_no_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_just_sq_bracket(self):
        text = "This is text with a [rick roll]"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_empty_alt_and_text(self):
        text = "This is text with a []()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_links(text), expected)



if __name__== "__main__":
    unittest.main()