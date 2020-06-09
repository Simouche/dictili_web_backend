def trim_text_to_90chars(text: str) -> list:
    words = text.split()
    a_line = ""
    lines = []
    for word in words:
        if (len(a_line) + len(word)) < 90:
            a_line += " " + word
        else:
            lines.append(a_line)
            a_line = ""
    lines.append(a_line)
    return lines
