# python-json-rpc


Best python json-rpc library I found.   
From: http://json-rpc.org/

### Changelog
Added basic web auth support


### Installation 
Download the source using git.
```
$ git clone https://github.com/snuker/python-json-rpc.git
```
As root/administrator install the package running the provided setup script. 
```
$ cd trunk/python-jsonrpc
$ python setup.py install
```

If you do not wish to install the package you can simply copy the jsonrpc folder to where python can find it when it searches for modules to be imported. 
E.g. this can be the same place where you python script resides in. 

### Using the ServiceProxy class 
 If everything worked you should now be able to call JSON-RPC services. Start your favourite python shell and enter the code below: 
```
>>> from jsonrpc import ServiceProxy
>>> s = ServiceProxy("http://jsolait.net/services/test.jsonrpc")
>>> print s.echo("foobar")

```
 The example above creates a proxy object for a service hosted on jsolait.net It calls the service's echo method and prints out the result of the call. 

### Creating CGI based services 
 To provide your own service you can create a python CGI-Script and use jsonrpc's handleCGI method for handling requests. 
```
#!/usr/bin/env python

from jsonrpc import handleCGI, ServiceMethod

@ServiceMethod
def echo(msg):
    return msg


if __name__ == "__main__":
    handleCGI()

```
 This is the simplest way to create a service using as CGI script. All methods in the script decorated using the ServiceMethod decorator are available to remote callers. all other methods are inaccessible to the "outside world".

handleCGI() gives you some flexibility to define what to use as the service. By default, as seen above it uses the __main__ module as a service. You can though, specify a particular service to be used by passing it to handleCGI(service) as first parameter: 
```
#!/usr/bin/env python

from jsonrpc import handleCGI, ServiceMethod

class MyService(object):
    @ServiceMethod
    def echo(self, msg):
        return msg


if __name__ == "__main__":
    service = MyService()
    handleCGI(service)
    
 ```
 
 ### Error handling
 ```
 try:
  print s.echo("foobar")
except JSONRPCException, e:
  print repr(e.error)
  ```
  Any exception raised in a Service's method during invokation will be converted into an error object and transmitted back to the caller by jsonrpc. The error object will use the exception's class name as a name property and it's message property as the message property of the error object being returned. 
