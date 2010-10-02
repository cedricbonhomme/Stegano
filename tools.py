#! /usr/local/bin/python
# -*- coding: utf-8 -*-




def a2bits(chars):
    """
    Convert a string to its bits representation as a string of 0's and 1's.
    """
    return bin(reduce(lambda x, y : (x<<8)+y, (ord(c) for c in chars), 1))[3:]

def bs(s):
    """
    Convert a int to its bits representation as a string of 0's and 1's.
    """
    return str(s) if s<=1 else bs(s>>1) + str(s&1)