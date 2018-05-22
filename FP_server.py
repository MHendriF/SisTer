import hashlib

def get_node(namafile):
	petalokasi = {}
	petalokasi ['a'] = 'PYRO:example.warehouse@localhost:51279'
	h1= hashlib.md5(namafile).hexdigest()[-1]
	return petalokasi[h1]

	# h1= hashlib.md5(namafile).hexdigest()[-1]
	# cek = cekkoneksi(h1)
	# if(cek):
	# 	return petalokasi[h1]
	# h2= hashlib.md5(namafile).hexdigest()[-2]
	# cek = cekkoneksi(h2)
	# if(cek):
	# 	return petalokasi[h2]

	# return False

def storefile(namafile,isifile):
	lokasi = get_node(namafile)
	storage = Pyro4.Proxy(lokasi)
	storage.storefile(namafile,content)

def getfile(namafile):
	storage = Pyro4.Proxy(lokasi)
	content = storage.getfile(namafile)
	return content