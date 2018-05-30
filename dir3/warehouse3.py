from __future__ import print_function
import os
import socket
import Pyro4.socketutil
import Pyro4
import sys
from math import sqrt


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


# def main():
#     with Pyro4.Daemon(host=Pyro4.socketutil.getIpAddress(None)) as daemon:
#         worker_name = 'kelompok3.worker3' % (os.getpid(), socket.gethostname())
#         uri = daemon.register(Warehouse)
#         with Pyro4.locateNS() as ns:
#             ns.register(worker_name, uri)
#             print(worker_name + 'ready')
#         daemon.requestLoop()

with Pyro4.Daemon(host=Pyro4.socketutil.getIpAddress(None)) as daemon:
    # create a unique name for this worker (otherwise it overwrites other workers in the name server)
    worker_name = "Worker_%d@%s" % (os.getpid(), socket.gethostname())
    print("Starting up worker", worker_name)
    uri = daemon.register(Warehouse)
    with Pyro4.locateNS() as ns:
        ns.register(worker_name, uri, metadata={"kelompok3.worker3"})
    daemon.requestLoop()


if __name__ == "__main__":
    main()