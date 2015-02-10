""" Pipulate lets you collect data straight off of the Web into spreadsheets.
          _____ _             _       _
         |  __ (_)           | |     | |
         | |__) | _ __  _   _| | __ _| |_ ___     ___ ___  _ __ ___
         |  ___/ | '_ \| | | | |/ _` | __/ _ \   / __/ _ \| '_ ` _ \
         | |   | | |_) | |_| | | (_| | ||  __/  | (_| (_) | | | | | |
         |_|   |_| .__/ \__,_|_|\__,_|\__\___| (_)___\___/|_| |_| |_|
                 | |
                 |_|

            It doesn't look like much, but looks can be deceiving.
           I center these lines in the vim editor by hitting shift-V
            to highlight the text and then hitting :center[Enter].
              This is important to remember. I program in Python
                 primarily so that I can work on this project.
                     You will not understand this message
                           until you do. Greetings!
"""

import globs                                        # Talmudic style commentaries
import requests, time, sys, os, json, datetime      # Requests will help 3.x port
from flask_wtf import Form                          # All Flask form examples use it
from wtforms import StringField
from flask import (Flask,                           # This app is all about Flask
  stream_with_context,                              # Yes, comments even work here
  render_template,
  Response,                                         # Occasionally, open the Python
  request,                                          # interactive interpreter and
  session,                                          # then type: import this
  redirect,                                         # Internalize those messages
  url_for,                                          # and then wonder why exit()
  flash)                                            # needs those parentheses.

app = Flask(__name__)                               # Flask init requirement

app.secret_key = "m\x00\r\xa5\\\xbeTW\xb3\xdf\x17\xb0!T\x9b6\x88l\xcf\xa1vmD}"

def out(msg):                                       # Debug output to server terminal
  if globs.DBUG:
    print(msg)

def stream_template(template_name, **context):      # This is the key to streaming
  app.update_template_context(context)              # output to the user in the
  t = app.jinja_env.get_template(template_name)     # web browser much like a
  rv = t.stream(context)                            # long page load, but with
  return rv                                         # better memory efficiency.

@app.context_processor                              # Anything that I want to be
def templateglobals():                              # available in Jinja2 templates
  return dict(loginlink=getLoginlink(),             # without having to always
  bookmarklet=getBookmarklet(),                     # pass them as parameters
  logoutlink=getLogoutlink(),
  cyclemotto=cyclemotto(),
  )

class PipForm(Form):
  pipurl = StringField('Paste a Google Spreadsheet URL:')

@app.route("/", methods=['GET', 'POST'])            # Main point of entry when
def main():                                         # visiting app's homepage.
  out("Entered main function,")
  streamit = False                                  # Default to not streaming.
  form = PipForm(csrf_enabled=False)                # Initialize form for UI.
  if session:                                       # I've seen you before!
    if 'oa2' in session:                            # and I think you're logged in
      import gspread                                # so I'll grab spreadsheet API
      creds = Credentials(access_token=session['oa2'])
      for x in range(0, globs.retrytimes):
        try:
          gsp = gspread.authorize(creds)
          gsp.openall()
          session['loggedin'] = "1"
        except:
          session.clear()
          flash("Login expired. Please log back in")

  if request.method == 'POST':                      # Pipulation must only ever
    if form.pipurl.data:                            # occur on the POST method
      globs.PIPURL = form.pipurl.data               # with a submitted URL. That
      streamit = stream_with_context(pipulate())    # tells us to start streaming.
    else:                                           # Some messages just have to
      flash('Please enter a URL to Pipulate')       # be flashed versus streamed.
  else:
    if request.args and "access_token" in request.args:
      session['oa2'] = request.args.get("access_token")
      session['loggedin'] = "1"
      if 'u' in session:
        return redirect(url_for('main', u=session['u']))
      else:
        return redirect(url_for('main'))
    elif request.args and 'logout' in request.args:
      if session:
        if 'oa2' in session:
          revokeurl = 'https://accounts.google.com/o/oauth2/revoke?token=' + session['oa2']
          requests.get(revokeurl)
        if 'u' in request.args:
          form.pipurl.data = request.args.get('u')
        session.clear()
        flash('Logged out from Google.')
    elif request.args:
      if 'u' in request.args:
        form.pipurl.data = request.args.get('u')
        session['u'] = request.args.get('u')
      if session and 'u' in session:
        form.pipurl.data = session['u']
    if form.pipurl.data and request.url_root == url_root(form.pipurl.data):
      form.pipurl.data = '' #can't pipulate the pipulate site
  if streamit:
    return Response(stream_template('pipulate.html', form=form, data=streamit))
  else:
    return render_template('pipulate.html', form=form)

