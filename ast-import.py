import argparse
import ast
import os
from collections import defaultdict


def find_imports(path):
    imports_dict = defaultdict(set)  # Dictionary to store imports and their files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=full_path)
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.Import, ast.ImportFrom)):
                                module = getattr(node, 'module', None)
                                if module:
                                    imports_dict[module].add(full_path)  # Track which file imports the module
                                elif isinstance(node, ast.ImportFrom):
                                    # Handle relative imports
                                    imports_dict[node.module if node.module else "Relative import"].add(full_path)
                except SyntaxError:
                    print(f"Syntax error in {full_path}, skipped.")
                except Exception as e:
                    print(f"Error reading {full_path}: {str(e)}")
    return imports_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Python module imports")
    parser.add_argument("--module-path", type=str, required=True, help="Path to the Python module directory")
    args = parser.parse_args()

    directory_path = args.module_path
    imports = find_imports(directory_path)

    print(f"Imports in {directory_path}:")
    for module, files in sorted(imports.items()):
        print(f"Module: {module}")
        for file in sorted(files):
            print(f"  Imported by: {file}")
        print()
