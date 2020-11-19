import os

#print(os.getcwd())
os.chdir("C:\midicsv-1.1") # Directorio donde se trabajara
print(os.getcwd())

nmid = 'music14' # nombre del archivo MIDI
import subprocess
outfd=open('Out.txt','w+')
errfd=open('Err.txt','w+')

print('Archivo', nmid)
subprocess.call(['midicsv', '-v', nmid+'.mid'], stdout=outfd, stderr=errfd) # Ejecuta MIDICSV
outfd.close()
errfd.close()

