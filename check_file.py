import os.path
from os import path

def main():

   print ("file exist:"+str(path.exists('store/guru99.txt')))
   print ("File exists:" + str(path.exists('career.guru99.txt')))
   print ("directory exists:" + str(path.exists('myDirectory')))

if __name__== "__main__":
   main()