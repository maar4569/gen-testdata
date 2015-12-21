# -*- coding: utf-8 -*-
import csv
import random
import datetime
import syslog
def gen_ip():
    iplist = ["192.168.","172.16.","10.1."]
    ip = iplist[random.randrange(0,len(iplist))]
    ip += ".".join(map(str, (random.randint(0,255) for _ in range(2))))
    return ip
def gen_httpport():
    portlist = [8080,443,80]
    port = portlist[random.randrange(0,len(portlist))]
    return port

def gen_method():
    dataset = ["GET","POST"]
    data = dataset[random.randrange(0,len(dataset))]
    return data

def gen_status():
    dataset = [200,400,401,403,404,410,500,502,503]
    data = dataset[random.randrange(0,len(dataset))]
    return 200
def gen_httpver():
    dataset = ["HTTP/1.1"]
    data = dataset[random.randrange(0,len(dataset))]
    return data
def gen_useragent():
    dataset = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv9.0.1)Gecko/20100101 Firefox/9.0.1",
	       "Mozilla/5.0 (cmopatible; MSIE 10.0; Windows NT6.2; WOW64; Trident/6.0)",
	       "Mozilla/5.0 (Windows NT 6.1) AppleWebkit/537.36(KHTML,like Gecko) Chrome/28.0.1500.63 Safari/537.36"]
    data = dataset[random.randrange(0,len(dataset))]
    return data

def random_str(len):
    src_str = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ"
    return "".join([ random.choice(src_str) for x in xrange(len) ])
def random_str2(seed,len):
    #if len(seed) < 100:
    return "".join([ random.choice(seed) for x in xrange(len) ])
    #else:
        #return ""

def random_int(max):
    return   random.randrange(0,max)


def makerandomurl(proto,domain,urldepth):
    proto_str  = proto[random.randint(0,len(proto)-1)]
    domain_str = domain[random.randint(0,len(domain)-1)]
    urlstr =""
    for i in range(urldepth):
        urlstr = urlstr + "/" + random_str(6)

    src_str = "abcdefghijklmnopqrstuwxyz0123456789"
    return proto_str + "://" + random_str2(src_str,6) + "." + domain_str + urlstr

filename="userinfo"
if __name__ == '__main__':
    #set syslog config start
    syslog.openlog('weblog_generator',syslog.LOG_PID,syslog.LOG_LOCAL6)
    #set syslog config end
    proto  = ["https","http"]
    tlv_domain = ["com","jp","cn","uk","kr","ar"]
    depth  = random.randint(1,6)
    print makerandomurl(proto,tlv_domain,depth)

    iskiriban =  lambda x: True if x % 100000 == 0 else False
    user_reader = csv.reader(open('usermaster.csv','r'))
    next(user_reader)
    #header
    print "date(yyyy-mm-dd),time(hh:mm:ss),c-ip,cs-username,stl_-sitename,s-computername,s-ip,s-port,cs-method,cs-uri-stem,cs-uri-query,sc-status,sc-substatus,sc-bytes,cs-bytes,time-taken,cs-versioni,cs(User-Agent)"
    for line in user_reader:
	syslog_msg = ""
	dt = datetime.datetime.today()
        tmp_date = dt.strftime("%Y-%m-%d")
	tmp_time = dt.strftime("%H:%M:%S:%f")
	tmp_msecs  = dt.strftime("%f")
        #print tmp_date + "," + tmp_time  + "," + gen_ip() + "," + line[1]+line[0] + "," + \
	#      "PC_"+ line[0]  + "," +gen_ip()+"," + str(gen_httpport()) + "," + gen_method() + \
	#      ",,," + str(gen_status()) + ","+str(random_int(10000))+","+ str(random_int(10000)) + \
	#      "," + str(random_int(50))+ "," + gen_httpver() + "," + gen_useragent() + ","+ makerandomurl(proto,tlv_domain,depth)
        syslog_msg = tmp_date + "," + tmp_time  + "," + gen_ip() + "," + line[1]+line[0] + "," + \
	      "PC_"+ line[0]  + "," +gen_ip()+"," + str(gen_httpport()) + "," + gen_method() + \
	      ",,," + str(gen_status()) + ","+str(random_int(10000))+","+ str(random_int(10000)) + \
	      "," + str(random_int(50))+ "," + gen_httpver() + "," + gen_useragent() + ","+ makerandomurl(proto,tlv_domain,depth)
	syslog.syslog(syslog.LOG_INFO,syslog_msg)
	print syslog_msg
	#--------
	#gerenate threatslog
	#--------
	if iskiriban(int(tmp_msecs,10)):
	    gen_threats_log = lambda dt,tm,ms,url: dt + "," + tm + "," + ms + "," + url
	    #print gen_threats_log(tmp_date,tmp_time,tmp_msecs,"threatsURL")
	    syslog_msg = gen_threats_log(tmp_date,tmp_time,tmp_msecs,"threatsURL")
	    syslog.syslog(syslog.LOG_CRIT,syslog_msg)
            print syslog_msg
    #print gen_ip()

