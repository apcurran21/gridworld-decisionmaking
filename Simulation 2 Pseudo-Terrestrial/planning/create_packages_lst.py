import os 
import re
from collections import defaultdict
from pathlib import Path

def find_imports_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    regex_str = r'^\s*(?:import|from)\s+([^\s]+)'
    imports = re.findall(regex_str, content, re.MULTILINE)
    return imports

def find_all_imports(directorypath):
    imports = defaultdict(int)
    for root, _, files in os.walk(directorypath):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                file_imports = find_imports_in_file(filepath)
                for import_str in file_imports:
                    imports[import_str.split('.')[0]] += 1
    return imports

def write_requirements(imports, output_file):
    with open(output_file, 'w') as f:
        for import_str in sorted(imports):
            f.write(f'{import_str}\n')

if __name__ == '__main__':
    directorypath = Path(r'/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning')
    output_file = 'unformatted_requirements.txt'
    imports = find_all_imports(directorypath)
    write_requirements(imports, output_file)