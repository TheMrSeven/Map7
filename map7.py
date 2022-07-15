# This is the map7 my project to run nmap faster and better without repetetion
# Is pretty basic, but it really help and make this fast!
# This project is created by me MrSeven
# This is my youtube Channel (https://www.youtube.com/c/MrSevenCyberSec)
# And the github page that you found that ()
import os
import subprocess
from ftplib import FTP
#-------------------------------------------------
#---------------Default Options-------------------
#-------------------------------------------------

#Always Create Directories?
wantfolders = "y" #Set the defalt value, "y" for always create dirs, "n" for never create dirs and "" to get asked everytiem

#Always run extra scans? (Carreful with this one) 
wantvulnscans = "y" #Set the defalt value, "y" for always run scans, "n" for never run scans and "" to get asked everytiem
 
#Show the output of the nmap scans, you can choose here
shownmap1 = True #Set to true if you want to see the output of "nmap <target-ip>"
shownmap2 = True #Set to true if you want to see the output of "nmap -p <open-ports> -sV -sC <target-ip>"
shownmap3 = False #Set to true if you want to see the output of "nmap -p- <target-ip>"
shownmap4 = False #Set to true if you want to see the output of "nmap -p <all-open-ports> -sV -sC <target-ip>"
shownmap5 = False #Set to true if you want to see the output of "nmap -sU <target-ip>"
#-------------------------------------------------
#-------This run the Inicials Scans---------------
#-------------------------------------------------
def inicialscans(targetip,targetfolder):
	# Create Folder
	if os.path.isdir(targetfolder) == False:
		os.system("mkdir "+ targetfolder)

	print("\n\n\nStating Inicial Scans - Get Ready!: \n \n")
	
	# Inicial scan to find open ports
	print("Step 1")
	os.system("mkdir "+targetfolder+"/nmap")
	print("Running This Command: "+"nmap " + targetip)
	os.system("nmap "+ targetip + "> quickscan.out")
	os.system("mv quickscan.out "+targetfolder+"/nmap\n")
	if shownmap1 == True:
		print("\n\n\nOutput of Step 1\n\n\n")
		os.system("cat "+targetfolder+"/nmap/quickscan.out\n\n\n")
	print("Step 1 Done")
	# Run Default Script and Version Enum on Open Ports
	print("Step 2")
	# Grep for the ports and sanityze
	os.system("cat " + targetfolder + "/nmap/quickscan.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	print("Running This Command: "+"nmap -p "+ ports + " -sV -sC "+targetip)
	os.system("nmap -p "+ ports + " -sV -sC "+targetip + "> inicialscans.out")
	os.system("mv inicialscans.out "+targetfolder+"/nmap")
	os.system("rm ports.txt\n")
	if shownmap2 == True:
		print("\n\n\nOutput of Step 2\n\n\n")
		os.system("cat "+targetfolder+"/nmap/inicialscans.out\n\n\n")
	print("Step 2 Done")

	# Scan for all open ports
	print("Step 3")
	print("Running This Command: "+"nmap -p- "+targetip)
	os.system("nmap -p- "+targetip+"> quick-allports.out")
	os.system("mv quick-allports.out "+targetfolder+"/nmap\n")
	if shownmap3 == True:
		print("\n\n\nOutput of Step 3\n\n\n")
		os.system("cat "+targetfolder+"/nmap/quick-allports.out\n\n\n")
	print("Step 3 Done")
	# Run Default Scripts and Versions of All Open Ports
	print("Step 4")
	os.system("cat " + targetfolder + "/nmap/quick-allports.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	print("Running This Command: "+"nmap -p "+ ports + " -sV -sC "+targetip)
	os.system("nmap -p "+ ports + " -sV -sC "+targetip + "> all-ports.out")
	os.system("mv all-ports.out "+targetfolder+"/nmap")
	os.system("rm ports.txt\n")
	if shownmap4 == True:
		print("\n\n\nOutput of Step 4\n\n\n")
		os.system("cat "+targetfolder+"/nmap/all-ports.out\n\n\n")
	print("Step 4 Done")
		
	# Udp Scan
	print("Step 5")
	print("Running This Command: "+"nmap -sU "+targetip)
	os.system("nmap -sU "+targetip+">udpscan.out")
	os.system("mv udpscan.out "+targetfolder+"/nmap\n")
	if shownmap5 == True:
		print("\n\n\nOutput of Step 5\n\n\n")
		os.system("cat "+targetfolder+"/nmap/udpscan.out\n\n\n")
	print("Step 5 Done")
	print("\n\n\nScans Are All Done!\n\n\n")

#-------------------------------------------------
#-------This run the Scripts for Vulns------------
#-------------------------------------------------
def vulnscans(targetip):
	os.system("cat " + targetfolder + "/nmap/quick-allports.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	# SMB
	print("Let's start with SMB")
	if "445" in ports:
		print("Trying to map folders with smbmap")
		os.system("smbmap -H "+targetip+">"+targetfolder+"/smb/smbmap.out")
		os.system("smbmap -u \"guest\" -H "+targetip+">"+targetfolder+"/smb/smbmap-guest.out")
		canirun = input("Port 445(SMB) Looks Open, can I run the vulns scripts on that?[y][n]\n")
		if canirun == "y":
			canbeunsafe = input("Can I set the arguments as unsafe? This can crash the system[y][n]\n")
			if canirun == "y":
				print("Running This Command:"+"nmap -p 139,445 --script=smb-vuln* --script-args=unsafe=1 "+targetip )
				os.system("nmap -p 139,445 --script=smb-vuln* --script-args=unsafe=1 "+targetip)
			else:
				print("Running This Command:"+"nmap -p 139,445 --script=smb-vuln* "+targetip )
				os.system("nmap -p 139,445 --script=smb-vuln* "+targetip)
	else:
		print("Dosen't Look Like Smb is present")
	if "21" in ports:
		global ftp
		print("What about FTP")
		print("Trying Anonymous Connection")
		ftp = FTP(targetip,user='anonymous', passwd='')
		print("Printing Folders if anonymous connection worked")

		if ftp.dir() == "None":
			print("I can connect but not getting anything, maybe the FTP is empty")
		else:
			print(ftp.dir())
	else:
		print("Dosen't Look Like FTP is present")
	# Remove The Ports File
	os.system("rm ports.txt")

#-----------------------
#-------Create Folders--
#-----------------------
def createfolders(targetfolder):
	print("\n\nCreating Folders Based on Open Ports\n\n")
	os.system("cat " + targetfolder + "/nmap/quick-allports.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	os.system("rm ports.txt")
	#SMB
	if "445" in ports:
		if os.path.isdir(targetfolder+"/smb") == False:
			os.system("mkdir "+targetfolder+"/smb")
			print("Created the SMB Folder")
	#FTP
	if "21" in ports:
		if os.path.isdir(targetfolder+"/ftp") == False:
			os.system("mkdir "+targetfolder+"/ftp")
			print("Created the FTP Folder")
	#WWW
	if "80" in ports or "443" in ports:
		if os.path.isdir(targetfolder+"/www") == False:
			os.system("mkdir "+targetfolder+"/www")
			print("Created the WWW Folder")
	#PRIV-ESC
	if os.path.isdir(targetfolder+"/priv-esc") == False:
		os.system("mkdir "+targetfolder+"/priv-esc")
		os.system("cp /opt/PEASS-ng/winPEAS/winPEASexe/binaries/x64/Release/winPEASx64.exe "+targetfolder+"/priv-esc")
		os.system("cp /opt/PEASS-ng/linPEAS/linpeas.sh "+targetfolder+"/priv-esc")
		os.system("mv "+targetfolder+"/priv-esc/winPEASx64.exe "+targetfolder+"/priv-esc/winpeas64.exe")
		print("Created the Priv-Esc Folder")
	#SHELLS
	if os.path.isdir(targetfolder+"/shells") == False:
		os.system("mkdir "+targetfolder+"/shells")
		os.system("cp /opt/webshells/simple_phpwebshell.php "+targetfolder+"/shells")
		os.system("cp /opt/webshells/full_phpwebshell.php "+targetfolder+"/shells")	

#-----------------------
#-------MAIN------------
#-----------------------
# Global Variables
print("Welcome to Map7")
print("""\
          _____                    _____                    _____          
         /\    \                  /\    \                  /\    \         
        /::\____\                /::\    \                /::\    \        
       /::::|   |               /::::\    \              /::::\    \       
      /:::::|   |              /::::::\    \            /::::::\    \      
     /::::::|   |             /:::/\:::\    \          /:::/\:::\    \     
    /:::/|::|   |            /:::/__\:::\    \        /:::/__\:::\    \    
   /:::/ |::|   |           /::::\   \:::\    \      /::::\   \:::\    \   
  /:::/  |::|___|______    /::::::\   \:::\    \    /::::::\   \:::\    \  
 /:::/   |::::::::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\ 
/:::/    |:::::::::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |
\::/    / ~~~~~/:::/    /\::/    \:::\  /:::/    /\::/    \:::\  /:::|____|
 \/____/      /:::/    /  \/____/ \:::\/:::/    /  \/_____/\:::\/:::/    / 
             /:::/    /            \::::::/    /            \::::::/    /  
            /:::/    /              \::::/    /              \::::/    /   
           /:::/    /               /:::/    /                \::/____/    
          /:::/    /               /:::/    /                  ~~          
         /:::/    /               /:::/    /                               
        /:::/    /               /:::/    /                                
        \::/    /                \::/    /                                 
         \/____/                  \/____/                                  
 
 -By: Mr.Seven                                                                          
                    """)
targetip = input("Enter The Target IP: ")
targetfolder = input("Enter Machine Name(Folder Name): ")
if wantfolders == "":
	wantfolders = input("Do you want to create the folders? [y][n]")
if wantvulnscans == "":
	wantvulnscans = input("Do you want to run Vuln Scans? [y][n]")


# All starting Scans
inicialscans(targetip,targetfolder)

# Create Folders
if wantfolders == "y":
	createfolders(targetfolder)

# Start Extra Scans
if wantvulnscans == "y":
	vulnscans(targetip)

print("\n\n\n\nI`m just a tool for you?")