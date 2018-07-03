import requests
import time

target_list = ['jed@atlasuhv.com']

subject = 'open or ur computer will get aids'

for i in range(0,1):
	r = requests.post("https://psh-email-server.000webhostapp.com/mail.php", data={'to':target_list[0],'from':'Ramon Dailey support@daileycomputer.com','subject':subject,'message':'lol too late.'})
	print(r.status_code, r.reason)
	print(r.text)
	time.sleep(3)
