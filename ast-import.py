import argparse
import ast
import os
from collections import defaultdict


def find_imports(path, ignore_prefix=None, ignore_relative=False):
    imports_dict = defaultdict(set)  # Dictionary to store imports and their files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=full_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ImportFrom):
                                # Check if we should ignore relative imports
                                if ignore_relative and node.module and node.module.startswith('.'):
                                    continue
                                module = node.module if node.module else "Relative import"
                                if ignore_prefix and module.startswith(ignore_prefix):
                                    continue
                                imports_dict[module].add(full_path)
                            elif isinstance(node, ast.Import):
                                for alias in node.names:
                                    module = alias.name
                                    if ignore_prefix and module.startswith(ignore_prefix):
                                        continue
                                    imports_dict[module].add(full_path)
                except SyntaxError:
                    print(f"Syntax error in {full_path}, skipped.")
                except Exception as e:
                    print(f"Error reading {full_path}: {str(e)}")
    return imports_dict


def print_imports(directory_path, verbose=True, ignore_prefix=None, ignore_relative=False):
    imports = find_imports(directory_path, ignore_prefix, ignore_relative)

    print(f"Imports in {directory_path}:")
    for module, files in sorted(imports.items()):
        print(f"Module: {module}")
        if verbose:
            for file in sorted(files):
                print(f"  Imported by: {file}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Python module imports")
    parser.add_argument("--module-path", type=str, required=True, help="Path to the Python module directory")
    parser.add_argument("--verbose", action='store_true', default=True,
                        help="Print each module's importing files (default)")
    parser.add_argument("--quiet", action='store_false', dest='verbose',
                        help="Do not print each module's importing files")
    parser.add_argument("--ignore-local", action='store_true',
                        help="Ignore local imports that start with the local directory name")
    parser.add_argument("--ignore-relative", action='store_true', help="Ignore relative imports that start with a dot")

    args = parser.parse_args()

    arg_ignore_prefix = os.path.basename(args.module_path) + "." if args.ignore_local else None

    print_imports(args.module_path, args.verbose, arg_ignore_prefix, args.ignore_relative)
