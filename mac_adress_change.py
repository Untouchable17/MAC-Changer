#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
	""" Проверка и выводит информации """
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="Интерфейс для изменения MAC-адреса")
	parser.add_option("-m", "--mac", dest="new_mac", help="Новый MAC-адрес")
	(options, arguments) = parser.parse_args()
	if not options.interface:
		parse.error("[-] Укажите интерфейс для изменения, используйте --help для большей информации")
	elif not options.new_mac:
		parser.error("[-] Укажите новый МАК-адрес, используйте --help для большей информации")
	return options


def update_to_new_mac(interface, new_mac):
	""" Изменение на новый мак-адрес """
	print("[+] Изменение мак-адреса с " + interface + " на " + new_mac)
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
	""" Получение текущего мак-адреса """
	ifconfig_result = subprocess.check_output(["ifconfig", interface])

	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Не удалось прочитать мак-адрес")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Текущий MAC-адрес = " + current_mac)

update_to_new_mac(options.interface, options.new_mac)

# перезаписывается на новый мак адрес
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
	print("[+] MAC был успешно изменен на " + current_mac)
else:
	print("[-] MAC не был изменен")