def pipulate():
  out("Entering pipulate generator.")
  try:
    yield "Beginning to pipulate...", "", ""
    yield "spinon", "", ""
    out("Reading in functions.")
    funcs = [x for x in globals().keys() if x[:2] != '__'] #List all functions
    globs.transfuncs = ziplckey(funcs, funcs) #Keep translation table
    blankrows = 0
    import gspread
    if session:
      if 'oa2' in session:
        creds = Credentials(access_token=session['oa2'])
        out("Credential object created.")
      else:
        out("Expired login.")
        yield "Google Login appears to have expired. Log back in.", "", ""
        yield "spinoff", "", ""
        raise StopIteration
      try:
        gsp = gspread.authorize(creds)
      except:
        out("Login failed.")
        yield "Google Login unsuccessful.", "", ""
        yield "spinoff", "", ""
        raise StopIteration
      else:
        out("Login successful.")
      try:
        gdoc = gsp.open_by_url(globs.PIPURL) #HTTPError
      except gspread.httpsession.HTTPError, e:
        out("Login appeared successful, but rejected on document open attempt.")
        #yield 'HTTP ERROR %s occured' % e.code, "", ""
        yield "Session timed out. Please login again.", "", ""
        raise StopIteration
      except gspread.exceptions.NoValidUrlKeyFound:
        yield "Currently, the URL must be a Google Spreadsheet.", "", ""
        yield "<a href='https://docs.google.com/spreadsheets/create' target='_new'>Create</a> a new Google Spreadsheet and click Bookmarklet again.", "Google Spreadsheet Not Found.", ""
        raise StopIteration
      except gspread.exceptions.SpreadsheetNotFound:
        yield "Please give the document a name to force first save.", "", ""
        yield "spinoff", "", ""
        raise StopIteration
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ename = type(e).__name__
        fixme = "%s, %s, %s" % (ename, fname, exc_tb.tb_lineno)
        yield fixme, "", ""
        yield "spinoff", "", ""
        raise StopIteration
      else:
        out("Google Spreadsheet successfully opened.")
      try:
        onesheet = gdoc.worksheet("Pipulate")
      except:
        #headers = ['URL', 'Tweeted', 'Shared', 'Liked', 'Plussed', 'DateStamp', 'TimeStamp']
        headers = ['URL', 'Subscribers', 'ISOTimeStamp']
        out("Creating Pipulate tab.")
        yme = InitTab(gdoc, 'Pipulate', headers, pipinit())
        onesheet = gdoc.worksheet("Pipulate")
        out("Pipulate tab created.")
        yield yme, "", ""
      finally:
        out("Counting rows in Pipulate tab.")
        globs.numrows = len(onesheet.col_values(1)) #!!!UnboundLocalError
        out("%s rows found." % globs.numrows)
      try:
        gdoc.worksheet("Config")
      except:
        headers = ['name', 'value']
        out("Creating Config tab.")
        yme = InitTab(gdoc, 'Config', headers)
        out("Config tab created.")
        yield yme, "", ""
      try:
        out("Reading Config tab into globals.")
        globs.config = refreshconfig(gdoc, "Config") #HTTPError
      except:
        out("Copying Config tag to globals failed.")
      else:
        out("Config tab copied to globals.")
      try:
        gdoc.worksheet("Scrapers")
      except:
        headers = ['name', 'type', 'pattern']
        yme = InitTab(gdoc, 'Scrapers', headers, scrapes())
        out("Scrapers tab created.")
        yield yme, "", ""
      try:
        out("Loading Scrapers.")
        sst = gdoc.worksheet("Scrapers")
        lod = sst.get_all_records() #Returns list of dictionaries
        pat = [[d['pattern']][0] for d in lod]
        typ = [[d['type']][0] for d in lod]
        nam = [[d['name']][0] for d in lod]
        globs.scrapetypes = ziplckey(nam, typ)
        globs.scrapepatterns = ziplckey(nam, pat)
        globs.transscrape = ziplckey(nam, nam)
      except:
        out("Failed to load Scrapers.")
        raise StopIteration
      else:
        out("Scrapaers loaded.")
      try:
        out("Loading row1 into globals.")
        globs.row1 = lowercaselist(onesheet.row_values(1))
      except:
        out("Failed to load row 1.")
        raise StopIteration
      else:
        out("Row 1 succesfully loaded.")
      trendlistoflists = []
      out("Scanning row 1 for function and scraper names.")
      fargs = {}
      for coldex2, fname in enumerate(globs.row1):
        try:
          fname = fname.lower()
        except:
          pass
        if fname in globs.transfuncs.keys(): 
          out("Found function %s in row 1." % fname)
          fargs[coldex2] = {}
          from inspect import getargspec
          argspec = getargspec(eval(fname))
          if argspec:
            out("%s has arguments: %s" % (fname, argspec))
            myargs = argspec[0]
            mydefs = argspec[3]
            offset = 0
            if mydefs:
              out("%s has defaults: %s" % (fname, mydefs))
              offset = len(myargs) - len(mydefs)
              if offset:
                for i in range(0, offset-1):
                  fargs[coldex2][myargs[i]] = None
                for i in range(offset, len(myargs)):
                  fargs[coldex2][myargs[i]] = mydefs[offset-i]
            else:
              out("%s has no defaults." % (fname))
              for anarg in myargs:
                fargs[coldex2][anarg] = None
            for argdex, anarg in enumerate(myargs): #For each argument of function
              fargs[coldex2][anarg] = None
      out("Putting function argument dictionary in globals.")
      globs.fargs = fargs 
      trended = False
      qstart = 1
      yield "", "Then, we look for Trending requests (asterisks in row 2+)...", ""
      out("About to scan down Pipulate tab looking for asterisks.")
      for rowdex in range(1, onesheet.row_count+1):
        try:
          out("Scanning row %s for asterisks." % rowdex)
          onerow = onesheet.row_values(rowdex) #!!! HTTPError
        except:
          out("Couldn't open row.")
        else:
          out("Successfully opened row.")
        if onerow:
          if rowdex == 2: #Looking for trending requests
            if '*' in onerow:
              trended = True
              out("Found asterisks on row 2 -- trending activated!")
              trendlistoflists.append(onerow)
              yield "Found trending asterisks in row 2", "", json.dumps(onerow)
            else:
              break
          elif trendlistoflists and rowdex > 2:
            if '*' in onerow:
              out("Found astrisks on row %s." % rowdex)
              trendlistoflists.append(onerow)
              yme = ", %s" % rowdex
              yield yme, "", json.dumps(onerow)
            else:
              blankrows += 1
              if blankrows > 1:
                out("Found second row without asterisks, so stopped looking.")
                break
        else:
          blankrows += 1
          if blankrows > 1:
            out("Found second blank row, so trending scan complete.")
            break
      if trended and 'isotimestamp' in globs.row1:
        now = datetime.datetime.now()
        lastinsertdate = None
        backintime = globs.numrows - len(trendlistoflists)
        timeletter = globs.letter[globs.row1.index('isotimestamp')+1]
        mayhaverun = "%s%s:%s%s" % (timeletter, backintime, timeletter, globs.numrows)
        CellList = onesheet.range(mayhaverun)
        for onecell in CellList:
          out("Foo %s" % onecell.value)

        #cell = onesheet.cell(globs.numrows, globs.row1.index('isotimestamp')+1)
        #import dateutil.parser
        #lastinsertdate = dateutil.parser.parse(cell.value)
      #out("%s %s" % (now, lastinsertdate))
      #out((now-lastinsertdate).days * 24 * 60)
      #diff = now - lastinsertdate
      #out(diff.seconds/60)



      if trended:
        qstart = globs.numrows + 1
      else:
        qstart = 1
      if trendlistoflists:
        for x in range(0, globs.retrytimes):
          try:
            InsertRows(onesheet, trendlistoflists)
            trendlistoflists = []
            break
          except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1] #NameError
            out('%s, %s, %s, %s' % (filename, func_name, line_num, text))
            out("Error on trending, retry %s" % x)
            time.sleep(globs.retryseconds)

      #We need to get it again if trending rows were added.
      if trended:
        try:
          onesheet = gdoc.worksheet("Pipulate")
        except:
          yield "Couldn't reach Google Docs. Try logging in again.", "", ""
          yield "spinoff", "", ""
          raise StopIteration

      globs.numrows = len(onesheet.col_values(1))
      blankrows = 0 #Lets us skip occasional blank rows
      out("Question mark replacement")
      for index, rowdex in enumerate(range(qstart, onesheet.row_count+1)): #Start stepping through every row.
        if index == 0:
          yme = "Pipulating row: %s" % rowdex
          yield yme, "Next, we replace question marks (a.k.a. pipulate)...", ""
        else:
          yme = ", %s" % rowdex
          yield yme, "", ""
        globs.hobj = None
        globs.html = '' #Blank the global html object. Recylces fetches.
        rowrange = "A%s:%s%s" % (rowdex, globs.letter[len(globs.row1)], rowdex)
        CellList = onesheet.range(rowrange)
        onerow = []
        for cell in CellList:
          onerow.append(cell.value)
        if '?' in onerow:
          #Perfect opportunity to test nested generator messages
          blankrows = 0
          yield "", "", json.dumps(onerow)

          out("About to pipulate row %s." % rowdex)
          rowdexstring = str(rowdex)
          import traceback
          newrow = onerow[:]
          if rowdexstring > 1:
            #All subsequent rows are checked for question mark replacement requests.
            for coldex, acell in enumerate(newrow):
              if questionmark(onerow, rowdexstring, coldex):
                if 'url' in globs.row1: #Only fetch html once per row if possible
                  try:
                    globs.html = gethtml(onerow[globs.row1.index('url')])
                  except:
                    pass
                collabel = globs.row1[coldex]
                if collabel in globs.transfuncs.keys():
                  for x in range(0, globs.retrytimes):
                    fname = globs.transfuncs[globs.row1[coldex]]
                    fargs = globs.fargs[coldex]
                    evalme = "%s(" % fname #Begin building string that will eventually be eval'd
                    if fargs:
                      #The function we're looking at DOES have required arguments.
                      for anarg in fargs:
                        #Add an arg=value to string for each required argument.
                        anarg = anarg.lower()
                        argval = getargval(anarg, fargs[anarg], newrow)
                        evalme = "%s%s=%s, " % (evalme, anarg, argval)
                      evalme = evalme[:-2] + ')' #Finish building string for the eval statement.
                    else:
                      #No arguments required, so just immediately close the parenthesis.
                      evalme = evalme + ')'
                    try:
                      newrow[coldex] = eval(evalme)
                      out('%s worked' % collabel)
                      break
                    except Exception as e:
                      exc_type, exc_value, exc_tb = sys.exc_info()
                      filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]
                      out('%s, %s, %s, %s' % (filename, func_name, line_num, text))
                      out("Function problem on row %s. Retrying." % rowdexstring)
                      time.sleep(globs.retryseconds)
                elif collabel in globs.transscrape.keys():
                  for x in range(0, globs.retrytimes):
                    try:
                      newrow[coldex] = genericscraper(coldex, newrow) #Scraping
                      out('%s worked.' % collabel)
                      break
                    except Exception as e:
                      exc_type, exc_value, exc_tb = sys.exc_info()
                      filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]
                      out('%s, %s, %s, %s' % (filename, func_name, line_num, text))
                      out("Scrape problem on row %s. Retrying." % rowdexstring)
                      time.sleep(globs.retryseconds)





          out("Finished pipulating replacing questionmarks in memory.")
          newrow = ['' if x==None else x for x in newrow]
          yield "", "", json.dumps(newrow)
          for index, onecell in enumerate(CellList):
            onecell.value = newrow[index]
            result = None
          for x in range(0, globs.retrytimes):
            try:
              result = onesheet.update_cells(CellList)
              out("Successfully updated row %s" % rowdex)
              break
            except:
              out("API problem on row %s. Retrying." % rowdex)
              time.sleep(globs.retryseconds)
        elif onerow.count('') == len(onerow):
          blankrows += 1
          if blankrows > globs.skippableblankrows:
            break
      out('Finished question marks')
    else:
      yield 'Please Login to Google', "", ""
    yield "Pipulation complete.", "This box contains the last JSON data processed.", ""
    yield "spinoff", "", ""
    out("Pipulation complete")
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    ename = type(e).__name__
    if ename == "StopIteration":
      loginmsg = ""
      if session and 'loggedin' in session and session['loggedin'] != '1':
        loginmsg = "Login link under the upper-left \"burger button\"."
      yield "Try again or come back later.", loginmsg, ""
    else:
      fixme = "%s, %s, %s" % (ename, fname, exc_tb.tb_lineno)
      yield fixme, "", ""
      yield "Pipulation prematurely terminated.", "", ""
      yield "Please open an issue at https://github.com/miklevin/pipulate", "", ""
      yield "Or just tap me on the shoulder.", "", ""
    yield "spinerr", "", ""

