import requests, json, pprint, time, socket

# Disable warnings from untrusted server certificates
try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except Exception:
    print("Ignore messages related to insecure SSL certificates")


class Restful:

    def __init__(self,global_URL,global_user,global_password):

        global URL
        global user
        global password
        global headers

        URL = global_URL
        user = global_user
        password = global_password

        # set the headers for how we want the response
        headers = {'content-type': 'application/json','accept':'application/json'}



    ################
    ## make the json GET call to the public api
    ################
    def jsonGet(self, targetUrl):

        #make the actual request, specifying the URL, the JSON from above, standard basic auth, the headers and not to verify the SSL cert.
        #r = requests.post(target_uri, requestJSON, auth=('smc', 'smc'), headers=headers, verify=False)
        try:
            r = requests.get(targetUrl, auth=(user, password), headers=headers, verify=False)
        except:
            print("Exception:  Can't connect to API server URL:  " + targetUrl)
            print("Exiting")
            exit(1)

        #take the raw response text and deserialize it into a python object.
        try:
            responseObj = json.loads(r.text)
        except:
            print("Exception")
            print(r.text)

            print(responseObj.get("message", "API failed to return expected result"))
            self.jsonPrint(responseObj)
            return dict()

        return responseObj

    ################
    ## make the json POST call to the public api
    ################
    def jsonPost(self, targetUrl, requestObj):

        #turn this into a JSON string
        requestJSON = json.dumps(requestObj, sort_keys=True, indent=4)
        #print(requestJSON)

        #make the actual request, specifying the URL, the JSON from above, standard basic auth, the headers and not to verify the SSL cert.
        try:
            r = requests.post(targetUrl, requestJSON, auth=(user, password), headers=headers, verify=False)
        except:
            print("Exception:  Can't connect to API server URL:  " + targetUrl)
            print("Exiting")
            exit(1)

        #take the raw response text and deserialize it into a python object.
        try:
            responseObj = json.loads(r.text)
        except:
            print("Exception")
            print(r.text)
        #self.jsonPrint(responseObj)
        return responseObj


    ################
    ## print a json object nicely
    ################
    def jsonPrint(self, jsonObj):
    	print(json.dumps(jsonObj, sort_keys=False, indent=2))


    #################################################################
    ## Functions to implement Unisphere REST API for VMAX3
    #################################################################

    ######################################
    ## SYSTEM Resource group
    ######################################


    ################
    ## get a list of All Alert ids across all symmetrix arrays
    ################
    def getAlerts(self, URL):
        target_uri = "%s/univmax/restapi/system/alert" % (URL)
        responseKey = 'alertId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    ################
    ## queries for a specified Alert
    ################
    def getAlert(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/system/alert/%s" % (URL, resourceId)
        responseKey = 'symmetrix'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    ################
    ## get the version of Unisphere (the API)
    ################
    def getVersion(self, URL):
        target_uri = "%s/univmax/restapi/system/version" % (URL)
        responseKey = 'version'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    ################
    ## get a list of symmetrix serial #'s known by Unisphere
    ################
    def getSymms(self, URL):
        target_uri = "%s/univmax/restapi/system/symmetrix" % (URL)
        responseKey = 'symmetrixId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    ################
    ## This call queries for a specific Authorized Symmetrix Object that is compatible with slo provisioning using its ID
    ################
    def getSymm(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/system/symmetrix/%s" % (URL, resourceId)
        responseKey = 'symmetrix'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()


    def getSloSymms(self, URL):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix" % (URL)
        responseKey = 'symmetrixId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloSymm(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s" % (URL, resourceId)
        responseKey = 'symmetrix'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloDirectors(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/director" % (URL, resourceId)
        responseKey = 'directorId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloDirector(self, URL, symmId, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/director/%s" % (URL, symmId, resourceId)
        responseKey = 'director'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloPorts(self, URL, symmId, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/director/%s/port" % (URL, symmId, resourceId)
        responseKey = 'symmetrixPortKey'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloPort(self, URL, symmId, directorId, portId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/director/%s/port/%s" % (URL, symmId, directorId, portId)
        responseKey = 'symmetrixPort'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloHosts(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/host" % (URL, resourceId)
        responseKey = 'hostId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloHost(self, URL, symmId, hostId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/host/%s" % (URL, symmId, hostId)
        responseKey = 'host'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloHostgrps(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/hostgroup" % (URL, resourceId)
        responseKey = 'hostGroupId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloHostgrp(self, URL, symmId, grpId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/hostgroup/%s" % (URL, symmId, grpId)
        responseKey = 'hostGroup'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloInitiators(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/initiator" % (URL, resourceId)
        responseKey = 'initiatorId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloInitator(self, URL, symmId, initiatorId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/initiator/%s" % (URL, symmId, initatorId)
        responseKey = 'initiator'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloMaskingviews(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/maskingview" % (URL, resourceId)
        responseKey = 'maskingViewId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloMaskingview(self, URL, symmId, mvId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/maskingview/%s" % (URL, symmId, mvId)
        responseKey = 'maskingView'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSloMvConnections(self, URL, symmId, mvId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/maskingview/%s/connections" % (URL, symmId, mvId)
        responseKey = 'maskingViewConnection'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloPorts(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/port" % (URL, resourceId)
        responseKey = 'symmetrixPortKey'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloPortgrps(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/portgroup" % (URL, resourceId)
        responseKey = 'portGroupId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSloPortgrp(self, URL, symmId, pgId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/portgroup/%s" % (URL, symmId, pgId)
        responseKey = 'portGroup'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSlos(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/slo" % (URL, resourceId)
        responseKey = 'sloId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSlo(self, URL, symmId, sloId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/slo/%s" % (URL, symmId, sloId)
        responseKey = 'slo'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    def getSrps(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/srp" % (URL, resourceId)
        responseKey = 'srpId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    def getSrp(self, URL, symmId, srpId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/srp/%s" % (URL, symmId, srpId)
        responseKey = 'srp'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    ################
    ## get a list of Storage Groups on a given SLO Symmetrix
    ################
    def getSgList(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/storagegroup" % (URL, resourceId)
        responseKey = 'storageGroupId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    ################
    ## get the details of a particular SLO managed Storage Group
    ################
    def getSg(self, URL, symmId, sgId):
        target_uri = "%s/univmax/restapi/sloprovisioning/symmetrix/%s/storagegroup/%s" % (URL, symmId, sgId)
        responseKey = 'storageGroup'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()

    ################
    ## get a list of Thin Pools on a given Symmetrix
    ################
    def getThinPoolList(self, URL, resourceId):
        target_uri = "%s/univmax/restapi/provisioning/symmetrix/%s/thinpool" % (URL, resourceId)
        responseKey = 'poolId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey]
        else:
            return dict()

    ################
    ## get the details of a particular Thin Pool
    ################
    def getThinPool(self, URL, symmId, tpId):
        target_uri = "%s/univmax/restapi/provisioning/symmetrix/%s/thinpool/%s" % (URL, symmId, tpId)
        responseKey = 'poolId'
        responseObj = self.jsonGet(target_uri)
        if responseKey in responseObj:
            return responseObj[responseKey][0]
        else:
            return dict()
