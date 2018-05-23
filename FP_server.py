import Pyro4
import hashlib

def get_node(namafile):
    petalokasi = {}
    petalokasi ['A'] = 'PYRO:example.warehouse@localhost:51279'
    petalokasi['B'] = 'PYRO:example.warehouse@localhost:51280'
    petalokasi['C'] = 'PYRO:example.warehouse@localhost:51281'
    petalokasi['D'] = 'PYRO:example.warehouse@localhost:51282'

    h1= hashlib.md5(namafile).hexdigest()[-1]
    if  h1 == '0' or h1 == '1' or h1 == '2' or h1 == '3':
        return petalokasi['A']
    elif h1 == '4' or h1 == '5' or h1 == '6' or h1 == '7':
        return petalokasi['B']
    elif h1 == '8' or h1 == '9' or h1 == 'a' or h1 == 'b':
        return petalokasi['C']
    elif h1 == 'c' or h1 == 'd' or h1 == 'e' or h1 == 'f':
        return petalokasi['D']

	# h1= hashlib.md5(namafile).hexdigest()[-1]
	# cek = cekkoneksi(h1)
	# if(cek):
	# 	return petalokasi[h1]
	# h2= hashlib.md5(namafile).hexdigest()[-2]
	# cek = cekkoneksi(h2)
	# if(cek):
	# 	return petalokasi[h2]

	# return False

def storefile(namafile, isifile):
	lokasi = get_node(namafile)
	storage = Pyro4.Proxy(lokasi)
	storage.storefile(namafile, content)

def getfile(namafile):
	storage = Pyro4.Proxy(lokasi)
	content = storage.getfile(namafile)
	return content