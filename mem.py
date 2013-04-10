#python 3

import json
import csv
import urllib.request
import urllib.error
import datetime
import time

jenkinsUrl = "http://xxxxxxxxx/computer"

def get_nodes(url, printer):
    try:
        nodes = urllib.request.urlopen(jenkinsUrl + "/api/json" )
    except Exception as e:
        print(e)
    else:
        if nodes.status == 200:
            printer(json.loads(nodes.read().decode('utf-8')))
        nodes.close()
    
def console_printer(dict_info):
    for node_info in dict_info['computer']:
        print(node_info['displayName'])
        mem_info = node_info['monitorData']\
                   ['hudson.node_monitors.SwapSpaceMonitor']
        print('availablePhysicalMemory: '  \
              + str(mem_info['availablePhysicalMemory']))
        print('totalPhysicalMemory    : ' \
              + str(mem_info['totalPhysicalMemory']))
        print('availableSwapSpace     : ' \
              + str(mem_info['availableSwapSpace']))
        print('totalSwapSpace         : ' \
              + str(mem_info['totalSwapSpace']))
def csv_printer(dict_info):
    for node_info in dict_info['computer']:
        mem_info = node_info['monitorData']\
                   ['hudson.node_monitors.SwapSpaceMonitor']
        if node_info['offline'] == False:
            with open('tmp/' + node_info['displayName'] + '.csv',\
                      'a+', newline = '') as csvfile:
                info_writer = csv.writer(csvfile)
                info_writer.writerow([datetime.datetime.now().time(),\
                                      str(mem_info['availablePhysicalMemory']),\
                                      str(mem_info['totalPhysicalMemory']),\
                                      str(mem_info['availableSwapSpace']),\
                                      str(mem_info['totalSwapSpace'])])

def mem_printer(dict_info):
    for node_info in dict_info['computer']:
        mem_info = node_info['monitorData']\
                   ['hudson.node_monitors.SwapSpaceMonitor']
        with open('tmp/mem.csv', 'a+', newline = '') as csvfile:
            info_writer = csv.writer(csvfile)
            info_writer.writerow(\
                [node_info['displayName'],\
                 str(mem_info['totalPhysicalMemory']/1024/1024/1024)])

if __name__ == '__main__':
    counter = 0
    while counter < 90:
        get_nodes(jenkinsUrl, csv_printer)
        print('[' + str(counter) +']' + str(datetime.datetime.now()))
        counter += 1
        time.sleep(2 * 60)
