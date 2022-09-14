import socket
from tqdm import tqdm as t
import os , datetime, time
server_ip = "192.168.103.24"
server_port = 8000
buffer_size= 8096 * 1000
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((server_ip,server_port))
recv = client.recv(buffer_size)
recv = recv.decode()
file_info = recv.split('<::>')

file_name = os.path.basename(file_info[0])

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

file_size = file_info[1]
raw_size = int(file_size)
file_size , file_unit = conversion(file_size)

def percentage(downloaded_size,pbar):
	 percent = round((downloaded_size/raw_size)*100)
	 colour = {percent < 50 :'red', percent >=50 and percent < 80: 'yellow' , percent >= 80 : 'green'}
	 pbar.colour = colour[True]

def file_download():
	pbar = t(range(0,int(raw_size/buffer_size)),unit_scale = True , bar_format = "\r{l_bar}{bar}")
	downloaded = 0
	with open(file_name,'wb') as file:
		while True:
			time.sleep(1)
			file_segment = client.recv(buffer_size)
			if not file_segment:
				client.close()
				break
			file.write(file_segment)
			downloaded += len(file_segment)
			down_str , down_unit = conversion(downloaded)
			time.sleep(1)
			download_speed , speed_unit = conversion(len(file_segment))

			download_speed_str = f"{round(download_speed,2)}{speed_unit}/s"
			 
			eta = eta_time = int((raw_size - downloaded)/len(file_segment))
			eta = str(datetime.timedelta(seconds=eta))
			pbar.set_description(f"[*] {file_name} : {round(file_size,2)} {file_unit}/{round(down_str,2)} {down_unit} [ ETA: {eta}] [ Speed : {download_speed_str} ]")
			pbar.n = 0
			pbar.update(int(downloaded/buffer_size))
			percentage(downloaded,pbar)
			


file_download()
print('[*] File Downloaded Successfully')