def url_root(url):
  from urlparse import urlparse
  parsed = urlparse(url)
  return "%s://%s%s" % (parsed[0], parsed[1], parsed[2])

def getLoginlink():
  redir = 'http://'+request.headers['Host']
  if request.args and 'u' in request.args:
    session['u'] = request.args.get('u')
  baseurl = "https://accounts.google.com/o/oauth2/auth"
  qsdict = {  'scope': 'https://docs.google.com/feeds/ https://docs.googleusercontent.com/ https://spreadsheets.google.com/feeds/',
              'response_type': 'token',
              'redirect_uri': redir,
              'approval_prompt': 'force',
              'client_id': '394883714902-h3fjk3u6rb4jr4ntpeft41kov6et2nve.apps.googleusercontent.com'
            }
  from urllib import urlencode
  return "%s?%s" % (baseurl, urlencode(qsdict))

def getBookmarklet():
  return '''javascript:(function(){window.open('http://%s/?u='+encodeURIComponent(document.location.href), 'Pipulate', 'toolbar=0,resizable=1,scrollbars=1,status=1,width=640,height=520');})();''' % (request.headers['Host'])

def getLogoutlink():
  from urllib import quote_plus
  u = ''
  host = request.headers['Host']
  if session and 'u' in session:
    u = session['u']
  elif request.args and 'u' in request.args:
    u = request.args.get('u')
  if u:
    u = quote_plus(u)
  if u:
    logout = "http://%s?logout&u=%s" % (host, u)
  else:
    logout = "http://%s?logout" % host
  return logout

