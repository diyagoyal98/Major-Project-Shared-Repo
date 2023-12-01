import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""

def update_all_food_count(dict1,dict2):
    output_dict={}
    for key, value in dict1.items():
        output_dict[key] = output_dict.get(key, 0) + value

    # Update values from dict2
    for key, value in dict2.items():
        output_dict[key] = output_dict.get(key, 0) + value

    return output_dict


def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result