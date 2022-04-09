# PYTHON2.7
import xml.etree.ElementTree as ET
tree = ET.parse('./scidox.reflib')
root = tree.getroot()
wfile = open('./scidox.html', 'w+')
container = root.findall("./doclist/doc")
tags = root.findall("./taglist/tag")
listtags={}
for t in tags:
    a = t.findall("./uid")[0].text.encode('ascii', 'xmlcharrefreplace')
    b = t.findall("./name")[0].text.encode('ascii', 'xmlcharrefreplace')
    listtags[a.decode('UTF-8')] = b.decode('UTF-8')
data = []
#names = []
for doc in container:
    key = doc.findtext("./bib_authors") + '/' + doc.findtext("./bib_title")
    data.append((key,doc))
data.sort()

firstpart = open('./create_html_files/first_part.html', 'r')
for line in firstpart:
    print(line, file=wfile)

print("<script type=\"text/javascript\">", file=wfile)
print("function toggleVisibility(x) { var e = document.getElementById(x); if(e.style.display == 'block') e.style.display = 'none'; else e.style.display = 'block';}", file=wfile)
print("</script>", file=wfile)
print("<center><a href=\"#\" onclick=\"toggleVisibility('links')\">LINKS</a></center>", file=wfile)
print("<div id=\"links\" style=\"display:block\">", file=wfile)
print("<table style=\"font-size:16px\"><td width=\"100\%\"><i>", file=wfile)
sortedtags = []
for x in listtags:
    sortedtags.append(listtags[x])
sortedtags.sort()
for x in sortedtags:
    print("<a href=\"scidox.html?search=&quot;[^]*{" + x + "}&quot;\">" + x + " /</a>", file=wfile)
print("</i></td></table>", file=wfile)
print("</div>", file=wfile)

middlepart = open('./create_html_files/middle_part.html', 'r')
for line in middlepart:
    print(line, file=wfile)

i = 0
for d in data:
    doc = d[1]
    title = ""
    authors = ""
    url = ""
    year = ""
    dockey = ""
    tag = []
    for x in doc.findall("./bib_title"):
        if x.text is not None:
          title = x.text.encode('ascii', 'xmlcharrefreplace')
    for x in doc.findall("./bib_authors"):
        if x.text is not None:
          authors = x.text.encode('ascii', 'xmlcharrefreplace')
    for x in doc.findall("./bib_extra"):
        if x.attrib['key'] == 'Url' or x.attrib['key'] == 'url':
          if x.text is not None:
            url = x.text.encode('ascii', 'xmlcharrefreplace').replace(b'arxiv', b'ar5iv')
    for x in doc.findall("./bib_year"):
        if x.text is not None:
          year = x.text.encode('ascii', 'xmlcharrefreplace')
    for x in doc.findall("./key"):
        if x.text is not None:
          dockey = x.text.encode('ascii', 'xmlcharrefreplace')
    for x in doc.findall("./tagged"):
        if x.text is not None:
          tag.append(x.text.encode('ascii', 'xmlcharrefreplace'))
    i += 1
    print("<tr id=\"", str(i), "\" class=\"entry\"><td>", "<a href=\"" + url.decode('UTF-8') + "\"><div style=\"height:100%;width:100%\"><small>", file=wfile)
    print("<font color=\"black\">", "\n&nbsp; &bull;<b/>", title.decode('UTF-8').replace('{', '').replace('}', ''), "("+year.decode('UTF-8')+")</b>", "&nbsp; - &nbsp;",  authors.decode('UTF-8'), "&nbsp; - &nbsp;", url.decode('UTF-8'), "&nbsp; - &nbsp;", dockey.decode('UTF-8'), "&nbsp; - &nbsp;", file=wfile)
    for tg in tag:
            print("{" + listtags[tg.decode('UTF-8')] + "}", file=wfile)
    print("</small></font></div></a></td></tr>", file=wfile)
     
firstpart = open('./create_html_files/last_part.html', 'r')
for line in firstpart:
    print(line, file=wfile)
