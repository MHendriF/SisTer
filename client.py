import sys
import Pyro4
import os

def readFile(file):
    print ">> Membaca file"
    with open(file,'rb') as f1:
        buf=f1.read()
    return buf

def main():
    uri = 'PYRO:middleware@127.0.0.1:8001'
    middleware = Pyro4.Proxy(uri)
    commands = middleware.getCommands()
    cwd = '/'
    while True:
        args = []
        print ('cli >> '+ cwd ),
        arg = raw_input()
        args.extend(arg.split(' '))

        if args[0] in commands:
            if args[0] == 'exit':
                break

            if args[0] == 'cd':
                errors, results, cwd = middleware.args(args, cwd)
                if(errors is not None):
                    print('Server: '+errors)

            if args[0] == 'ls':
                errors, results, cwd = middleware.args(args, cwd)
                if(errors is not None):
                    print('Server: '+errors)
                else:
                    if(isinstance(results, list)):
                        for result in results:
                            print(result)
                    else:
                        print(results)

            if args[0] == 'rm' or args[0] == 'touch' or args[0] == 'cp' or args[0] == 'mv':
                errors, results, cwd = middleware.args(args, cwd)
                if(errors is not None):
                    print('Server: '+errors)
                else:
                    print('Server: '+results)

            if args[0] == 'upload':
                print '>> ' + str(args)
                print '>> Sedang mengupload...'
                data = readFile(args[1])
                middleware.upload(args[1],data)
                print '>> File ' + args[1] + ' berhasil di upload!'
                del args[:]

        elif args[0] == '':
            continue

        else:
            print('server: command not found: '+args[0])



if __name__ == "__main__":
    main()
