import argparse


class StoreDictKeyPair(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        bf = {}
        for kv in values.split(","):
            k, v = kv.split("=")
            bf[k] = v
        setattr(namespace, self.dest, bf)
