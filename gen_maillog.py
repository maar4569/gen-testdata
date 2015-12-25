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
    src_str = "0123456789abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ"
    return "".join([ random.choice(src_str) for x in xrange(len) ])
def random_str2(seed,len):
    #if len(seed) < 100:
    return "".join([ random.choice(seed) for x in xrange(len) ])
    #else:
        #return ""

def random_int(max):
    return   random.randrange(0,max)
def random_int2(a,b):
    if ( a < b  and a >= 0 and b > 0):
        return   random.randint(a,b)
    else:
        return   random.randint(0,99999)
def dummy_domain():
    tlvd     = ["com","jp","cn","uk","kr","ar"]
    subd     = ["google","facebook","amazon","apple","hogehoge","foo","bar","yahoo","alibaba"]
    sub_str = subd[random.randint(0,len(subd)-1)]
    top_str = tlvd[random.randint(0,len(tlvd)-1)]
    return sub_str + "." + top_str

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
    syslog.openlog('maillog_generator',syslog.LOG_PID,syslog.LOG_LOCAL6)
    #set syslog config end
    hostname       = "smtpsv1"
    syslogname     = "mail:info"
    prog_smtp      = "postfix/smtp[" +  str(random_int2(0,10000)) + "]:"
    prog_smtpd     = "postfix/smtpd[" +  str(random_int2(0,10000)) + "]:"
    prog_cleanup   = "postfix/cleanup[" + str(random_int2(0,10000)) + "]:"
    prog_qmgr      = "postfix/qmgr[" + str(random_int2(0,10000)) + "]:"
    user_reader    = csv.reader(open('usermaster.csv','r'))
    next(user_reader)
    #header
    for line in user_reader:
        queid       = random_str(8)
        clientip    = gen_ip()
	syslog_msg = ""

	dt = datetime.datetime.today()
        tmp_date = dt.strftime("%Y-%m-%d")
	tmp_time = dt.strftime("%H:%M:%S:%f")
        #transaction loop
        #1.accesslog
        common_fields = tmp_date + " " + tmp_time + " " + hostname + " " + syslogname  
        syslog_msg = common_fields + " " + prog_smtpd  + " "  \
                     + "connect from unknown[" + clientip + "]"
	syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg

        #2.start
        syslog_msg = common_fields + " " + prog_smtpd   + " " + queid + ": " \
                     + "client=unknown[" + clientip + "]"
	syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg

        #3.cleanup
        syslog_msg = common_fields + " " + prog_cleanup + " " + queid + ": " \
                     + "message-id=<" + random_str(30) + "@example.com" + ">"
	syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg

        #4.process
        syslog_msg = common_fields + " " + prog_qmgr    + " " + queid + ": " \
                     + "from=<" + line[4] + ">, size=" + str(random_int(5)) +" ,nrcpt=1 (queue active)"

	syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg
         
        #5.end
        syslog_msg = common_fields + " " + prog_smtpd + " " + queid + ": " \
                     + "disconnect from unknown[" + clientip + "]"

	syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg
        #6.deliver
        queid2       = random_str(8)
        username     = random_str(3) + "_" + random_str(4)
        syslog_msg = common_fields + " " + prog_smtp + " " + queid + ": " \
                     + "to=<" + username + "@" + dummy_domain() + ">, relay=destip:25, delay=0.21, delays=0.1/0/0.5/0.26, dsn=2.0.0,  status=send (250 2.0.0 "+ queid2 +" Message accepted for delivery)"
	#syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg
        
        #7.removed
        syslog_msg = tmp_date + " " + tmp_date  + " " + hostname + " " + syslogname + " " \
                     + prog_qmgr + " " + queid + ": " \
                     + "removed"
	#syslog.syslog(syslog.LOG_INFO,syslog_msg)
        print syslog_msg

