import os
import re


def write(chat, direct):
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)

    files = []
    for match in matches:
        # Strip the filename of any non-allowed characters and convert / to \
        path = re.sub(r'[<>"|?*]', "", match.group(1))

        # Remove leading and trailing brackets
        path = re.sub(r"^\[(.*)\]$", r"\1", path)

        # Remove leading and trailing backticks
        path = re.sub(r"^`(.*)`$", r"\1", path)

        # Remove trailing ]
        path = re.sub(r"\]$", "", path)

        path = re.sub(r":", "", path)
        path = re.sub(r"`", "", path)

        # Get the code
        code = match.group(2)

        # Add the file to the list
        files.append((path, code))

    # Get all the text before the first ``` block
    # readme = chat.split("```")[0]
    # files.append(("README.md", readme))

    for file_name, file_content in files:
        file_path = os.path.join(direct, file_name)
        dirt = os.path.dirname(file_path)
        os.makedirs(dirt, exist_ok=True)

        with open(file_path, "w") as file:
            file.write(file_content)
