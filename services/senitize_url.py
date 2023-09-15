import re

def sanitize_file_path(url):
    unsafe_chars_pattern = r"[^a-zA-Z0-9_\-:/?=&. ]"
    sanitized_url = re.sub(unsafe_chars_pattern, '_', url)
    return sanitized_url