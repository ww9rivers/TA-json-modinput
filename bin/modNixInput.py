def parse_items_file(filename='/common/etc/node_masterfile.stz'):
    """
    Parse a file containing items with attributes in the format:
    item_name:
        attribute = value

    Args:
        filename (str): Path to the file to parse

    Returns:
        dict: Dictionary where keys are item names and values are dictionaries of attributes
    """
    items = {}
    current_item = None

    with open(filename, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Check if this is an item definition (ends with colon)
            if line.endswith(':'):
                current_item = line[:-1]  # Remove the colon
                items[current_item] = {}
                continue

            # If we have an attribute line
            if current_item and '=' in line:
                # Split and clean up the attribute-value pair
                attr_name, attr_value = [x.strip() for x in line.split('=', 1)]
                # Store the attribute
                items[current_item][attr_name] = attr_value
    return items
