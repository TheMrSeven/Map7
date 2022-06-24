# This is the 7map my project to run nmap faster and better without repetetion
# Is pretty basic, but it really help and make this fast!
# This project is created by me MrSeven
# This is my youtube Channel (https://www.youtube.com/c/MrSevenCyberSec)
# And the github page that you found that ()


import os
import subprocess

#-------------------------------------------------
#-------This run the Inicials Scans---------------
#-------------------------------------------------
def inicialscans(targetip,targetfolder):
	# Create Folder
	os.system("mkdir "+ targetfolder)

	print("Stating Inicial Scans - Get Ready!: \n \n")
	
	# Inicial scan to find open ports
	print("Step 1")
	print("Running This Command: "+"nmap " + targetip)
	os.system("nmap "+ targetip + "> quickscan.out")
	os.system("mv quickscan.out "+targetfolder+"\n")

	print("Step 1 Done")

	# Run Default Script and Version Enum on Open Ports
	print("Step 2")
	# Grep for the ports and sanityze
	os.system("cat " + targetfolder + "/quickscan.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	print("Running This Command: "+"nmap -p "+ ports + " -sV -sC "+targetip)
	os.system("nmap -p "+ ports + " -sV -sC "+targetip + "> InicialScans.out")
	os.system("mv InicialScans.out "+targetfolder)
	os.system("rm ports.txt\n")

	print("Step 2 Done")

	# Scan for all open ports
	print("Step 3")
	print("Running This Command: "+"nmap -p- "+targetip)
	os.system("nmap -p- "+targetip+"> quick-allports.out")
	os.system("mv quick-allports.out "+targetfolder+"\n")
	print("Step 3 Done")
	# Run Default Scripts and Versions of All Open Ports
	print("Step 4")
	os.system("cat " + targetfolder + "/quick-allports.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	print("Running This Command: "+"nmap -p "+ ports + " -sV -sC "+targetip)
	os.system("nmap -p "+ ports + " -sV -sC "+targetip + "> All-Ports.out")
	os.system("mv All-Ports.out "+targetfolder)
	os.system("rm ports.txt\n")
	print("Step 4 Done")
		
	# Udp Scan
	print("Step 5")
	print("Running This Command: "+"nmap -sU "+targetip)
	os.system("nmap -sU "+targetip+">udpscan.out")
	os.system("mv udpscan.out "+targetfolder+"\n")
	print("Step 5 Done")
	print("Starting Scans Are All Done!")

#-------------------------------------------------
#-------This run the Scripts for Vulns------------
#-------------------------------------------------
def vulnscans(targetip):
	os.system("cat " + targetfolder + "/quick-allports.out | grep open | awk -F \"/\" '{print $1}' | sed '$!s/$/,/' | tr -d \"\n\" > ports.txt")
	ports = os.popen('cat ports.txt').read()
	print(ports)
	# SMB
	print("Let's start with SMB")
	if "445" in ports:
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

	# Remove The Ports File
	os.system("rm ports.txt")

# Global Variables
targetip = input("Enter The Target IP: ")
targetfolder = input("Enter The Target Folder: ")

#-----------------------
#-------MAIN------------
#-----------------------

# All starting Scans
#inicialscans(targetip,targetfolder)

wantvulnscans = input("Do you want to run Vuln Scans? [y][n]")

# Do you want Vuln Scans?
if wantvulnscans == "y":
	vulnscans(targetip)
else:
	print("Ok! No Scans For You")