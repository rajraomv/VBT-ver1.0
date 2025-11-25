from fetcher import parse_sections

def test_parsing():
    description1 = """
    Here is a video about Python.
    
    00:00 Intro
    01:30 Setup
    05:45 Writing Code
    10:00 Conclusion
    """
    
    description2 = """
    No timestamps here.
    """
    
    description3 = """
    Timestamps with dashes:
    0:00 - Start
    2:15 - Middle part
    """

    print("--- Test 1: Standard ---")
    sections = parse_sections(description1)
    for s in sections:
        print(s)
        
    print("\n--- Test 2: None ---")
    sections = parse_sections(description2)
    for s in sections:
        print(s)

    print("\n--- Test 3: Dashes ---")
    sections = parse_sections(description3)
    for s in sections:
        print(s)

if __name__ == "__main__":
    test_parsing()
