import argparse
import ast
import os
from collections import defaultdict


def find_imports(path, ignore_prefix=None, ignore_relative=False):
    imports_dict = defaultdict(set)  # Dictionary to store imports and their files

    def process_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=file_path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        # Check if we should ignore relative imports
                        if ignore_relative and node.module and node.module.startswith('.'):
                            continue
                        module = node.module if node.module else "Relative import"
                        if ignore_prefix and module.startswith(ignore_prefix):
                            continue
                        imports_dict[module].add(file_path)
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            module = alias.name
                            if ignore_prefix and module.startswith(ignore_prefix):
                                continue
                            imports_dict[module].add(file_path)
        except SyntaxError:
            print(f"Syntax error in {file_path}, skipped.")
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")

    if os.path.isfile(path):
        if path.endswith('.py'):
            process_file(path)
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    process_file(full_path)

    return imports_dict


def print_imports(path, verbose=True, ignore_prefix=None, ignore_relative=False):
    imports = find_imports(path, ignore_prefix, ignore_relative)

    print(f"Imports in {path}:")
    for module, files in sorted(imports.items()):
        print(f"Module: {module}")
        if verbose:
            for file in sorted(files):
                print(f"  Imported by: {file}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Python module imports")
    parser.add_argument("--path", type=str, required=True, help="Path to the Python file or package directory")
    parser.add_argument("--verbose", action='store_true', default=True,
                        help="Print each module's importing files (default)")
    parser.add_argument("--quiet", action='store_false', dest='verbose',
                        help="Do not print each module's importing files")
    parser.add_argument("--ignore-local", action='store_true',
                        help="Ignore local imports that start with the local directory name")
    parser.add_argument("--ignore-relative", action='store_true', help="Ignore relative imports that start with a dot")

    args = parser.parse_args()

    arg_ignore_prefix = os.path.basename(args.path) + "." if args.ignore_local else None

    print_imports(args.path, args.verbose, arg_ignore_prefix, args.ignore_relative)
