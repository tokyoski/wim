import getpass
import re
import subprocess

wlan = None
iwdev = subprocess.check_output("iw dev | grep 'Interface' | cut -d ' ' -f2", shell=True, encoding="UTF-8")
wlan_list = str(iwdev)

def choose_wlan():
	global wlan
	while True:
		print("Wireless interfaces found: ", end="\n")
		print(wlan_list)
		print("Input the interface you want to switch:", end=" \n\n")
		wlan_in = input()
		if wlan_in in wlan_list:
			wlan = wlan_in
			break
		else:
			print("There is no such interface! Please check the list again!", end="\n\n")
			continue

def monitor():
	subprocess.call('airmon-ng check kill && ip link set {0} down && iw {0} set monitor control && ip link set {0} up'.format(wlan), shell=True)
	return

def managed():
	subprocess.call('ip link set {0} down && iw {0} set type managed && ip link set {0} up && systemctl start NetworkManager'.format(wlan), shell=True)
	return

def commands():
	print("1. Turn on monitor mode\n2. Turn on managed mode\n3. Exit the script\n\nYour input:", end=" ")
	command = input()
	while True:
		if command == "1":
			monitor()
			print("Your wireless interface is now in monitor mode")
			break
		elif command == "2":
			managed()
			print("Your wireless interface is now in managed mode.")
			break
		elif command == "3":
			print("Exiting...")
			exit()
		else:
			print("\n")
			break
			commands()

def main():
	if getpass.getuser() == "root":
		choose_wlan()
		commands()
	else:
		print("Please run the script as root ('sudo python wims.py' or 'sudo python3 wims.py').")
		exit()

main()
