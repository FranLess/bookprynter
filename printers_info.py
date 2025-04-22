import subprocess, sys

command = 'lpstat e'
result = subprocess.check_output(command, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)
print(result)
# NOTE: I got no more than one printer so im actually guessing printers are shonw separated by ' '
# or could be by \n idk
AVAILABLE_PRINTERS = result.split[' ']

#The next opens the pdf with the default user's app to open pdfs
subprocess.run(["xdg-open", 'pdfile'])