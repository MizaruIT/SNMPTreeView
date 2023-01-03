from pysnmp.hlapi import * #Pysnmp = implement SNMP into python
from pyasn1.type.univ import * 
from pyasn1.type import univ
from sqlite3 import * 
import json 
import ast
from pyasn1.type.univ import ObjectIdentifier
from pysnmp.entity.rfc3413.oneliner import cmdgen

# The different exceptions which can happen
class SnmpError(Exception):
    pass

class EndOfTreeView(SnmpError):
    pass

class ErrorIndication(SnmpError):
    pass

class ErrorStatus(SnmpError):
    pass

class SnmpClient(object):
    def __init__(self, addr, port, community, version, userName, authKey, privKey, authProtocol, privProtocol):
        super(SnmpClient, self).__init__()
        self.addr = addr
        self.port = port
        self.community = community
        self.version = version
        self.engine = SnmpEngine()
        #If version 3 is implemented:
        self.userName = userName
        self.authKey = authKey
        self.privKey = privKey
        self.authProtocol = authProtocol
        self.privProtocol = privProtocol

    # Function to return all the informations from the subbranches via the database/request snmp
    def getAllInfos_fromSub(self, oid):
        infos = ['oid', 'filename', 'name', 'description', 'maxaccess', 'indices', 'type']
        all_info_sub = []
        while True:
            list_subbranches = self.getBrancheswithVal(oid)
            if len(list_subbranches) == 1 and list_subbranches[0]['node_type'] == "internal":
                oid = list_subbranches[0]['oid']
            else:
                break
        for subbranches in list_subbranches:
            new_info = self.getInfo_fromOID(subbranches['oid'])
            if subbranches['node_type'] == "internal":
                new_info['nodes'] = []
            new_info['datatype'] = subbranches['datatype']
            if subbranches['node_type'] == "leaf":  
                new_info['value'] = subbranches['value']
            if new_info['indices'] is not None:
                new_info['indices'] = new_info['indices'].replace('\n', '<br/>')
            if new_info['maxaccess'] == "read-write" or new_info['maxaccess'] == "write-only":
                new_info['backColor'] = "#d7c797" 
            all_info_sub.append(new_info)
        return all_info_sub

    # Function to set up USM user name + carry crypto keys/protocols to SNMP engine
    def usmuserdata(self):
        # Auth protocol
        if self.authProtocol == "USM_AUTH_MD5":
            self.authProtocol = cmdgen.usmHMACMD5AuthProtocol
        if self.authProtocol == "USM_AUTH_SHA":
            self.authProtocol = cmdgen.usmHMACSHAAuthProtocol
        if self.authProtocol == "USM_AUTH_NONE":
            self.authProtocol = cmdgen.usmNoAuthProtocol 
        # Privacy protocol
        if self.privProtocol == "USM_PRIV_NONE":
            self.privProtocol = cmdgen.usmNoAuthProtocol
        if self.privProtocol == "USM_PRIV_CBC56_DES":
            self.privProtocol = cmdgen.usmDESPrivProtocol
        if self.privProtocol == "USM_PRIV_CBC168_3DES":
            self.privProtocol = cmdgen.usm3DESEDEPrivProtocol
        if self.privProtocol == "USM_PRIV_CFB128_AES":
            self.privProtocol = cmdgen.usmAesCfb128Protocol
        if self.privProtocol == "USM_PRIV_CFB192_AES":
            self.privProtocol = cmdgen.usmAesCfb192Protocol
        if self.privProtocol == "USM_PRIV_CFB256_AES":
            self.privProtocol = cmdgen.usmAesCfb256Protocol
        #print(f'userName : {self.userName} / authKey : {self.authKey} / privKey : {self.privKey} / authproto : {self.authProtocol} / privProto : {self.privProtocol}')
        return cmdgen.UsmUserData(
            userName=self.userName,
            authKey=self.authKey, privKey=self.privKey,
            authProtocol=self.authProtocol,
            privProtocol=self.privProtocol
            )

    # Function to return the SNMP request
    def execute_command(self, cmd, oid):
        security_model = CommunityData(self.community, mpModel=self.version) # If version 1 or v2c
        if str(self.userName) != '': # If version 3
            self.version = 3
            self.community = None
            security_model = self.usmuserdata()
        #Udp can be in two forms:
        #timeout = in seconds
        #retries = max number of retries
        #Udp for IPv4 : UdpTransportTarget(('195.218.195.228'), 161, timeout=1, retries=5)
        #Udp for IPv6 : Udp6TransportTarget(('2a00:1450:4007:80e::200e', 161), timeout=., ...)
        g = cmd(self.engine,
                security_model,
                UdpTransportTarget((self.addr, self.port), timeout=1, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lookupMib=False)
        return g

    # Function to make a SNMP get request and return the name (OID) and value of this OID
    def get_Request(self, oid):
        g = self.execute_command(getCmd, oid)
        errorIndication, errorStatus, errorIndex, varBinds = next(g)
        if errorIndication:
            raise ErrorIndication(f'Error indication : {errorIndication}')
        elif errorStatus:
            error = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
            raise ErrorStatus(f'Error status : {error}')
        else:
            for name, val in varBinds:
                return name, val

    # Function to make a SNMP get next request and return the name (OID) and value of this OID
    def getNext_Request(self, oid):
        g = self.execute_command(nextCmd, oid)
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(g)
        except:
            raise EndOfTreeView(f'No next OIDs after {oid}')
        #for errorIndication, errorStatus, errorIndex, varBinds in g:
        #print(errorIndication, errorStatus, errorIndex)
        if errorIndication:
            raise ErrorIndication(f'Error indication : {errorIndication}')
        elif errorStatus:
            error = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
            raise ErrorStatus(f'Error status : {error}')
        else:
            for name, val in varBinds:
                return name, val
        #else:
        #    raise EndOfTreeView(f'No next OIDs after {oid}')

    # Function to make a SNMP get bulk request and return the name (OID) and value of this OID / Not used
    def getBulk_Request(self, oids):
        g = bulkCmd(SnmpDispatcher(),
                CommunityData(self.community, mpModel=self.version),
                UdpTransportTarget((addr, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oids)),
                lookupMib=False) 
        for errorIndication, errorStatus, errorIndex, varBinds in g:
            if errorIndication:
                raise ErrorIndication(f'Error indication : {error}')
            elif errorStatus:
                error = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
                raise ErrorStatus(f'Error status : {error}')
            else:
                for name, val in varBinds:
                    return name
    
    def set_Request(self, oid, new_value, datatype):
        security_model = CommunityData(self.community, mpModel=self.version) # If version 1 or v2c
        if str(self.userName) != '': # If version 3
            self.version = 3
            self.community = None
            security_model = self.usmuserdata()
        # Set the type in function nof the type of the value
        if datatype in ['Integer', 'Boolean', 'BitString', 'OctetString', 'Null',
           'ObjectIdentifier', 'Real', 'Enumerated',
           'SequenceOfAndSetOfBase', 'SequenceOf', 'SetOf',
           'SequenceAndSetBase', 'Sequence', 'Set', 'Choice', 'Any',
           'NoValue', 'noValue']:
            new_value = getattr(univ, datatype)(new_value)
        g = setCmd(self.engine,
                security_model,
                UdpTransportTarget((self.addr, self.port), timeout=1, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity(oid), new_value),
                lookupMib=False)
        errorIndication, errorStatus, errorIndex, varBinds = next(g)
        if errorIndication:
            raise ErrorIndication(f'Error indication : {error}')
        elif errorStatus:
            error = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
            raise ErrorStatus(f'Error status : {error}')
        else:
            for name, val in varBinds:
                return val

    # Function to make a SNMP get next request (and padding the OID if needed)
    def get_next(self, oid):
        # Pad OID to 2 components
        l = list(oid)
        while len(l) < 2:
            l += [0]
        return self.getNext_Request(oid2str(l))
   
    # Function to return the list of sub-OIDs and their information (maybe need to remove str(base_oid) in the return) 
    def getBrancheswithVal(self, base_oid):
        base_oid = ObjectIdentifier(base_oid)
        list_branches = []
        prefix_len = len(base_oid)
        current = base_oid
        while base_oid.isPrefixOf(current):
            try:
                next_, value = self.get_next(current) 
                datatype = str(value.subtype.__self__.__class__.__name__)
            except EndOfTreeView:
                break
            if not base_oid.isPrefixOf(next_) or datatype=='Null': #Not the best way (datatype=='Null') but problem with the v1, i don't know why
                break
            next_len = len(ObjectIdentifier(next_))
            if next_len == prefix_len+1: # If next OID is a leaf, we retrieve its value, datatype
                dict_infos = {'oid':str(next_[:prefix_len+1]), 'value': str(value.prettyPrint()), 'datatype': datatype, 'node_type':'leaf'} 
            elif next_len > prefix_len: #If next OID is internal
                dict_infos = {'oid':str(next_[:prefix_len+1]), 'node_type':"internal", 'datatype': datatype}
            list_branches.append(dict_infos)
            current = increment1oid(next_, prefix_len)
        return list_branches 

    # Function to return the information from the OID selected (by retrieving the information from the database)
    def getInfo_fromOID(self, oid):
        conn = connect('snmp_mibs.db')
        conn.row_factory = Row
        cur = conn.cursor()
        cur.execute("SELECT oid, filename, name, description, maxaccess, indices from mibs WHERE oid=?", (oid,))
        row = cur.fetchone()
        (oid, filename, name, description, maxaccess, indices) = row if row else (oid, None, None, None, None, None) 
        if not row and oid:
            previousOID = oid2str(oid.split('.')[:-1])
            while not row and previousOID:
                previousOID = oid2str(previousOID.split('.')[:-1])
                cur.execute("SELECT oid, filename, name, description, maxaccess, indices from mibs WHERE oid=?", (previousOID,))
                row = cur.fetchone()
            if row:
                if str(row['oid']).startswith(previousOID):
                    name = oid.replace(str(row['oid']), str(row['name']))
                filename = str(row['filename'])
        row = {'oid':oid, 'filename':filename, 'name':name, 'description':description, 'maxaccess':maxaccess, 'indices':indices} 
        return row

# To increment the OID (ex: 1.3.6.1 -> 1.3.6.2)
def increment1oid(oid, length):
    return ObjectIdentifier(list(oid[:length]) + [oid[length] + 1])

# To modify the type of the OID (ex: 1.3.6.1 -> [1, 3, 6, 1])
def str2oid(oid):
    if not oid:
        return []
    return [int(x) for x in oid.split('.')]

# To modify the type of the OID (ex: [1, 3, 6, 1] -> 1.3.6.1)
def oid2str(base_Oid):
    return '.'.join(map(str, base_Oid))
