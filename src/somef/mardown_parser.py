import markdown
import re
import pandas as pd
from . import regular_expressions

def extract_headers(original_text):
    text, bashes = extract_bash(original_text)
    html_text = markdown.markdown(text)
    splitted = html_text.split("\n")
    index = 0
    limit = len(splitted)
    output = {}
    regex = r'<[^<>]+>'
    while index < limit:
        line = splitted[index]
        if line.startswith("<h"):
            if is_header(line):
                #text = re.sub(regex, '', line)
                text = get_tag_content(line)
                if index + 1 >= limit:
                    output[text] = True
                elif not splitted[index + 1].startswith("<h"):
                    output[text] = True
                else:
                    output[text] = False
        index += 1
    return output


def extract_headers_with_tags(original_text):
    text, bashes = extract_bash(original_text)
    html_text = markdown.markdown(text)
    splitted = html_text.split("\n")
    index = 0
    limit = len(splitted)
    output = []
    while index < limit:
        line = splitted[index]
        if line.startswith("<h"):
            if is_header(line):
                output.append(replace_html_tags(line))
        index += 1
    return output


def extract_content_per_header(original_text, headers):
    keys = list(headers.keys())
    content = []
    output = {}
    limit = len(keys)
    index = 0
    top = keys[0]
    bottom = None
    none_header_content = None
    text_tokenized = original_text.split('\n')
    if len(text_tokenized) == 1:
        return text_tokenized[0]
    top_index = get_position(0, text_tokenized, top)
    # si hay algo antes de la primera cabecera, no se procesa porque no está relacionado con ninguna cabecera
    if top_index > 0:
        none_header_content = get_text(0, top_index, text_tokenized)
        none_header_content = regular_expressions.remove_links_images(none_header_content)
        none_header_content = regular_expressions.remove_html_tags(none_header_content)
        #print(none_header_content)
    offset = 1
    if not text_tokenized[top_index].startswith('#'):
        offset = 2
    while index < limit:
        index += 1
        if index < limit:
            bottom = keys[index]
            bottom_index = get_position(top_index, text_tokenized, bottom)
            if headers[top]:
                header_content = get_text(top_index + offset, bottom_index, text_tokenized)
                if header_content.startswith('\n'):
                    header_content = header_content[1:]
                content.append(header_content)
                output[top] = header_content
            top = bottom
            top_index = bottom_index

    header_content = get_text(top_index + offset, -1, text_tokenized)
    if header_content.startswith('\n'):
        header_content = header_content[1:]
    content.append(header_content)
    output[top] = header_content
    return content, none_header_content


def get_position(init_index, text_tokenized, text):
    while init_index < len(text_tokenized):
        val = text_tokenized[init_index]
        val = remove_hash(val).strip()
        if val.startswith(text):
            return init_index
        init_index += 1
    return -1


def remove_hash(text):
    """Removes hash from a given text"""
    while text.startswith("#"):
        text = text[1:]
    return text


def get_text(init_index, end_index, text_tokenized):
    if end_index == -1:
        end_index = len(text_tokenized)

    output = text_tokenized[init_index]
    init_index += 1
    while init_index < end_index:
        output = output + '\n' + text_tokenized[init_index]
        init_index += 1
    return output


def extract_bash(text):
    output = {}
    index = 1
    while text.find('```')!= -1:
        init = text.find('```')
        end = text.find('```',init+3)
        if end == -1:
            break
        bash_text = text[init:end+3]
        text = text.replace(bash_text, "BASH"+str(index)+"*")
        output["BASH"+str(index)+"*"] = bash_text
        index += 1
    return text, output


