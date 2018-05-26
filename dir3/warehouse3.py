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
    Pyro4.Daemon.serveSimple(
        {
            Warehouse: "example.warehouse3"
        },
        ns=False)


if __name__ == "__main__":
    main()