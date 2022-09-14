import socket
import os , threading , sys , time, random
from tqdm import tqdm as t
ip = "192.168.103.24"
port = 8000
buffer_size = 8096 * 1000
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
#file_name = "C:/Users/Dell/Downloads/LINUX/Parrot-home-5.0.1_amd64.iso"
file_name ="D:/Grand Theft Auto - San Andreas.rar"
print(f"\n[*] Listening {ip}:{port}")
def file_serve(client,file_name,file_size,unit,raw_size):
	uploaded = 0
	pbar = t(range(0,int(raw_size/buffer_size)),unit_scale = True , bar_format = "\r{l_bar}{bar}")
	
	with open(file_name,"rb") as file:
		while True:
			#time.sleep(1)
			file_segment = file.read(buffer_size)
			
			if not file_segment:
				client.close()
				break
			
			try:
				client.sendall(file_segment)
			except:
				print("[*] Connection Closed, Data Transfer unsuccessfull")
				client.close()
				break

			uploaded = uploaded+len(file_segment)
			up_size , up_unit = conversion(uploaded)
			pbar.set_description(f"[*] {file_name} : {round(file_size,2)} {unit}/{round(up_size,2)} {up_unit}")
			pbar.n = 0
			pbar.update(int(uploaded/buffer_size))

def conversion(size):
	size = float(size)
	kb = 1/1024
	mb = 1/(1024*1024)
	gb = 1/(1024*1024*1024)
	if size >= 1/kb and size < 1/mb:
		return size*kb , 'Kb' 
	elif size >= 1/mb and size < 1/gb:
		return size*mb , 'Mb'
	elif size >= 1/gb:
		return size*gb , 'Gb'

	return size , 'byte'

def initial_setup(client,addr):
	print(f"\n[*] Accepted Connection From {addr[0]}:{addr[1]}\n")
	raw_size = os.path.getsize(file_name)	
	file_size , unit = conversion(raw_size)
	file_info = f"{file_name}<::>{raw_size}"
	client.send(file_info.encode())
	file_serve(client,file_name,file_size,unit,raw_size)
	# print("\n[*] File Transferred Successfully")


Client_Threads = []
while True:
    client , addr = server.accept()
    client_threads = threading.Thread(target = initial_setup,args=(client,addr))
    client_threads.start()
    Client_Threads.append(client_threads)

for thread in Client_Threads:
	thread.join()




