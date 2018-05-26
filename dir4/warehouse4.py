from __future__ import print_function
import Pyro4


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
    with Pyro4.Daemon(host='localhost') as daemon:
        worker_name = 'kelompok3.worker4'
        uri = daemon.register(Warehouse)
        with Pyro4.locateNS() as ns:
            ns.register(worker_name, uri)
            print(worker_name + 'ready')
        daemon.requestLoop()


if __name__ == "__main__":
    main()