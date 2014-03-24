# -*- coding: UTF-8 -*-
from bitarray import bitarray
import mmh3

class BloomFilter:

    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_array[result] = 1

    def lookup(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            if self.bit_array[result] == 0:
                #return "Nope"
                return False
        return True

bf = BloomFilter(500000, 7)

#lines = open("./mgc.txt").read().splitlines()
#lines = open("/home/test/xueyu/newvers/ywbweb/merchant/mgc1.txt").read().splitlines()
lines = open("/root/xueyu/sensitive/ywbweb/sfilter/mgc1.txt").read().splitlines()

for line in lines:
    bf.add(line)

#print bf.lookup("google")
#print bf.lookup("Max")
#print bf.lookup("转是政府")
#print bf.lookup("阿宾")
