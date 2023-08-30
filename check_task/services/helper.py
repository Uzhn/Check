def format_error_lines(split_errors: list) -> list:
    formatted_errors_lst = []
    for line in split_errors:
        parts = line.split(':')
        filename = parts[0].split('/')[-1]
        rest_of_line = ':'.join(parts[1:])
        formatted_line = f'{filename}:{rest_of_line}'
        formatted_errors_lst.append(formatted_line)
    return formatted_errors_lst
