#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  未命名.py
#  
#  Copyright 2015 monitor <monitor@GFQH-TEST02>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import zmq
import pdb

def main():
    ctx=zmq.Context()
    s=ctx.socket(zmq.REQ)
    s.connect("tcp://10.68.89.100:8197")
    for i in range(20):
        a = s.send_multipart(["R","NQZ5"])
        print a
        b = s.recv_multipart()
        print b
    return 0

if __name__ == '__main__':
    main()

