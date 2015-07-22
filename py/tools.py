#encoding:utf-8
import random as rd
import re
import sys
import math

def readfiles(path):
    data=[]
    for line in file(path):
        data.append(line)
    return data

def writefile(path, data):
    filee=open(path,'w')
    if isinstance(data,dict):
        for i in data:
            filee.write(i + "\t"+str(data[i]))
    elif isinstance(data,list):
        for i in data:
            filee.write(i)
    else:
        print "not list or dict"
    filee.close()

def genworddict(worddict):
    dictword2vec = {}
    dictdata = readfiles(worddict)
    for line in dictdata:
        da = line.split("\t")
        dictword2vec[da[0].decode("utf-8")] = da[1]
    return dictword2vec

def rdmnegative(alldoc, te, po, num):
    rdmdata = []
    sp = [te, po]
    cur = te
    for i in range(num):
        while cur in sp:
            cur = rd.choice(alldoc)
        sp.append(cur)
        rdmdata.append(cur)
    return rdmdata

def text2vec(worddict, te):
    tevec=[]
    allwords =worddict.keys()
    aw = re.findall(u"[\u4E00-\u9FA5]{1}", te)
    for w in aw:
        if w not in allwords: continue
        tevec.append(worddict[w])
    return tevec

def gentraindoc(sourcefile, worddict, num):
    alldoc = []
    traindoc = []
    seg = "***************\n"
    #num is the number of negative samples
    #get vector of each word
    dictword2vec = genworddict(worddict)
    #get source file
    source=readfiles(sourcefile)

    for line in source:
        da = line.split("\t")
        alldoc.append(da[0]+"\n")
        alldoc.append(da[1])

    for line in source:
        da = line.split("\t")
        s = da[0]+"\n"
        p = da[1]
        traindoc.append(s.decode("utf-8"))
        traindoc.append(p.decode("utf-8"))
        rdmneg = rdmnegative(alldoc, s, p, num)
        for i in rdmneg:
            traindoc.append(i.decode("utf-8"))
        traindoc.append(seg)
    return traindoc, seg

def genvecfortraindoc(sourcefile, worddict, num):
    #num is the number of negative sample
    vecdata = []
    flag = []
    flagls = []
    doc, seg = gentraindoc(sourcefile, worddict, num)
    word2vec = genworddict(worddict)
    num = 0
    for line in doc:
        print line
        if line != seg:
            txvec = text2vec(word2vec, line)
            print len(txvec)
            num += len(txvec)
            flagls.append(num)
            for vecc in txvec:
                vecdata.append(str(vecc).replace("[",'').replace("]",'').replace(","," ").replace("'"," "))
        else:
            num = 0
            flag.append(str(flagls).replace("[",'').replace("]",'').replace(","," ").replace("'"," ") + "\n")
            flagls = []
    return vecdata, flag

def geninferdoc():
    doc = []
    vecdata = []
    flag = []
    flagls = []
    num = 0
    seg = "***************\n"
    word2vec = genworddict()
    for line in readfiles("fmttest3.txt"):
        da = line.split("\t")
        s = da[0]+"\n"
        p = da[1]
        doc.append(s.decode("utf-8"))
        doc.append(p.decode("utf-8"))
        doc.append(seg)

    for line in doc:
        if line != seg:
            txvec = text2vec(word2vec, line)
            num += len(txvec)
            flagls.append(num)
            for vecc in txvec:
                vecdata.append(str(vecc).replace("[",'').replace("]",'').replace(","," ").replace("'"," "))
        else:
            num = 0
            flag.append(str(flagls).replace("[",'').replace("]",'').replace(","," ").replace("'"," ") + "\n")
            flagls = []
    return vecdata, flag

#***********************add sogo url***********************

def getusfinfo2sogourl():
    data = readfiles("data.txt")
    url = []
    title = []
    istitle = False
    for line in data:
        if line.startswith(r"http://"):
            url.append(line.replace("\n", "\t").replace("\r", ""))
            istitle = True
            continue
        if istitle :
            title.append(line)
            istitle = False
    return url, title