def extract_blocks_excerpts(header_content):
    output = []
    for block_text in header_content:
        text_mod, bashes = extract_bash(block_text)
        block_pieces = text_mod.split("\n\n")
        p_block = False
        p_text = []
        b_block = False
        b_text = []
        limit = len(block_pieces)
        index = 0
        # for piece in block_pieces:
        while index < limit:
            piece = block_pieces[index]
            if piece.startswith('<') or piece.startswith('['):
                if p_block:
                    output.append(join_elements(p_text))
                    p_text.clear()
                    p_block = False
                if b_block:
                    output.append(join_elements(b_text))
                    b_text.clear()
                    b_block = False
                output.append(piece)
            elif piece.find('BASH') != -1:
                if p_block:
                    output.append(join_elements(p_text))
                    p_text.clear()
                    p_block = False
                index_bash = piece.find('BASH')
                key = retrieve_bash_key(piece, index_bash)
                if key != '':
                    piece = piece.replace(key, bashes[key])
                    if index + 1 < limit and block_pieces[index + 1].startswith("BASH"):
                        b_text.append(piece)
                        b_block = True
                    elif b_block:
                        b_text.append(piece)
                        output.append(join_elements(b_text))
                        b_text.clear()
                        b_block = False
                    else:
                        output.append(piece)
            else:
                if len(piece) > 0:
                    if b_block:
                        output.append(join_elements(b_text))
                        b_text.clear()
                        b_block = False
                    if index + 1 < limit and block_pieces[index + 1].startswith("BASH"):
                        bash_piece = block_pieces[index + 1]
                        key = retrieve_bash_key(bash_piece, 0)
                        bash_piece = bash_piece.replace(key, bashes[key])
                        p_text.append(piece)
                        p_text.append(bash_piece)
                        p_block = True
                        index += 1
                    else:
                        if p_block:
                            output.append(join_elements(p_text))
                            p_text.clear()
                            p_block = False
                        output.append(piece)
                else:
                    if p_block:
                        output.append(join_elements(p_text))
                        p_text.clear()
                        p_block = False
                    if b_block:
                        output.append(join_elements(b_text))
                        b_text.clear()
                        b_block = False
            index += 1
        if p_block:
            output.append(join_elements(p_text))
            p_text.clear()
            p_block = False
        if b_block:
            output.append(join_elements(b_text))
            b_text.clear()
            b_block = False

    return output


def retrieve_bash_key(bash_piece, index_bash):
    #if bash_piece.find('\n', index_bash) != -1:
    #    key = bash_piece[index_bash:bash_piece.find('\n', index_bash)]
    #else:
    #    key = bash_piece[index_bash:]
    key = bash_piece[index_bash:bash_piece.find('*')+1]
    return key


def join_elements(p_text):
    output = ''
    for text in p_text:
        if not text.endswith('\n'):
            output = output + text + '\n'
        else:
            output = output + text

    return output


def extract_text_excerpts_header(original_text):
    headers = extract_headers(original_text)
    keys = list(headers.keys())
    content = []
    output = {}
    limit = len(keys)
    index = 0
    if limit > 0:
        top = keys[0]
        bottom = None
        text_tokenized = original_text.split('\n')
        if len(text_tokenized) == 1:
            output[top] = text_tokenized[0]
            return process_blocks_header(output)
        top_index = get_position(0, text_tokenized, top)
        offset = 1
        if not text_tokenized[top_index].startswith('#'):
            offset = 2
        while index < limit:
            index += 1
            if index < limit:
                bottom = keys[index]
                bottom_index = get_position(top_index, text_tokenized, bottom)
                if headers[top]:
                    header_content = get_text(top_index + offset, bottom_index, text_tokenized)
                    if header_content.startswith('\n'):
                        header_content = header_content[1:]
                    content.append(header_content)
                    output[top] = header_content
                # else:
                    # print('No se procesa-->' + top)
                top = bottom
                top_index = bottom_index

        header_content = get_text(top_index + offset, -1, text_tokenized)
        if header_content.startswith('\n'):
            header_content = header_content[1:]
        content.append(header_content)
        output[top] = header_content
    return process_blocks_header(output)


