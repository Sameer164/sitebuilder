from textnode import TextNode, TextType

def main():
    t = TextNode("Hello", TextType.BOLD_TEXT, 'https://')
    print(t)

if __name__ == "__main__":
    main()