def getsearchinfo2title():
    s2t = {} #search info 2 title
    u2s = {} #url 2 search info
    u2t = {} #url 2 its title
    tc = readfiles("title_click.txt")
    for line in tc:
        temp = line.split("\t")
        u2s [temp[1].replace("\n", "\t").replace("\r", "")] = temp[0]
    url, title= getusfinfo2sogourl()
    for i in range(len(url)):
        u2t[url[i].replace(r"http://","")] = title[i]
    print len(u2t),len(u2s)
    sameurl = list(set(u2s.keys()) & set(u2t.keys()))
    print len(sameurl)
    for j in sameurl:
        ti = u2t[j]
        if "404" not in ti and "None" not in ti:
            s2t[u2s[j].replace("[", "").replace("]", "")] = ti
    return s2t
# make no chinese or english char into backspace
def formattext():
    data = readfiles("search2title.txt")
    fmtdata = []
    for line in data:
        fmtdata.append(str(re.sub(u'[^\u4E00-\u9FA5A-Za-z0-9\t]', ' ', line.decode("utf-8")).encode("utf-8")).strip()+"\n")
    return fmtdata

#del single line or "不存在" in title
def filterfmttest():
    data = readfiles("fmttest.txt")
    newdata = []
    for line in data:
        da = line.split("\t")
        if (len(da)) != 2 or "不存在" in da[1] or "找不到" in da[1] or "错误" in da[1] or "信息提示" in da[1] or da[0]==da[1].replace("\n",''):
            continue
        if "Powered by" in line:
            line = line.split("Powered by")[0]+"\n"
        if "powered by" in line:
            line = line.split("powered by")[0]+"\n"
        print "\t" in line
        if re.search(u"[a-zA-Z0-9]", line) == None:
            newdata.append(re.sub(u" {2,}", " ", line).lower())

    return newdata

#get all single word for each sentence to generate word dict without chinese
def getallsingleword():
    data = readfiles("fmttest2.txt")
    singleword = {}
    for line in data:
        da = re.sub(u"[\u4E00-\u9FA5]", "", line.decode("utf-8"))
        print da
        for word in da.split(" "):
            w = word.split("\t")
            for y in w:
                singleword[y] = 0
    return singleword

def getvalue(w):
    da = []
    for line in w:
        da.append([float(i) for i in line.replace("\n", "").split()])
    return da

def checkwcws():
    wc = getvalue(readfiles("wc.txt"))
    ws = getvalue(readfiles("ws.txt"))

def cossim(ls1, ls2):
    if len(ls1) != len(ls2):
        print "not equal len"
    m1 = 0
    m2 = 0
    sum = 0
    for i in xrange(len(ls1)):
        m1 += math.pow(ls1[i], 2)
        m2 += math.pow(ls2[i], 2)
        sum +=ls1[i] * ls2[i]
    return sum/(math.sqrt(m1) *math.sqrt(m2))

def checkres():
    vecdata = []
    for line in readfiles("ymat.txt"):
        vecdata.append([float(i) for i in line.split()])
    for j in range(len(vecdata)):
        te = []
        for k in range(len(vecdata)):
            sim = cossim(vecdata[j], vecdata[k])
            if sim>=1: sim=-100
            te.append(sim)

        print j, '_', te.index(max(te))

def checkresdoc():
    resu = []
    vec = []
    for line in readfiles("ymat.txt"):
        vec.append([float(i) for i in line.split()])
    doc = readfiles("checkdocment.txt")
    data = {doc[i]:vec[i] for i in range(len(vec))}
    num = 0
    for d1 in data:
        num +=1
        print num
        te = {}
        for d2 in data:
            sim = cossim(data[d1], data[d2])
            if d1 == d2:sim = -1000
            te[d1+"_"+d2] = sim
        da = sorted(te.iteritems(), key=lambda x:x[1], reverse=True)
        resu.append(da[0][0])
    writefile("finalresult.txt", resu)
def checkresdoccount():
    n = 0
    resu = []
    vec = []
    for line in readfiles("ymat.txt"):
        vec.append([float(i) for i in line.split()])
    doc = [i.replace('\n', '') for i in readfiles("checkdocment.txt")]
    data = {doc[i]:vec[i] for i in range(len(vec))}
    num = 0
    for d1 in data:
        te = {}
        for d2 in data:
            sim = cossim(data[d1], data[d2])
            if d1 == d2:sim = -1000
            te[d1+"_"+d2] = sim
        da = sorted(te.iteritems(), key=lambda x:x[1], reverse=True)
        d = da[0][0].split("_")
        d1 = doc.index(d[0])
        d2 = doc.index(d[1])
        if d1 - d2 ==1 or d1 - d2 ==-1:
            n += 1
    print n*2.0/len(doc)