def process_blocks_header(headers_content):
    output = {}
    df = pd.DataFrame(columns=['text', 'header'])
    for header in headers_content:
        block_text = headers_content[header]
        text_mod, bashes = extract_bash(block_text)
        block_pieces = text_mod.split("\n\n")
        p_block = False
        p_text = []
        b_block = False
        b_text = []
        limit = len(block_pieces)
        index = 0
        # for piece in block_pieces:
        while index < limit:
            piece = block_pieces[index]
            if piece.startswith('<') or piece.startswith('['):
                if p_block:
                    s_row = pd.Series([join_elements(p_text), header], index=df.columns)
                    df = df.append(s_row, ignore_index=True)
                    p_text.clear()
                    p_block = False
                if b_block:
                    s_row = pd.Series([join_elements(b_text), header], index=df.columns)
                    df = df.append(s_row, ignore_index=True)
                    b_text.clear()
                    b_block = False
                s_row = pd.Series([piece, header], index=df.columns)
                df = df.append(s_row, ignore_index=True)
            elif piece.find('BASH') != -1:
                if p_block:
                    s_row = pd.Series([join_elements(p_text), header], index=df.columns)
                    df = df.append(s_row, ignore_index=True)
                    p_text.clear()
                    p_block = False
                index_bash = piece.find('BASH')
                key = retrieve_bash_key(piece, index_bash)
                if key !='':
                    piece = piece.replace(key, bashes[key])
                    if index + 1 < limit and block_pieces[index + 1].startswith("BASH"):
                        b_text.append(piece)
                        b_block = True
                    elif b_block:
                        b_text.append(piece)
                        s_row = pd.Series([join_elements(b_text), header], index=df.columns)
                        df = df.append(s_row, ignore_index=True)
                        b_text.clear()
                        b_block = False
                    else:
                        s_row = pd.Series([piece, header], index=df.columns)
                        df = df.append(s_row, ignore_index=True)
            else:
                if len(piece) > 0:
                    if b_block:
                        s_row = pd.Series([join_elements(b_text), header], index=df.columns)
                        df = df.append(s_row, ignore_index=True)
                        b_text.clear()
                        b_block = False
                    if index + 1 < limit and block_pieces[index + 1].startswith("BASH"):
                        bash_piece = block_pieces[index + 1]
                        key = retrieve_bash_key(bash_piece, 0)
                        bash_piece = bash_piece.replace(key, bashes[key])
                        p_text.append(piece)
                        p_text.append(bash_piece)
                        p_block = True
                        index += 1
                    else:
                        if p_block:
                            s_row = pd.Series([join_elements(p_text), header], index=df.columns)
                            df = df.append(s_row, ignore_index=True)
                            p_text.clear()
                            p_block = False
                        s_row = pd.Series([piece, header], index=df.columns)
                        df = df.append(s_row, ignore_index=True)
                else:
                    if p_block:
                        s_row = pd.Series([join_elements(p_text), header], index=df.columns)
                        df = df.append(s_row, ignore_index=True)
                        p_text.clear()
                        p_block = False
                    if b_block:
                        s_row = pd.Series([join_elements(b_text), header], index=df.columns)
                        df = df.append(s_row, ignore_index=True)
                        b_text.clear()
                        b_block = False
            index += 1
        if p_block:
            s_row = pd.Series([join_elements(p_text), header], index=df.columns)
            df = df.append(s_row, ignore_index=True)
            p_text.clear()
            p_block = False
        if b_block:
            s_row = pd.Series([join_elements(b_text), header], index=df.columns)
            df = df.append(s_row, ignore_index=True)
            b_text.clear()
            b_block = False
    return df


def extract_headers_parents(original_text):
    headers = extract_headers_with_tags(original_text)
    output = {}
    parents = []
    parent = ""
    test = []
    for header in headers:
        parent, parents = update_parents(header, parents)
        output[header] = parents
        parents.append(header)

    return remove_tags_new(output)


def remove_tags(header_parents):
    output = {}
    regex = r'<[^<>]+>'
    for key in header_parents.keys():
        value = header_parents[key]
        new_key = re.sub(regex, '', key)
        new_value = re.sub(regex, '', value)
        output[new_key] = new_value

    return

def remove_tags_new(header_parents):
    output = {}
    regex = r'<[^<>]+>'
    for key in header_parents.keys():
        #new_key = re.sub(regex, '', key)
        new_key = key[4:len(key)-5]
        new_list = []
        for value in header_parents[key]:
            if key != value:
                #new_value = re.sub(regex, '', value)
                new_value = value[4:len(value)-5]
                new_list.append(new_value)
        output[new_key] = new_list

    return output


def update_parents(new_header, parents):
    parent = ""
    parent_list = []
    try:
        for p in parents:
            if minor_than(new_header, p):
                parent_list.append(p)
                parent = p
            else:
                return parent, parent_list
    except ValueError:
        print("Error when retrieving the parent header list")

    return parent, parent_list


def minor_than(second, first):
    if first == "":
        return False
    return int(second[2]) > int(first[2])


def is_header(header):
    if (header.startswith('<h1') or header.startswith('<h2') or header.startswith('<h3')
        or header.startswith('<h4') or header.startswith('<h5') or header.startswith('<h6')) \
            and header.find('</h') > 0:
        return True
    else:
        return False


def get_tag_content(header):
    init = header.index(">")
    end = header.rindex("</h")
    return replace_html_tags(header[init+1:end])


def replace_html_tags(text):
    text = text.replace("<i>","*").replace("</i>","*")
    text = text.replace("<em>","*").replace("</em>","*")
    text = text.replace("<b>", "**").replace("</b>", "**")
    text = text.replace("<strong>", "**").replace("</strong>", "**")
    text = text.replace("<code>", "`").replace("</code>", "`")
    return text
