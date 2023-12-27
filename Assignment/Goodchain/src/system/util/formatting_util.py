def create_formatted_string(prefix, data):
    formatted_data = f"{prefix} " + ','.join(f"{key}:{value}" for key, value in data.items())
    return formatted_data

def parse_formatted_string(data_string):
    data_pairs = data_string.split(',')
    parsed_data = {}
    for pair in data_pairs:
        key, value = pair.split(':')
        parsed_data[key] = value

    return parsed_data