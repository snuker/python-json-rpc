
"""
  Copyright (c) 2017 Suhanov Dmitriy
  Copyright (c) 2007 Jan-Klaas Kollhof

  This file is part of jsonrpc.

  jsonrpc is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import urllib2, base64
from jsonrpc.json import dumps, loads

class JSONRPCException(Exception):
    def __init__(self, rpcError):
        Exception.__init__(self)
        self.error = rpcError
        
class ServiceProxy(object):
    def __init__(self, serviceURL, serviceName=None,auth=None):
        self.__serviceURL = serviceURL
        self.__serviceName = serviceName
	self.__auth=auth

    def __getattr__(self, name):
        if self.__serviceName != None:
            name = "%s.%s" % (self.__serviceName, name)
        return ServiceProxy(self.__serviceURL, name,self.__auth)

    def __call__(self, *args):
         print self.__auth
         postdata = dumps({"method": self.__serviceName, 'params': args, 'id':'jsonrpc'})
         request = urllib2.Request(self.__serviceURL)
         if self.__auth:
             login,passwd=self.__auth
             base64string = base64.encodestring('%s:%s' % (login, passwd)).replace('\n', '')
             request.add_header("Authorization", "Basic %s" % base64string)   
         request.add_data(postdata)
         respdata = urllib2.urlopen(request).read()
         resp = loads(respdata)
         if resp['error'] != None:
             raise JSONRPCException(resp['error'])
         else:
             return resp['result']
         

