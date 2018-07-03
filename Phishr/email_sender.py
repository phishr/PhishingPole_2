import requests

url = "https://lowderwithcrowder.000webhostapp.com/mail.php"

r = requests.post(url, data={'to': 'jed@atlasuhv.com', 'from': 'Ramon Dailey support@daileycomputer.com <support@daileycomputer.com>', 'subject': 'You need to read this or your computer will get aids.','message': 'lol too late'})

print(r.text[:100])