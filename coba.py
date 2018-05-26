import Pyro4
import hashlib

def get_node(namafile):
    petalokasi = {}
    petalokasi['A'] = ('PYRONAME:kelompok3.worker1')
    petalokasi['B'] = ('PYRONAME:kelompok3.worker2')
    petalokasi['C'] = ('PYRONAME:kelompok3.worker3')
    petalokasi['D'] = ('PYRONAME:kelompok3.worker4')
    encode = namafile.encode('utf-8')
    h1= hashlib.md5(encode).hexdigest()[-1]
    if  h1 == '0' or h1 == '1' or h1 == '2' or h1 == '3':
        return petalokasi['A']
    elif h1 == '4' or h1 == '5' or h1 == '6' or h1 == '7':
        return petalokasi['B']
    elif h1 == '8' or h1 == '9' or h1 == 'a' or h1 == 'b':
        return petalokasi['C']
    elif h1 == 'c' or h1 == 'd' or h1 == 'e' or h1 == 'f':
        return petalokasi['D']


def storefile(namafile, isifile):
    lokasi = get_node(namafile)
    print(lokasi)
    storage = Pyro4.Proxy(lokasi)
    storage.store (namafile,isifile)

def getfile(namafile,isifile):
    lokasi = get_node(namafile)
    storage = Pyro4.Proxy(lokasi)
    konten = storage.get (namafile,isifile)
    return konten

def main():
    file = "buku"
    isi = "pdf"
    file2 = "koran"
    isi2 = "tulisan"
    storefile(file,isi)
    getfile(file,isi)
    storefile(file2, isi2)



if __name__ == '__main__':
    main()



