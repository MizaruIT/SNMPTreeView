#!/usr/bin/python3

import argparse 
from terminaltables import SingleTable
from textwrap import wrap
import sys 
import ast
sys.path.append('.')
from snmpclientclass import SnmpClient, str2oid, increment1oid, oid2str

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to show a table and ask a choice among the OIDs and their information 
def choose_subtree(snmpclient, list_branches):
    print(f"\n{bcolors.HEADER}LIST OF THE OIDs (aka BRANCHES){bcolors.ENDC}")
    table_data = [['Choice', 'OID', 'File name', 'Name', 'Value', 'Description', 'maxacccess', 'indices', 'Type']]
    i = 0
    for subbranches in list_branches:
        infos = snmpclient.getInfo_fromOID(subbranches['oid'])
        if subbranches['node_type'] == "internal":
            infos['nodes'] = []
        infos['datatype'] = subbranches['datatype']
        if subbranches['node_type'] == "leaf":
            infos['value'] = subbranches['value']
            infos['value'] = '\n'.join(wrap(str(infos['value']), 30))
        infos['description'] = '\n'.join(wrap(str(infos['description']), 40))
        infos_list = [i, infos.get('oid'), infos.get('filename'), infos.get('name'), infos.get('value'), infos.get('description'), infos.get('maxaccess'), infos.get('indices'), infos.get('datatype')]
        table_data.append(infos_list)
        i+=1
    all_table = SingleTable(table_data)
    all_table.inner_row_border = True
    max_width = all_table.column_widths
    print(all_table.table)
    print("Which OID (aka branch) do you want to check the sub-OIDs (aka subtrees)?")
    index = check_Int(len(list_branches)-1)
    return list_branches[index]['oid']

# Function check if the value type is Int and its value is between 0 < x < max value
def check_Int(valMax): 
    while True:
        val = input("Choice = ")
        try:
            val = int(val)
            if 0 <= val <= valMax:
                return val
            else:
                print("Please enter a valid number between 0 and " + str(valMax))
        except ValueError:
            print("Please enter a valid number between 0 and " + str(valMax))

# Function to parse through the SNMP tree
def checkTree(snmp, oid):
    branches = snmp.getBrancheswithVal(oid)
    while branches:
        while True:
            branches = snmp.getBrancheswithVal(oid)
            if len(branches) == 1 and branches[0]['node_type'] == "internal":
                oid = branches[0]['oid']
            else:
                break
        oid = choose_subtree(snmp, branches)
        branches = snmp.getBrancheswithVal(oid)

if __name__ == '__main__':
    #Parser to add the different arguments required or not
    parser = argparse.ArgumentParser(description='SNMP Tool to browse the tree of OIDs in a non-linear way')
    parser.add_argument('-a', '--addr', type=str, help='Address of the target', required=True)
    parser.add_argument('-o', '--oid', type=str, help='OID to parse, per default it is the value 0 to start at the beginning', default = '')
    parser.add_argument('-c', '--community', type=str, help='Authentication with the community as input, per default it is the value : public', default='public')
    parser.add_argument('-v', '--version', type=int, help='Version of the SNMP, per default it is the version 2 : v2c', default=1, choices = [0, 1, 3])
    parser.add_argument('-u', '--userName', type=str, help='The user name for the v3 of SNMP', default='')
    parser.add_argument('--authKey', type=str, help='The key of the authentication protocol', default=None)
    parser.add_argument('--privKey', type=str, help='The key of the privacy protocol', default=None)
    parser.add_argument('--authProtocol', type=str, help='The type of the authentication protocol', choices = ['USM_AUTH_NONE', 'USM_AUTH_SHA', 'USM_AUTH_MD5'], default='USM_AUTH_NONE')
    parser.add_argument('--privProtocol', type=str, help='The type of the privacy protocol', choices = ['USM_PRIV_NONE', 'USM_PRIV_CBC56_DES', 'USM_PRIV_CBC168_3DES', 'USM_PRIV_CFB128_AES', 'USM_PRIV_CFB192_AES', 'USM_PRIV_CFB256_AES'], default='USM_PRIV_NONE')
    args = parser.parse_args()
    print(f"--------------------------------------\n{bcolors.BOLD}Welcome to the SNMPTreeView Tool{bcolors.ENDC}\n--------------------------------------")
    snmp = SnmpClient(args.addr, 161, args.community, args.version, args.userName, args.authKey, args.privKey, args.authProtocol, args.privProtocol)
    try:
        checkTree(snmp, args.oid)
    except Exception as e:
        print(e)
