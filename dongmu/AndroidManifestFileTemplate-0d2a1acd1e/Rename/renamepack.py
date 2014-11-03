# Rename a binary AndroidManifest.xml file's package name
#
# Wrritten by hhjack

import struct
import sys

def rename(oldname,newname):
    
    fp=open("AndroidManifest.xml","rb")
    buff=fp.read()
    fp.close()

    pos=0
    magicword=struct.unpack("i",buff[pos:pos+4])[0]
    if magicword!=0x00080003:
        print "Invalid AndroidManifest.xml"
        return
    
    pos=4
    filesize=struct.unpack("i",buff[pos:pos+4])[0]
    print "File Size: %d"%filesize

    stringchunk=4*2
    pos=stringchunk
    chunktype=struct.unpack("i",buff[pos:pos+4])[0]
    if chunktype!=0x001C0001:
        print "Invalid chunktype"
        return
    
    pos=stringchunk+4
    chunksize=struct.unpack("i",buff[pos:pos+4])[0]
    print "Chunk Size: %d"%chunksize
    
    pos=stringchunk+4*2
    stringcount=struct.unpack("i",buff[pos:pos+4])[0]
    print "string count: %d"%stringcount
    
    pos=stringchunk+4*3
    stylecount=struct.unpack("i",buff[pos:pos+4])[0]
    if stylecount!=0:
        print "Never met such contition! Result may contain errors! Go on..."
    print "style count: %d"%stylecount
    
    pos=stringchunk+4*5
    stringpool=struct.unpack("i",buff[pos:pos+4])[0]
    print "String Pool offset: 0x%08X"%stringpool
    stringpool+=stringchunk

    stringoffsets=[]
    for i in range(0,stringcount):
        pos=stringchunk+4*7+i*4
        stringoffsets.append(struct.unpack("i",buff[pos:pos+4])[0])

    mark=0
    for i in range(0,stringcount-1):
        startp=stringoffsets[i]+stringpool
        endp=stringoffsets[i+1]+stringpool
        if oldname==bin2string(buff[startp:endp]):
            mark=i
            break

    if mark==0:
        print "Error finding package name!"
        return

    difflen=len(newname)-len(oldname)
    difflen*=2
    
    if difflen<0:
        print "Actually, you dont need me at all!"
        pos=stringpool+stringoffsets[mark]
        newbuff=buff[0:pos]
        newbuff+=string2bin(newname)+"\x00"*(0-difflen)
        pos=stringpool+stringoffsets[mark+1]
        newbuff+=buff[pos:]
        fp=open("AndroidManifest.xml","wb")
        fp.write(newbuff)
        fp.close()
        return

    # 4-Byte Alignment
    alignnum=0
    if difflen%4!=0:        
        alignnum=4-(difflen%4)
        
    pos=stringpool+stringoffsets[mark]
    newbuff=buff[0:pos]
    newbuff+=string2bin(newname)+"\x00"*alignnum
    pos=stringpool+stringoffsets[mark+1]
    newbuff+=buff[pos:]
    
    filesize+=difflen+alignnum
    filesize=struct.pack("i",filesize)
    chunksize+=difflen+alignnum
    chunksize=struct.pack("i",chunksize)

    newbuff=list(newbuff)

    for j in range(0,4):
        newbuff[4+j]=filesize[j]
        newbuff[stringchunk+4+j]=chunksize[j]

    for i in range(mark+1,stringcount):
        pos=stringchunk+4*7+i*4
        orgv=stringoffsets[i]
        orgv+=difflen+alignnum
        orgv=struct.pack("i",orgv)
        for j in range(0,4):
            newbuff[pos+j]=orgv[j]

    newbuff="".join(newbuff)
    
    fp=open("AndroidManifest.xml","wb")
    fp.write(newbuff)
    fp.close()
    

def string2bin(sstring):
    return struct.pack("h",len(sstring))+"\x00".join(list(sstring))+"\x00"*3

def bin2string(bstring):
    length=struct.unpack("h",bstring[0:2])[0]
    stringc=bstring[2:2+length*2]
    stringc=stringc.replace("\x00","")
    return stringc

if len(sys.argv)!=3:
    print "Usage: python renamepack.py old_package_name new_package_name"
    exit(0)

oname=sys.argv[1]
nname=sys.argv[2]
rename(oname,nname)
print "Rename Successfully!"



