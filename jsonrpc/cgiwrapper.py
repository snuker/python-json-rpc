import sys, os, json
from jsonrpc import ServiceHandler
import base64,urllib,urlparse
class CGIServiceHandler(ServiceHandler):
    def __init__(self, service):
        if service == None:
            import __main__ as service

        ServiceHandler.__init__(self, service)

    def handleRequest(self, fin=None, fout=None, env=None):
        if fin==None:
            fin = sys.stdin
        if fout==None:
            fout = sys.stdout
        if env == None:
            env = os.environ
        
        try:
	    
		if os.environ['REQUEST_METHOD'] == 'GET':
			qs=urllparse.parse_qs(os.environ['QUERY_STRING'])
			method=qs['method'][0]
			params=json.loads(urllib.unquote_plus(base64.decodestring(qs['params'][0])))
			rid=qs['id'][0]
			data=json.dumps({'params':params,'method':method,'id':rid})
		else:
         	   contLen=int(env['CONTENT_LENGTH'])
         	   data = fin.read(contLen)
        except Exception, e:
            data = ""

        resultData = ServiceHandler.handleRequest(self, data)
        
        response = "Content-Type: text/plain\n"
        response += "Content-Length: %d\n\n" % len(resultData)
        response += resultData
        
        #on windows all \n are converted to \r\n if stdout is a terminal and  is not set to binary mode :(
        #this will then cause an incorrect Content-length.
        #I have only experienced this problem with apache on Win so far.
        if sys.platform == "win32":
            try:
                import  msvcrt
                msvcrt.setmode(fout.fileno(), os.O_BINARY)
            except:
                pass
        #put out the response
        fout.write(response)
        fout.flush()

def handleCGI(service=None, fin=None, fout=None, env=None):
    CGIServiceHandler(service).handleRequest(fin, fout, env)
