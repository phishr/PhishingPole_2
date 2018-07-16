import requests
import time

target_list = ['eliasbothell22@gmail.com']

subject = 'Phishr Password Recovery Code'

for i in range(0,1):
	r = requests.post("https://psh-email-server.000webhostapp.com/mail.php", data={'to':target_list[0],'from':'support@phishr.io','subject':subject,'message':'Your password recovery code is: 42069'})
	print(r.status_code, r.reason)
	print(r.text)
	time.sleep(3)
