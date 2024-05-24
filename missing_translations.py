import re
import sys
import yaml

from pathlib import Path
from yaml.constructor import SafeConstructor


# Remove boolean parsing (e.g. avoid "yes" being converted to True)
def add_bool(self, node):
    return self.construct_scalar(node)


SafeConstructor.add_constructor("tag:yaml.org,2002:bool", add_bool)

project_root = sys.argv[1]
locale_file = sys.argv[2]

string_pattern = re.compile(r'\.Trans\("([\S.]+)".*\)', re.NOFLAG)

with open(locale_file, "r") as file:
    locale_yaml = yaml.safe_load(file)

has_missing = False
for path in Path(project_root).rglob("*.go"):
    contents = path.read_text("utf-8")

    matches = string_pattern.findall(contents)
    for match in matches:
        locale_yaml_depth = locale_yaml
        for item in match.split("."):
            locale_yaml_depth = locale_yaml_depth.get(item, None)
            if not locale_yaml_depth:
                has_missing = True
                print(f"- {path}: Missing '{match}'")
                break

if has_missing:
    print("\nOops, there are missing translation strings.")
else:
    print("\nNo missing translation strings. Good job!")

exit(has_missing)