class Credentials (object):
  def __init__ (self, access_token=None):
    self.access_token = access_token

def refreshconfig(gdoc, sheetname):
  #!!! Needs optimization
  onesheet = gdoc.worksheet(sheetname)
  names = onesheet.col_values(1)
  values = onesheet.col_values(2)
  return ziplckey(names, values)

def ziplckey(keys, values):
  keys = lowercaselist(keys)
  return dict(zip(keys, values))

def lowercaselist(onelist):
  for index, item in enumerate(onelist):
    try:
      onelist[index] = item.lower()
    except:
      pass
  return onelist

def InsertRow(onesheet, onelist):
  column = globs.letter[len(onelist)]
  endrow = globs.numrows + 1
  rowrange = "A%s:%s%s" % (endrow, column, endrow)
  if endrow == onesheet.row_count + 1:
    onesheet.append_row(onelist)
    #onesheet.add_rows(1)
  else:
    CellList = onesheet.range(rowrange)
    out('Inserting row in range %s' % rowrange)
    for index, cell in enumerate(CellList):
      ival = ''
      if onelist[index] == None:
        ival = ''
      else:
        ival = onelist[index]
      cell.value = ival
      onesheet.update_cells(CellList)
  globs.numrows += 1

def InsertRows(onesheet, listoflists):
  numnewrows = len(listoflists)
  lastrowused = globs.numrows
  numrowsneeded = len(listoflists)
  allrowsevenempty = onesheet.row_count
  availableblankrows = allrowsevenempty - lastrowused
  if availableblankrows < numrowsneeded:
    rowstoadd = numrowsneeded - availableblankrows
    onesheet.add_rows(rowstoadd)
    globs.numrows += rowstoadd
  upperleftrangenumber = lastrowused + 1
  lowerrightrangenumber = lastrowused + numnewrows
  column = globs.letter[len(listoflists[0])]
  rowrange = "A%s:%s%s" % (upperleftrangenumber, column, lowerrightrangenumber)
  flattenitlist = []
  for onelist in listoflists:
    for onecell in onelist:
      flattenitlist.append(onecell)
  flattenitlist = ['?' if x=='*' else x for x in flattenitlist]
  CellList = onesheet.range(rowrange)
  for index, onecell in enumerate(CellList):
    try:
      onecell.value = flattenitlist[index]
    except:
      pass
  onesheet.update_cells(CellList)
  return

