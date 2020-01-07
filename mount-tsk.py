#!/usr/bin/env python3
import sys
import os
import pytsk3

def main(imgpath):
    img = pytsk3.Img_Info(imgpath)
    vol = pytsk3.Volume_Info(img)
    bs = vol.info.block_size
    for part in vol:
        try:
            mount(imgpath, part, bs)
        except Exception as e:
            print(e)

def mount(imgpath, part, bs):
    valid = part.flags == pytsk3.TSK_VS_PART_FLAG_ALLOC
    if valid:
        dirname='vol%s'%part.addr
        os.makedirs(dirname, exist_ok=True)
        cmd = "mount -o ro,offset=%s,sizelimit=%s '%s' '%s'"%(part.start*bs, part.len*bs, 
imgpath, dirname)
        result = os.system(cmd)
        if result != 0:
            print('mount failed:', cmd)

if __name__ == "__main__":
    main(*sys.argv[1:])
