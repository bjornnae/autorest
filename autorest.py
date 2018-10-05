import time
import os
import requests
import shutil

global _verbose 
_verbose = True

class Autopublish:
    
    def __init__(self, cfg):
        self.logRecords = ""
        self.state = "init"
        self.executedLaps = 0
        self.maxLaps = 10
        self.config = cfg
        self.knownFiles = []
        
    def log(self, level, message):
        global _verbose
        logStr = "\n<%s><%s><%s> %s" % (time.time(), self.config["name"], level, message) 
        if _verbose: print(logStr)
        self.logRecords += logStr 
    
    def detectNewFiles(self, dirPath):
        newFiles = []
        availableFiles = os.listdir(self.config["inPath"])
        for fn in availableFiles:
            if fn not in self.knownFiles:
                newFiles.append(fn)
                self.log("INFO", "Detected new file: %s" % (fn))
                self.knownFiles.append(fn)
        return(newFiles)

    def step(self):    
        if self.state != "stopped":
            self.log("INFO", "Stepping")
            newfiles = self.detectNewFiles(self.config["inPath"])
            if len(newfiles) > 0:
                for fn in newfiles:
                    ddata = ""
                    with open(self.config["inPath"] + "/" + fn, "r") as fh:
                        ddata += fh.read()        
                    
                    r = requests.post(self.config["url"], data = ddata, headers = self.config["headers"])

                    self.log("INFO", "Received status code %s from server." % r.status_code)
                    if r.status_code == 200:
                        shutil.move(self.config["inPath"] + "/" + fn, self.config["okPath"] + "/" + fn + "_" + str(time.time()) )                
                        self.log("INFO", "Success posting %s" % fn)
                    else:
                        shutil.move(self.config["inPath"] + "/" + fn, self.config["failPath"] + "/" + fn + "_" + str(time.time()))                
                        self.log("ERROR", "Failure posting %s" % fn)
            self.pollWait()

    def pollWait(self):
        self.state = "sleep"
        time.sleep(self.config["pollWait"])
        self.run()

    def stop(self):
        self.state = "stopped"

    def run(self):
        if self.executedLaps < self.maxLaps:  
            self.state ="running"
            self.executedLaps += 1
            self.step()
    

if __name__ == "__main__":
    cfg = { "name" : "Basic Post test",
            "url" : "http://localhost:5000/Put", 
            "method" : "POST", 
            "headers" : {"content" : "application/text"},
            "inPath" : "./IN",
            "okPath" : "./OK",
            "failPath" : "./FAIL",
            "pollWait": 1 
            }
    a1 = Autopublish(cfg)
    a1.run()



