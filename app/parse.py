import re


def parse_indice(key):
    m = re.search(r'(.*)\[(\d)]', key)
    if m:
        return m.group(1), int(m.group(2))
    else:
        return None, None


def merge_dict(a, b):
    return {**a, **b}


def parse_col(keys, current_value, current_output):
    current_key = keys[0]
    real_key, indice = parse_indice(current_key)
    if len(keys) == 1:
        if real_key:
            if real_key not in current_output:
                current_output[real_key] = []
            current_output[real_key] += [current_value]
        else:
            current_output[current_key] = current_value
    else:
        if real_key:
            if real_key not in current_output:
                current_output[real_key] = []
            if len(current_output[real_key]) - 1 < indice:
                current_output[real_key] += [{}]
            parse_col(keys[1:], current_value, current_output[real_key][indice])
        else:
            if current_key not in current_output:
                current_output[current_key] = {}
            parse_col(keys[1:], current_value, current_output[current_key])
    return current_output


def parse_row(row):
    parsed = {}
    for key, value in row.items():
        key_tree = key.split('.')
        parse_col(key_tree, value, parsed)
    return parsed
