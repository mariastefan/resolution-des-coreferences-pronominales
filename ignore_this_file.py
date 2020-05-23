import os
import re

requirements = open('requirements.txt', 'r')
uninstall = open('uninstall.sh', 'w')
regex = "([^=\s]+)=|\s.*"
dependency1 = False
dependency2 = False
dependency3 = False
for one_requirements_line in requirements:
    found = False
    requirements_pattern = re.search(regex, one_requirements_line)
    already_installed = os.popen('pip freeze')
    for one_already_installed_line in already_installed:
        installed_pattern = re.search(regex, one_already_installed_line)
        if requirements_pattern and installed_pattern and requirements_pattern.group(1) == installed_pattern.group(1):
            found = True
            break
        elif installed_pattern and installed_pattern.group(1) == 'fr-core-news-sm':
            dependency1 = True
            break
        elif installed_pattern and installed_pattern.group(1) == 'importlib-metadata':
            dependency2 = True
            break
        elif installed_pattern and installed_pattern.group(1) == 'zipp':
            dependency3 = True
            break
    if requirements_pattern and requirements_pattern.group(1) is not None and not found:
        uninstall.write("yes | pip3 uninstall " + str(requirements_pattern.group(1)) + ";\n")
if not dependency1:
    uninstall.write("yes | pip3 uninstall fr-core-news-sm;\n")
if not dependency2:
    uninstall.write("yes | pip3 uninstall importlib-metadata;\n")
if not dependency3:
    uninstall.write("yes | pip3 uninstall zipp;\n")
