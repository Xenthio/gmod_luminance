import sys
import os



def findmask(data, hexstr, start=0):
    if '??' not in hexstr:
        return data.find(bytes.fromhex(hexstr), start)
    parts = hexstr.split('??')
    while True:
        findpos = data.find(bytes.fromhex(parts[0]), start)
        if findpos == -1:
            return -1
        good = True
        checkpos = findpos
        for part in parts:
            if part != '':
                bpart = bytes.fromhex(part)
                if data[checkpos:checkpos+len(bpart)] != bpart:
                    good = False
                    break
            checkpos += (len(part) // 2) + 1
        if good:
            return findpos
        start = findpos + 1

def install():
    patches = {
    'garrysmod/bin/client.dll': [
        ['558bec538b5d08568b7510578b', '32c0c3'],
        ['00e8????efff8b0d??????10??????????????????????????ff', '01'],
    ],
    'bin/engine.dll': [
        ['558bec538b5d08568b7510578b7d0c565753e8????ffff83c40c83f8027466', '32c0c3'],
        ['558bec538b5d08568b7510578b7d0c565753e8??ddffff83c40c83f8027453', '32c0c3'],
        ['7530f30f10', 'eb'],
        ['7e3ceb06', 'eb'],
        ['75438b4604', 'eb'],
    ],
    'bin/shaderapidx9.dll': [
        ['83c4108be55dc3cccccccccccccccccc55', '85c07502b0048be55dc3'],
    ],
    }
    #if len(sys.argv) != 2:
        #print('Usage: applypatch.py folder')
        #sys.exit(1)




    vers = "."#sys.argv[1]
    if not os.path.isdir(vers):
        print(f'Error: [{vers}]: No such directory')
        return [False, "Error: .: No such directory"]
        
    #os.mkdir(os.path.join(vers, "patched"))
    #os.mkdir(os.path.join(vers, "bin")) 
    #os.mkdir(os.path.join(vers, "garrysmod"))
    #os.mkdir(os.path.join(vers, "garrysmod/bin"))

    ver = {}
    missing = False
    for fname in patches:
        path = os.path.join(vers, fname)
        if not os.path.exists(path):
            print(f'Error: Missing file [{fname}]')
            missing = True
        else:
            print(f'Loading {fname}')
            with open(path, 'rb') as f:
                ver[fname] = bytearray(f.read())
    if missing:
        return [False, f"Error: Missing file [{fname}]"]

    os.makedirs(os.path.join(vers), exist_ok=True)
    for fname in patches:
        print(f'\nPatching {fname}')
        for patch in patches[fname]:
            findpos = findmask(ver[fname], patch[0])
            findpos2 = findmask(ver[fname], patch[0], findpos+1)
            if findpos != -1 and findpos2 == -1:
                pdata = bytes.fromhex(patch[1])
                print(f'{findpos:X}: Changing `{ver[fname][findpos:findpos+len(pdata)].hex()}` to `{patch[1]}`')
                ver[fname][findpos:findpos+len(pdata)] = pdata
            else:
                print(f'Failed to locate patch for {patch[0]}')

    for fname in patches:
        with open(os.path.join(vers, fname), 'wb') as f:
            f.write(ver[fname])

    
    return [True, "And then Garry says to you, \"You cannot win, this is my Mod!\""]