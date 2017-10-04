import sys
from bs4 import BeautifulSoup, element
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html

#Take this class for granted.Just use result of rendering.
class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

user_ref = '/gabeleibo'
url = 'https://soundcloud.com'+ user_ref + '/followers'
r = Render(url)
result = r.frame.toHtml()
#This step is important.Converting QString to Ascii for lxml to process
archive_links = html.fromstring(str(result.encode('ascii', 'ignore')))
print (archive_links)
soup = BeautifulSoup(result, 'lxml')
print(soup.prettify())
