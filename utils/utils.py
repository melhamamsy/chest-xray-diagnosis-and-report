import os
from dotenv import load_dotenv


def initialize_env_variables(project_root=None, override=True):
    """
    Initialize environment variables from a .env file.

    Args:
        project_root (str, optional): The root directory of the
        project. Default is None.
    """
    # Construct the full path to the .env file
    if not project_root:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

    dotenv_path = os.path.join(project_root, ".env")

    print("Initialized environment variables listed in:", dotenv_path)
    # Load the .env file
    load_dotenv(dotenv_path, override=override)

    
def word_counter(text):
    """
    """
    return len(text.split())


def count_ab_categories(sublists, category_a, category_b):
    """
    """
    a = 0
    b = 0
    a_b = 0
    n_ab = 0
    
    for sublist in sublists:
        if category_a in sublist and category_b in sublist:
            a_b += 1
        elif category_a in sublist:
            a += 1
        elif category_b in sublist:
            b += 1
        else:
            n_ab += 1
    
    return {
        f"{category_a}": a,
        f"{category_b}": b,
        f"{category_a} & {category_b}": a_b,
        "Neither": n_ab
    }
