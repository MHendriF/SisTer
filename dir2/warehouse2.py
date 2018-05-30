from __future__ import print_function
import Pyro4
import Pyro4.socketutil
import os
import socket

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Warehouse(object):
    def __init__(self):
        self.contents = []

    def list_contents(self):
        return self.contents

    def get(self, name, item):
        self.contents.remove(item)
        print("{0} took the {1}.".format(name, item))

    def store(self,name, item):
        self.contents.append(item)
        print("{0} stored the {1}.".format(name, item))



def main():
    with Pyro4.Daemon(host=Pyro4.socketutil.getIpAddress(None)) as daemon:
<<<<<<< HEAD
        #worker_name = 'kelompok3.worker2'
        worker_name = "Worker_%d@%s" % (os.getpid(), socket.gethostname())
=======
        worker_name = 'kelompok3.worker2'
>>>>>>> 8aff1f164f6e74d387a5676f3ebddee8314c3130
        uri = daemon.register(Warehouse)
        with Pyro4.locateNS() as ns:
            ns.register(worker_name, uri, metadata={"example3.worker2"})
        print(worker_name + 'ready')
        daemon.requestLoop()



if __name__ == "__main__":
    main()