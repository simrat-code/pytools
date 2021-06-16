#!/usr/bin/env python3
#
# Author: Simrat Pal Singh
# Date  : 10-Dec-2019
#

from os import path


class HTMLHandler:
        
    def __init__(self):
        self.outpath = "/opt/datastore/tmp/"
        #self.sample_file = "/opt/datastore/tmp/sample.html"
        self.buf = ''
        self.index = {}
        self.pre_flag = False
        self.start = ("<HTML><HEAD>" 
                    "<TITLE>{filename}</TITLE>" 
                    "<LINK rel=\"stylesheet\" href=\"styles.css\">" 
                    "</HEAD><BODY>")
        self.end = "</BODY></HTML>"


    def read_sample(self):
        if (not path.exists(self.sample_file)):
            raise ValueError
        long_string = ""
        with open(self.sample_file, "r") as fp:
            for line in fp:
                long_string += line.strip()
        return long_string


    def create_page(self, inpath, fname):
        #
        # parsing arguments
        #
        if (not fname or not inpath):
            print("[-] error: invalid number of arguments")
            raise ValueError
        print("[=] inpath/fname: {}{}".format(inpath, fname))
        ##long_string = self.read_sample()
        #
        # replace {filename}
        #
        # long_string = self.start.replace("{filename}", fname)
        long_string = self.start.format(**{"filename": fname})
    
        outfile = self.outpath + fname + ".html"
        infile = inpath + fname + ".txt"
    
        print("[=] outfile: "+ outfile)
        #print("[=] infile : "+ infile)
        
        with open(infile, "r") as ifp:
            with open(outfile, "w") as ofp:
                ofp.write(long_string+"\n")
                ofp.write("<p><a href=\"index.html\">INDEX Page</a></p>")
                count = 0
                for line in ifp:
                    ##line = line.strip()
                    #if (count < 99):
                    #    print(">>>" + line)
                    count = count + 1
                    content = self._decodeLine(line)
                    if (content == ''): continue
                    ofp.write(content)
                ofp.write(self.end)
                print("[=] {} lines read".format(count))

        self.index[fname[2:]] = fname +'.html'


    def genIndex(self):
        long_string = self.start.replace("{filename}", 'Index Contents')
        outfile = self.outpath + 'index.html'

        with open(outfile, "w") as ofp:
            ofp.write(long_string+'\n')
            ofp.write('<h1>Contents</h1><br>\n')

            for key in self.index.keys():
                #print(key, self.index[key])
                ofp.write("<a href=\"{}\">{}</a><br>\n".format(self.index[key], key))
            ofp.write(self.end)


    def _decodeLine(self, line):
        """Insert html tags by replacing text symbols """
        # check if line need to be decoded
        if (line.find("<pre>") != -1):
            self.pre_flag = True
        elif (line.find("</pre>") != -1):
            self.pre_flag = False

        text =''
        if (line == '' or line[0] == '\n'):
            self.buf += '<br>'
            text = ''

        elif (line[:6] == '======'):
            self.buf = ''
            text = '<br><br><br>\n'

        elif (line[:6] == '------'):
            self.buf = ''
            text = '<br><br>\n'

        elif (line[:3] == '== '):
            self.buf = ''
            text = '<h1>'+ line[3:] +'</h1>'

        elif (line[:3] == '-- '):
            self.buf = ''
            text = '<h3>'+ line[3:] +'</h3>'

        else:
            self.buf = ''
            text = self.buf + line + '<br>'

        if (self.pre_flag):
            text = text.replace("<br>", " ")

        return text




class FileHandler:
    def write_file(self, target, source, nchars=0, nlines=0, upto_pattern="", from_pattern=""):
        try:
            infile = open(source, "r")
            outfile = open(target, "a")

            if (nchars != 0):
                # CHAR 
                npos = 0
                while (npos < nchars):
                    npos = npos + 512
                    content = infile.read(512)
                    outfile.write(content)

            elif (nlines != 0):
                # LINE
                for i in range(nlines):
                    content = infile.readline()
                    if (content == ''):
                        break
                    outfile.write(content)

            elif (not upto_pattern):
                # UPTO PATTERN
                while True:
                    content = infile.readline()
                    if (content == ''):
                        break

                    pos = content.find(upto_pattern)
                    if (pos == -1):
                        outfile.write(content)
                    else:
                        outfile.write(content[:pos])
                        break

            elif (not from_pattern):
                # FROM PATTERN
                flag = False
                while True:
                    content = infile.readline()
                    if (content == ''):
                        break

                    if (flag == False):
                        pos = content.find(from_pattern)
                        if (pos == -1):
                            continue
                        else:
                            flag = True
                            outfile.write(content[pos:])
                    else:
                        outfile.write(content)

            else:
                raise ValueError

        except:
            pass

        finally:
            infile.close()
            outfile.close()
# --end--
