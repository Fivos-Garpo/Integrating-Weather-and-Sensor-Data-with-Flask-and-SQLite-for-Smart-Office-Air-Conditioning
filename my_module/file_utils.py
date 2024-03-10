def read_api_key_from_file(file_path):
    """Read API key from a file."""
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print("File not found.")
        return None
