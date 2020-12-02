import template
from main import burpconverter


def codeblock(code, title):
    return template.bold_start + title + template.bold_end +\
           "\n\n" +\
           template.code_start + code + template.code_end

def create_request(request, title="Request:"):
    return codeblock(burpconverter.request_to_readable(request), title)

def create_response(response, title="Request:"):
    return codeblock(burpconverter.response_to_readable(response), title)

def highlight_line(code, highlight):
    output = ''
    for line in code.split("\n"):
        if highlight in line:
            output += template.highlight_start + line + template.highlight_end + "\n"
        else:
            output += line + "\n"
    return output

def highlight_word(code, highlight):
    return code.replace(highlight, template.highlight_start + highlight + template.highlight_end)

def highlight_ifall_inline(code, highlight):
    output = ""
    for line in code:
        if all(parts in line for parts in highlight):
            output = template.highlight_start + line + template.highlight_end + "\n"
        else:
            output = line + "\n"
    return output

#ToDo: remove empty lines between header and body
def create_both(request, response, highlightline=[""], highlightword=[""], reqtitle="Request:", resptitle="Response:"):
    tmp = create_request(request, reqtitle) + create_response(response, resptitle)
    if (not highlightword == [""]):
        for ele in highlightword:
            tmp = highlight_word(tmp, ele)
    if (not highlightline == [""]):
        for ele in highlightline:
            tmp = highlight_line(tmp, ele)
    return tmp
