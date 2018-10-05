# Autorest

A publishing robot that makes put or post calls to a rest endpoint.

## dependencies
* python 3
* requests
* flask (only needed for test server)

## usage 

1. Make a configuration file (example in autorest.py). 
2. Instantiate Autorest with the configuration. 
3. start the Autorest instance.
4. put files in the directory corresponding to inPath in the configuration.

The files will be discovered and the file content will be used as  body in either post or put calls.

When response has been received from the server, the input file will be moved to either OK or Fail folder specified in the configuration file and suffixed with a timestamp.

Also contains a test rest server that can be used for development purposes in testserver/. 
