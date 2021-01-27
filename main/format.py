import template
from main import burpconverter


def codeblock(code, title):
    return template.bold_start + title + template.bold_end +\
           "\n\n" +\
           template.code_start + code + template.code_end

def highlighting(text, highlightline=[""], highlightword=[""]):
    tmp = text
    if (not highlightword == [""]):
        for ele in highlightword:
            tmp = highlight_word(tmp, ele)
    if (not highlightline == [""]):
        for ele in highlightline:
            tmp = highlight_line(tmp, ele)
    #check for doubled marks
    tmp = remove_doubled_highlight(tmp)
    return tmp

def create_request(request, title="Request:", highlightline=[""], highlightword=[""]):
    tmp = burpconverter.request_to_readable(request)
    tmp = highlighting(tmp, highlightline, highlightword)
    return codeblock(tmp, title)

def create_response(response, title="Request:", highlightline=[""], highlightword=[""]):
    tmp = burpconverter.response_to_readable(response)
    tmp = highlighting(tmp, highlightline, highlightword)
    return codeblock(tmp, title)

def highlight_line(code, highlight):
    #ToDo: change to joinsep
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

def remove_doubled_highlight(text):
    tmp1 = text
    tmp2 = text.replace(template.highlight_start + template.highlight_start, template.highlight_start)
    tmp2 = text.replace(template.highlight_end + template.highlight_end, template.highlight_end)

    while (tmp1 != tmp2):
        tmp1 = tmp2
        tmp2 = tmp1.replace(template.highlight_start+template.highlight_start, template.highlight_start)
        tmp2 = tmp1.replace(template.highlight_end + template.highlight_end, template.highlight_end)

    return tmp2

#ToDo: remove empty lines between header and body
def create_both(request, response, highlightline=[""], highlightword=[""], reqtitle="Request:", resptitle="Response:"):
    return create_request(request, reqtitle, highlightline, highlightword) +\
           create_response(response, resptitle, highlightline, highlightword)
