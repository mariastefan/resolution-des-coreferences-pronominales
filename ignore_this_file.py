import os, re

already_installed = os.popen('pip freeze').read()
requirements = open('requirements.txt', 'r')
uninstall = open('uninstall.sh', 'w')
regex = "(.+)(==.+)"
pack1 = False
pack2 = False
pack3 = False
for req in requirements:
    found = False
    res_req = re.search(regex, req)
    for inst in already_installed:
        res_inst = re.search(regex, req)
        if res_req.group(1) == res_inst.group(1):
            found = True
            break
        elif res_inst == 'fr-core-news-sm':
            pack1 = True
            break
        elif res_inst == 'importlib-metadata':
            pack2 = True
            break
        elif res_inst == 'zipp':
            pack3 = True
            break
    if found == False:
        uninstall.write("yes | pip3 uninstall " + res_req.group(1) + ";\n")
if pack1 == False:
    uninstall.write("yes | pip3 uninstall fr-core-news-sm;\n")
if pack2 == False:
    uninstall.write("yes | pip3 uninstall importlib-metadata;\n")
if pack3 == False:
    uninstall.write("yes | pip3 uninstall zipp;\n")