def InitTab(gdoc, tabname, headerlist, listoflists=[]):
  numcols = len(headerlist)
  if listoflists and '*' in listoflists[1]:
    numrows = len(listoflists)+1
  elif listoflists:
    numrows = len(listoflists)+2
  else:
    numrows = 2
  endletter = globs.letter[numcols]
  newtab = gdoc.add_worksheet(title=tabname, rows=numrows, cols=numcols)
  CellList = newtab.range('A1:%s%s' % (endletter, numrows))
  initlist = []
  for onelist in listoflists:
    for onecell in onelist:
      initlist.append(onecell)
  wholelist = headerlist + initlist
  for index, onecell in enumerate(CellList):
    try:
      onecell.value = wholelist[index]
    except:
      pass
  newtab.update_cells(CellList)
  return "Making %s tab." % tabname

def questionmark(oldrow, rowdex, coldex):
  if rowdex != 1:
    if oldrow[coldex] == '?':
      return True
  return False

def genericscraper(coldex, onerow):
  sname = globs.transscrape[globs.row1[coldex]]
  stype = globs.scrapetypes[sname]
  spattern = globs.scrapepatterns[sname]
  if 'url' in globs.row1:
    url = onerow[globs.row1.index('url')]
    html = gethtml(url)
    if stype.lower() == 'xpath':
      import lxml.html
      searchme = lxml.html.fromstring(html)
      match = searchme.xpath(spattern)
      if match:
        return match[0]
      else:
        return None
    elif stype.lower() == 'regex':
      import re
      match = re.search(spattern, html, re.S | re.I)
      if match:
        if "scrape" in match.groupdict().keys():
          keep = match.group("scrape")
          return keep
        else:
          return None
      else:
        return None

