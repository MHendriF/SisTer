import os
import sys

isinya = None
with open('gambar.jpg','rb') as f1:
    while True:
        buf=f1.read()
        isinya = buf
        # isinya.append(buf)
        # print isinya
        break



with open('gambar2.jpg','wb') as f2:
    print isinya
    while True:
        # if isinya: 
        #     for byte in isinya:
        #         pass    # process the bytes if this is what you want
        #                 # make sure your changes are in buf
        
        f2.write(isinya)
        print 'makan'
        break
        