def checkres3doc(topN):
    n = 0
    resu = []
    vec = []
    for line in readfiles("ymat.txt"):
        vec.append([float(i) for i in line.split()])
    doc = [i.replace('\n', '') for i in readfiles("checkdocment.txt")]
    doc1 = [doc[i] for i in range(0, len(doc), 2)]
    doc2 = [doc[i] for i in range(1, len(doc), 2)]
    data = {doc[i]:vec[i] for i in range(len(vec))}
    num = 0
    for d1 in data:
        te = {}
        for d2 in data:
            sim = cossim(data[d1], data[d2])
            if d1 == d2:sim = -1000
            te[d1+"_"+d2] = sim
        da = [i[0].split("_")[-1] for i in sorted(te.iteritems(), key=lambda x:x[1], reverse=True)][:topN]
        if d1 in doc1:
            if doc2[doc1.index(d1)] in da:
                n+=1
        elif d1 in doc2:
            if doc1[doc2.index(d1)] in da:
                n+=1
        else:
            print "Value error!!!!"
    print n, topN
    print n*2.0/len(doc)
def bow():
    words = []
    wordsdict = {}
    for line in readfiles("checkdocment.txt"):
        te = line.decode("utf-8").replace("\n", "").replace(" ", "").replace("\t", "")
        for w in te:
            #print w
            words.append(w)
    wordlen = len(words)
    print wordlen
    for i in range(wordlen):
        te = [0 for i in range(wordlen)]
        te[i] = 1
        wordsdict[words[i].encode("utf-8")] = te
    print len(wordsdict)
    writefile("bow.txt", wordsdict)
    return

if __name__=="__main__":
    print "..."
    # search_click = sys.argv[0]
    # nagnum = sys.argv[1]
    # doc_vec = sys.argv[2]
    # doc_flag = sys.argv[3]
    #
    # vecdata, flag = genvecfortraindoc(search_click,nagnum)
    # writefile(doc_vec, vecdata)
    # writefile(doc_flag, flag)


    # vecdata, flag = genvecfortraindoc("search2title.txt",5)
    # writefile("doc_vec.txt", vecdata)
    # writefile("doc_flag.txt", flag)


    # num = 0
    # doc, seg = gentraindoc("title_click.txt", 5)
    # writefile("traindoc.txt", doc)
    # vec, flag = genvecfortraindoc(32)
    # writefile("textvec.txt", vec)
    # writefile("flag.txt", flag)
    # url, title = getusfinfo2sogourl()
    # for i in range(len(title)):
    #     if title[i] == "None\r\n":continue
    #     num = num+1
    # print len(url), len(title),url[-1], title[-1],num
    # s2t = getsearchinfo2title()
    # writefile("search2title.txt",s2t)
    # writefile("fmttest.txt", formattext())
    # writefile("fmttest2.txt", filterfmttest())
    # writefile("singlewordnoCH.txt", [i.strip()+"\n" for i in getallsingleword().keys()])

    #************************* second tackle (in Chinese)****************
    # url, title = getusfinfo2sogourl()
    # print len(url),len(title)
    # writefile("secondurl2title.txt", un2list2dict(url, title))
    # writefile('secondsearch2title.txt', getsearchinfo2title())
    # writefile("fmttest.txt", formattext())
    # writefile("fmttest2.txt", filterfmttest())
    # doc, flag = gentraindoc("fmttest2.txt",10)
    # writefile("traindata.txt", doc)
    # doc, flag = geninferdoc()
    # print doc
    
    # writefile("checkdoc.txt", doc)
    # writefile("checkfla.txt", flag)
    # checkres()
    #checkresdoc()
    #checkresdoccount()
    #for i in range(4, 11):
    #    checkres3doc(i)
    # bow()
    #vecdata, flag = genvecfortraindoc("fmttest3.txt", "bow.txt", 5)
    #writefile("doc_vec_bow.txt", vecdata)
    #writefile("doc_flag_bow.txt", flag)
