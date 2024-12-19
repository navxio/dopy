def preprocess_do_end(source):
    """
    Preprocesses Python code with do..end blocks into standard Python indentation.

    Args:
        source (str): Source code using do..end syntax
    Returns:
        str: Converted Python code with proper indentation
    """
    # Split the source into lines
    lines = source.split("\n")
    processed_lines = []
    indent_level = 0
    indent_size = 4

    for line in lines:
        # Strip original whitespace
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            processed_lines.append("")
            continue

        # Handle end keyword - decrease indent before processing
        if stripped == "end":
            indent_level -= 1
            if indent_level < 0:
                raise SyntaxError("Unmatched 'end' statement")
            continue

        # Add proper indentation
        processed_line = " " * (indent_level * indent_size) + stripped

        # Handle do keyword - increase indent after processing
        if stripped.endswith(" do"):
            # Remove 'do' and add ':'
            processed_line = processed_line[:-3] + ":"
            indent_level += 1

        processed_lines.append(processed_line)

    # Check for missing end statements
    if indent_level > 0:
        raise SyntaxError("Missing 'end' statement(s)")

    return "\n".join(processed_lines)


def process_file(input_path, output_path):
    """
    Process a file containing do..end syntax and write the converted code to output file.

    Args:
        input_path (str): Path to input file
        output_path (str): Path to output file
    """
    with open(input_path, "r") as f:
        source = f.read()

    processed = preprocess_do_end(source)

    with open(output_path, "w") as f:
        f.write(processed)
