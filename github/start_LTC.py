import os

os.chdir("LTC")
k = os.popen("ls *.py").read()
l = k.split('\n')

del l[-1]

for x in l:
    os.system("python3 " + x + ' &')