def gethtml(url):
  if globs.html:
    out("Recycling HTML.")
    return globs.html
  else:
    out("Doing first HTML fetch for row.")
    try:
      globs.hobj = requests.get(url)
    except:
      return None
    globs.html = globs.hobj.text
  return globs.html

def getargval(anarg, defargval, onerow):
  """Returns value to set argument equal-to in function invocation string.

  This function returns which value should be used as the arguments to the
  function invocation string being built. The value found on the row always
  beats the default provided by the function. Lacking values on the row and a
  default, the Python value of None will be returned."""
  for coldex, acol in enumerate(globs.row1):
    if acol == anarg: #Found column named same thing as a required argument.
      if onerow[coldex]: #The cell in that column has a non-zero/empty value.
        return adq(onerow[coldex]) #So, we got what we need. Return it.
  #Oops, no required arguments were found on the row.
  if defargval:
    return adq(defargval) #So, if it's got a default value, return that.
  else:
    return None #We ALWAYS have to return at least None, least errors ensue.

def adq(aval):
  """Conditionally builds quotes on arg-value for function invocation string.

  This handles the value quoting details when building argument part of the
  function invocation string when replacing a question mark. For example, the
  keyword None must not become quoted. Typically, numbers shouldn't be quoted
  either, but we're feeding everything but None around as strings for now."""
  if aval == None:
    return None #None-in/None-out. This special keyword shouldn't be quoted.
  else:
    return "'%s'" % (aval) #ALMOST everything else should be quoted.

from functions import *

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8888, debug=True)

