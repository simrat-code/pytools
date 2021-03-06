
import os

from html_page import HTMLHandler

if __name__ == "__main__":
    inpath = "/opt/datastore/learning_data/"
    #inpath = "/opt/datastore/tmp/"
    html = HTMLHandler()
    entries = os.scandir(inpath)
    for entry in entries:
        fname = entry.name
        if (fname[:2] != 'x_' and fname.endswith('.txt') ):
            print("[=] skiping file: {}".format(fname))
            continue
        print("[=] {}".format(fname))
        html.create_page(inpath, fname[:-4])
    html.genIndex()
#--end--
