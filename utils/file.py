import os
import re


def create_folder(folder_name: str, parent_folder: str = None) -> str or None:
    """
    Create a folder with the specified name inside the specified parent folder.

    :param folder_name: The name of the folder to create.
    :param parent_folder: The parent folder in which to create the folder. If None, the folder will be created in
    the current working directory.
    :return: The path to the created folder, or None if the folder couldn't be created.
    :rtype: str or None
    """
    try:
        cleaned_folder_name = re.sub(r'[<>:"/\\|?*]', '', folder_name)

        if parent_folder:
            folder_path = os.path.join(parent_folder, cleaned_folder_name)
        else:
            folder_path = cleaned_folder_name

        os.makedirs(folder_path, exist_ok=True)

        return folder_path
    except OSError as e:
        print(f"Error creating folder '{folder_name}': {e}")
        return None


def create_file(file_name: str, folder: str, content: str or bytes, mode='w') -> str or None:
    """
    Create a file with the specified name inside the specified folder.

    :param file_name: The name of the file to create.
    :param folder: The folder in which to create the file.
    :param content: The content to write to the file.
    :param mode: The mode in which to open the file. By default, the mode is 'w' (write).
    :return: The path to the created file, or None if file creation fails.
    :rtype: str or None
    """
    try:
        cleaned_file_name = re.sub(r'[<>:"/\\|?*]', '', file_name)
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, cleaned_file_name)

        print(f"Creating file '{cleaned_file_name}' in folder '{folder}'...")

        if mode == 'wb':
            with open(file_path, mode) as f:
                f.write(content)
        elif mode == 'w':
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)

        return file_path
    except Exception as e:
        print(f"An error occurred while creating file '{file_name}': {e}")
        return None
