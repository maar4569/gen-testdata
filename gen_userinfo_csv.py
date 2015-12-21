# -*- coding: utf-8 -*-
import csv
import random

def random_str(len):
    src_str = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ"
    return "".join([ random.choice(src_str) for x in xrange(len) ])
def random_str2(seed,len):
    #if len(seed) < 100:
    return "".join([ random.choice(seed) for x in xrange(len) ])
    #else:
        #return ""

def random_int(len):
    num = "1".zfill(len+1)
    ret =  depertment[random.randrange(0,len(depertment),1)]
    return "".join([ random.choice(src_str) for x in xrange(len) ])

def makerandomurl(proto,domain,urldepth):
    proto  =["https","http"]
    domain =["com","jp","cn","uk"]
    depth=urldepth

maildomain="example.com"
maxrecs=100
depertment=['rsearchanddevlopment','sales','humanresources','usersupport','accounting']
filename="userinfo"
if __name__ == '__main__':
    myoji_master=[]
    namae_master=[]
    
    master = csv.writer(open('usermaster.csv','w'),lineterminator='\n')

    myoji_reader = csv.reader(open('myoji.csv','r') )
    myoji_master=[line for line in myoji_reader]

    namae_reader = csv.reader(open('namae.csv','r') )
    namae_master=[line for line in namae_reader]

    master.writerow(["uid" , "uid2" , "name" , "account" , "mailaddress"  , "department" , "tel"])
    for i in range(maxrecs):
        myoji = myoji_master[random.randint(0,maxrecs-1)]
        namae = namae_master[random.randint(0,maxrecs-1)]
        uid2  = random_str2("ABCDE",3)
	dept  = depertment[random.randint(0,len(depertment)-1)]
        uid  = str(i).zfill(6)
	tel  =  random_str2("0123456789",3) + "-" + random_str2("0123456789",5)
        #print uid + "," + uid2 + "," + myoji[0]+namae[0]+ "," + namae[2] + "_" + myoji[2] + "," + namae[2] + "_" + myoji[2] + "@" + maildomain  + "," + dept + "," + tel
        master.writerow([uid , uid2 , myoji[0]+namae[0] ,  namae[2] + "_" + myoji[2] ,  namae[2] + "_" + myoji[2] + "@" + maildomain  , dept , tel])

