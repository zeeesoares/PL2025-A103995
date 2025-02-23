import re

def subBold(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", texto) 

def subItalic(texto):
    return re.sub(r"\*(.*?)\*", r"<i>\1</i>", texto) 

def subImage(texto):
    return re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img src="\2" alt="\1">', texto)  

def subLink(texto):
    return re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', texto)  

def tokenize(texto):
    return texto.split("\n")  

def parse(lines):
    parsed = []
    in_olist = False  
    in_ulist = False
    list_items = [] 

    for line in lines:
        line = line.strip()  

        if not line:  
            continue 
        
        match = re.match(r"^(#{1,6})\s+(.*)", line)
        if match:
            level = len(match.group(1))  
            parsed.append({"type": "header", "level": level, "content": match.group(2)})
            continue

        match = re.match(r"^\d+\.\s+(.*)", line)
        if match:
            if not in_olist:
                in_olist = "ol"
                list_items = []
            list_items.append(match.group(1))
            continue

        match = re.match(r"^[-*]\s+(.*)", line)
        if match:
            if not in_ulist:
                in_ulist = "ul"
                list_items = []
            list_items.append(match.group(1))
            continue
        
        if in_olist:
            parsed.append({"type": in_olist, "items": list_items})
            in_olist = False 

        if in_ulist:
            parsed.append({"type": in_ulist, "items": list_items})
            in_ulist = False 

        line = subBold(line)

        line = subItalic(line)

        line = subImage(line)

        line = subLink(line)

        parsed.append({"type": "text", "content": line})

    if in_olist:
            parsed.append({"type": in_olist, "items": list_items})
            in_olist = False 

    if in_ulist:
        parsed.append({"type": in_ulist, "items": list_items})
        in_ulist = False 

    return parsed


def semantic_analysis(parsed_tokens):
    html_content = ""

    for token in parsed_tokens:
        if token["type"] == "header":
            html_content += f"<h{token['level']}>{token['content']}</h{token['level']}>\n\n"
        elif token["type"] == "text":
            html_content += f"<p>{token['content']}</p>\n\n"
        elif token["type"] in ["ul", "ol"]:
            tag = token["type"]
            html_content += f"<{tag}>\n"
            for item in token["items"]:
                html_content += f"  <li>{item}</li>\n"
            html_content += f"</{tag}>\n\n"

    return html_content


def process_markdown_to_html(input_filename, output_filename):

    with open(input_filename, "r", encoding="utf-8") as f:
        content = f.read()

    lines = tokenize(content)  
    parsed_tokens = parse(lines) 
    html_content = semantic_analysis(parsed_tokens) 
    
    with open(output_filename, "w", encoding="utf-8") as rf:
        rf.write(html_content)


if __name__ == "__main__":
    process_markdown_to_html("in.md", "result.html")
