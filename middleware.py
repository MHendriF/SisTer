import sys
import Pyro4
import os
import hashlib
#list_workers= ['PYRO:obj_407b5d663ba94cdc974651d5433b6b35@10.151.254.104:50099','PYRO:obj_407b5d663ba94cdc974651d5433b6b35@10.151.254.104:50099','PYRO:obj_407b5d663ba94cdc974651d5433b6b35@10.151.254.104:50099','PYRO:obj_407b5d663ba94cdc974651d5433b6b35@10.151.254.104:50099','PYRO:obj_407b5d663ba94cdc974651d5433b6b35@10.151.254.104:50099']
list_workers = ['PYRO:obj_62764364dfd747f785df1ae8fcb88a9d@10.151.36.51:37204','PYRO:obj_19827bdb5bf349dd827246b6bdb0e02d@10.151.253.54:59078','PYRO:obj_6f02b7f6e16c4935a1c9416bf1240da0@10.151.253.54:59070','PYRO:obj_876decb6510b4bf4acdff621ab67d8ea@10.151.253.151:52778']
# list_workers = ['PYRO:worker@127.0.0.1:9000','PYRO:worker@127.0.0.1:9001']
workers = []


@Pyro4.expose
@Pyro4.callback
class Middleware(object):

    def __init__(self):
        self.commands = ['ls','cd','rm','mv','touch','exit','cp', 'upload']
        return

    def getCommands(self):
        return self.commands

    def upload(self, file, data):
        numberServer1,numberServer2 = self.chooseWorker(file)
        worker = workers[numberServer1]
        worker2 = workers[numberServer2]
        cwd = '/'
        worker.createFile(cwd, file, data)
        p = '>> Upload ' + file + ' berhasil! file disimpan di server ' + repr(numberServer1 + 1)
        print (p)
        worker2.createFile(cwd, file, data)
        p = '>> Upload ' + file + ' berhasil! file disimpan di server backup : ' + repr(numberServer2+1)
        print (p)

    def chooseWorker(self, file):
        self.h1= hashlib.md5(file).hexdigest()[-1]
        if self.h1 == '0' or self.h1 == '1' or self.h1 == '2' or self.h1 == '3' :
            return 0,3
        elif self.h1 == '4' or self.h1 == '5' or self.h1 == '6' or self.h1 == '7' :
            return 1,2
        elif self.h1 == '8' or self.h1 == '9' or self.h1 == 'a' or self.h1 == 'b' :
            return 2,1
        elif self.h1 == 'c' or self.h1 == 'd' or self.h1 == 'e' or self.h1 == 'f' :
            return 3,0

        # if self.h2 == '0' or self.h2 == '1' or self.h2 == '2' or self.h2 == '3':
        #     return 0
        # elif self.h2 == '4' or self.h2 == '5' or self.h2 == '6' or self.h2 == '7':
        #     return 1
        # elif self.h2 == '8' or self.h2 == '9' or self.h2 == 'a' or self.h2 == 'b':
        #     return 2
        # elif self.h2 == 'c' or self.h2 == 'd' or self.h2 == 'e' or self.h2 == 'f':
        #     return 3

        #return self.number%5

    def generateStructureFolder(self, cwd, args, path_req=''):
        if(len(args)==1):
            return cwd
        else:
            if path_req[0] == '/':
                return path_req

            elif '../' in path_req:
                temp_args = path_req.split('../')
                empty_n = temp_args.count('')

                temp_cwds = cwd.split('/')

                if(len(temp_args)==empty_n):
                    counter = empty_n-1

                    if(empty_n>len(temp_cwds)):
                        cwd = '/'
                        return cwd

                    for i in range(len(temp_cwds)-1, 0, -1):

                        temp_cwds[i] = temp_args[counter]
                        counter-=1
                        if(counter==0):
                            cwd_fix = []
                            for temp_cwd in temp_cwds:

                                if len(temp_cwd)>0:
                                    cwd_fix.append(temp_cwd)

                            cwd_fix = '/'.join(cwd_fix)
                            if(cwd_fix=='/'):
                                cwd_fix == '/'
                            else:
                                cwd_fix = '/'+cwd_fix
                            break
                    return cwd_fix
                else:
                    temp_cwds.reverse()
                    counter=1;
                    cwd_fix = '/'
                    flag_break = 0;
                    for i in range(0, len(temp_cwds)-1):

                        temp_cwds[i] = temp_args[counter]
                        counter+=1

                        if(len(temp_args)==counter):
                            cwd_fix = []
                            temp_cwds.reverse()
                            for temp_cwd in temp_cwds:

                                if len(temp_cwd)>0:
                                    cwd_fix.append(temp_cwd)

                            cwd_fix = '/'.join(cwd_fix)
                            if(cwd_fix=='/'):
                                cwd_fix == '/'
                            else:
                                cwd_fix = '/'+cwd_fix
                            break

                    return cwd_fix
            else:
                if cwd == '/':
                    return (cwd+path_req)
                else:
                    return (cwd+'/'+path_req)
    
    def removeData(self, cwd, path=None):
        errors = []
        flag_exist = 0
        for worker in workers:
            error, results = worker.removeData(cwd, path)
            if(error is not None):
                errors.append(error)

        if(len(workers)==len(errors)):
            return 'Tidak ada data', ''
        return None, 'Sudah dihapus'

    def touch(self, cwd, path=None):
        errors = []
        flag_exist = 0
        paths = path.split('/')
        if(len(paths)==2):
            size = -1000;
            worker_selected = ''
            for worker in workers:
                temp, temp_path = worker.checkData(path)
                if(temp):
                    errors.append(temp)

            for worker in workers:
                temp = worker.getSize()
                print(temp)
                if(size < temp):
                    size = temp
                    worker_selected = worker

            error, results = worker_selected.touch(cwd, path)
            if(error):
                return error, None
            return None, results
        else:
            for worker in workers:
                error, results = worker.touch(cwd, path)
                if(error is not None):
                    errors.append(error)

            if(len(workers)==len(errors)):
                return error, ''
            return None, 'File Sudah Dibuat'

    def copy(self, cwd, path_from, path_to):
        errors = []
        worker_from = ''
        method_copy = 0
        lists = []
        flag_exist = 0
        for worker in workers:
            error, method, data = worker.listSource(cwd, path_from)
            print('%s %s %s', error, method, data)
            if(error is not None):
                errors.append(error)
            else:
                worker_from = worker
                lists = data
                method_copy = method

        if(len(workers)==len(errors)):
            return 'Folder atau file '+path_from+' tidak ada', None

        if(method_copy==1):
            data = worker_from.readFile(cwd, path_from)
            errors = []
            paths_from = path_from.split('/')
            paths_to = path_to.split('/')
            if(len(paths_to)==2):
                print('root')
                size = -1000;
                worker_selected = ''
                for worker in workers:
                    temp, temp_path = worker.checkData(path_to)
                    if(temp):
                        errors.append(temp)

                if(len(errors) > 0):
                    return 'Tidak bisa membuat file, file sudah ada', None

                for worker in workers:
                    temp = worker.getSize()
                    print(temp)
                    if(size < temp):
                        size = temp
                        worker_selected = worker
                error, results = worker_selected.makeFile(cwd, path_to, data)
                if(error):
                    return error, None
                return None, results
            else:
                for worker in workers:
                    error, results = worker.makeFile(cwd, path_to, data)
                    print('%s %s', error, results)
                    if(error is not None):
                        errors.append(error)
                
                if(len(workers)==len(errors)):
                    print('gagal')
                    return error, ''
                print('sukses')
                return None, 'File Sudah Dicopy'
        else:
            paths_from = path_from.split('/')
            paths_to = path_to.split('/')
            errors = []
            if(len(paths_to)==2):
                size = -1000;
                worker_selected = ''
                for worker in workers:
                    temp, temp_path = worker.checkData(path_to)
                    print(temp)
                    if(temp):
                        errors.append(temp)

                print(errors)
                if(len(errors) > 0):
                    return 'Tidak bisa membuat folder, folder sudah ada', None

                print('lolos')
                for worker in workers:
                    temp = worker.getSize()
                    print(temp)
                    if(size < temp):
                        size = temp
                        worker_selected = worker

                error, result = worker_selected.makeFolder(cwd, path_to)
                if(error):
                    return error, None
                for file in lists:
                    if(file['type']==1):
                        print('ini file')
                        data = worker_from.readFile(cwd, path_from+file['name'])
                        error, results = worker_selected.makeFile(cwd, path_to+file['name'], data)
                    elif(file['type']==2):
                        print('ini folder')
                        error, result = worker_selected.makeFolder(cwd, path_to+file['name'])
                    
                    if(error):
                        return error, None

                return None, 'Berhasil copy'

            else:
                path_to_s = path_to.replace('/'+paths_to[len(paths_to)-1],'')
                print(path_to_s)
                worker_selected = ''
                errors = []
                for worker in workers:
                    temp, temp_path = worker.checkData(path_to_s)
                    if(temp==0):
                        errors.append(temp)
                    else:
                        worker_selected = worker

                if(len(errors) == len(workers)):
                    return 'Tidak bisa membuat folder, folder tidak tersedia', None

                error, result = worker_selected.makeFolder(cwd, path_to)
                if(error):
                    return error, None

                for file in lists:
                    if(file['type']==1):
                        print('ini file')
                        data = worker_from.readFile(cwd, path_from+file['name'])
                        error, results = worker_selected.makeFile(cwd, path_to+file['name'], data)
                    elif(file['type']==2):
                        print('ini folder')
                        error, result = worker_selected.makeFolder(cwd, path_to+file['name'])
                    
                    if(error):
                        return error, None

                return None, 'Berhasil copy'

    def mv(self, cwd, path_from, path_to):
        errors = []
        worker_from = ''
        method_copy = 0
        lists = []
        flag_exist = 0
        for worker in workers:
            error, method, data = worker.listSource(cwd, path_from)
            print('%s %s %s', error, method, data)
            if(error is not None):
                errors.append(error)
            else:
                worker_from = worker
                lists = data
                method_copy = method

        if(len(workers)==len(errors)):
            return 'Folder atau file '+path_from+' tidak ada', None

        if(method_copy==1):
            data = worker_from.readFile(cwd, path_from)
            errors = []
            paths_from = path_from.split('/')
            paths_to = path_to.split('/')
            print('bisa')
            if(len(paths_to)==2):
                print('root')
                size = -1000;
                worker_selected = ''
                for worker in workers:
                    temp, temp_path = worker.checkData(path_to)
                    if(temp):
                        errors.append(temp)

                if(len(errors) > 0):
                    return 'Tidak bisa membuat file, file sudah ada', None

                for worker in workers:
                    temp = worker.getSize()
                    print(temp)
                    if(size < temp):
                        size = temp
                        worker_selected = worker

                error, results = worker_selected.makeFile(cwd, path_to, data)
                if(error):
                    return error, None
                error, results = self.removeData(cwd, path_from)
                if(error):
                    return 'Tidak bisa memindah file', None
                return None, 'Berhasil memindah file'
            else:
                for worker in workers:
                    error, results = worker.makeFile(cwd, path_to, data)
                    print('%s %s', error, results)
                    if(error is not None):
                        errors.append(error)
                    else:
                        error, results = self.removeData(cwd, path_from)
                if(len(workers)==len(errors)):
                    print('gagal')
                    return error, ''
                print('sukses')
                return None, 'File Sudah Dipindah'
        else:
            paths_from = path_from.split('/')
            paths_to = path_to.split('/')
            errors = []
            if(len(paths_to)==2):
                size = -1000;
                worker_selected = ''
                for worker in workers:
                    temp, temp_path = worker.checkData(path_to)
                    print(temp)
                    if(temp):
                        errors.append(temp)

                print(errors)
                if(len(errors) > 0):
                    return 'Tidak bisa membuat folder, folder sudah ada', None

                print('lolos')
                for worker in workers:
                    temp = worker.getSize()
                    print(temp)
                    if(size < temp):
                        size = temp
                        worker_selected = worker

                error, result = worker_selected.makeFolder(cwd, path_to)
                if(error):
                    return error, None
                for file in lists:
                    if(file['type']==1):
                        print('ini file')
                        data = worker_from.readFile(cwd, path_from+file['name'])
                        error, results = worker_selected.makeFile(cwd, path_to+file['name'], data)
                    elif(file['type']==2):
                        print('ini folder')
                        error, result = worker_selected.makeFolder(cwd, path_to+file['name'])
                    
                    if(error):
                        return error, None
                error, results = self.removeData(cwd, path_from)
                if(error):
                    return 'Tidak bisa memindah file', None      
                return None, 'Berhasil copy'

            else:
                path_to_s = path_to.replace('/'+paths_to[len(paths_to)-1],'')
                print(path_to_s)
                worker_selected = ''
                errors = []
                for worker in workers:
                    temp, temp_path = worker.checkData(path_to_s)
                    if(temp==0):
                        errors.append(temp)
                    else:
                        worker_selected = worker

                if(len(errors) == len(workers)):
                    return 'Tidak bisa membuat folder, folder tidak tersedia', None

                error, result = worker_selected.makeFolder(cwd, path_to)
                if(error):
                    return error, None

                for file in lists:
                    if(file['type']==1):
                        print('ini file')
                        data = worker_from.readFile(cwd, path_from+file['name'])
                        error, results = worker_selected.makeFile(cwd, path_to+file['name'], data)
                    elif(file['type']==2):
                        print('ini folder')
                        error, result = worker_selected.makeFolder(cwd, path_to+file['name'])
                        
                    if(error):
                        return error, None
                error, results = self.removeData(cwd, path_from)
                if(error):
                    return 'Tidak bisa memindah folder', None
                return None, 'Berhasil dipindah'


    def listingFolder(self, cwd, path=None):
        list_folders = []
        errors = []
        flag_exist = 0
        for worker in workers:
            error, list_folder = worker.listingFolder(cwd, path)
            list_folders = list_folders+list_folder
            if(error is not None):
                errors.append(error)

        if(len(workers)==len(errors)):
            return 'Tidak ada folder', []
        return None, list_folders

    def checkDir(self, cwd):
        flag_exist = 0
        for worker in workers:
            res = worker.isExistFolder(cwd)
            if(res):
                flag_exist = 1;
                break
        if(flag_exist):
            return True
        else:
            return False

    def args(self,args,cwd):
        if args[0] == 'upload':
            workers[0].createFile(cwd, file, data)

        if args[0] == 'ls':
            if(len(args)==1):
                path = self.generateStructureFolder(cwd, args)
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            if(len(args)==1):
                error, result = self.listingFolder(cwd,path)
                return error, result, cwd
            else:
                error, result = self.listingFolder(cwd,path)
                return error, result, cwd

        elif args[0] == 'cd':
            if(len(args)==1):
                path = self.generateStructureFolder(cwd, args)
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            if(self.checkDir(path)):
                return None, cwd, path
            else:
                return 'Folder tidak ada', cwd, cwd
        elif args[0] == 'rm':
            if(len(args)==1):
                return args[0]+': missing operand',None,cwd
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            error, result = self.removeData(cwd, path)
            return error, result, cwd

        elif args[0] == 'touch':
            if(len(args)==1):
                return args[0]+': missing operand',None,cwd
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            error, result = self.touch(cwd, path)
            return error, result, cwd

        elif args[0] == 'cp':
            if(len(args)==1):
                return args[0]+': missing operand',None,cwd
            elif(len(args)==2):
                return args[0]+': missing destination file operand after '+args[1],None,cwd
            else:
                path_from = self.generateStructureFolder(cwd, args, args[1])
                path_to = self.generateStructureFolder(cwd, args, args[2])
            error, result = self.copy(cwd, path_from, path_to)
            return error, result, cwd

        elif args[0] == 'mv':
            print('bisa')
            if(len(args)==1):
                return args[0]+': missing operand',None,cwd
            elif(len(args)==2):
                return args[0]+': missing destination file operand after '+args[1],None,cwd
            else:
                path_from = self.generateStructureFolder(cwd, args, args[1])
                path_to = self.generateStructureFolder(cwd, args, args[2])
            error, result = self.mv(cwd, path_from, path_to)
            return error, result, cwd

        else:
            return None, 'Perintah tidak ada', cwd


def listenToWorker():
    for list_worker in list_workers:
        worker = Pyro4.Proxy(list_worker)
        workers.append(worker)

def main():
    listenToWorker()
    Pyro4.Daemon.serveSimple(
        {
            Middleware: "middleware"
        },
        ns=False, host="127.0.0.1", port=8001)

if __name__ == "__main__":
    main()
