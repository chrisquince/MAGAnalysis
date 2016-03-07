#!/usr/bin/python
# ***************************************************************
# Name:      KO2MODULEclusters2.py
# Purpose:   This script takes a KO x Clusters (contigs for a genome) abundance file and uses
# 	     http://www.genome.jp/kegg-bin/find_module_object
# 	     to generate a MODULE x Clusters file that contains the
#   	     proportions of completed modules. You can use this script with the clusters
# 	     obtained from CONCOCT software: https://github.com/BinPro/CONCOCT
# 	     Note that you need to have an active internet connection for the script
# 	     to work	 	
# Version:   0.2
# History:   0.1 - 0.2 Optimised module definition resolution
# Authors:   Umer Zeeshan Ijaz (Umer.Ijaz@glasgow.ac.uk)
#                 http://userweb.eng.gla.ac.uk/umer.ijaz
# Created:   2014-03-15
# License:   Copyright (c) 2015 Environments Group, University of Glasgow, UK
#
#            This program is free software: you can redistribute it and/or modify
#            it under the terms of the GNU General Public License as published by
#            the Free Software Foundation, either version 3 of the License, or
#            (at your option) any later version.
#
#            This program is distributed in the hope that it will be useful,
#            but WITHOUT ANY WARRANTY; without even the implied warranty of
#            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#            GNU General Public License for more details.
#
#            You should have received a copy of the GNU General Public License
#            along with this program.  If not, see <http://www.gnu.org/licenses/>.
# **************************************************************/ 

import urllib
import urllib2
import datetime,time
import getopt
import sys
import re
from bs4 import BeautifulSoup

def usage():
   print 'Usage:'
   print '\tpython KO2MODULEclusters.py -i <input_file> -o <output_file> [OPTIONS]'
   print 'Options:'
   print '\t-d Turn debugging on'	
def main(argv):
	input_file=''
	output_file=''
	debug=0

   	try:       
		opts, args =getopt.getopt(argv,"hi:o:d",["input_file=","output_file=","debug"])    
   	except getopt.GetoptError:       
		usage()       
		sys.exit(2)   
	for opt, arg in opts:       
		if opt == '-h':          
			usage()          
			sys.exit()       
   		elif opt in ("-i", "--input_file"):          
			input_file = arg       
        	elif opt in ("-o", "--output_file"):          
                	output_file = arg
		elif opt in ("-d", "--debug"):
			debug=1
   	if input_file=='' or output_file=='':
		usage()
		sys.exit(2)

	print_time_stamp("Loading "+input_file)	
   	ins=open(input_file,"r")
   	record_count=0
	extracted_KOs=[]
	extracted_clusters=[]
	clusters_KOs={}	
   	for line in ins:
		line=line.rstrip('\n').rstrip('\r')
		record=line.split(",")
		if record_count>0:
			extracted_KOs.append(record[0].replace('ko:',''))
			for i in range(len(record[1:])):
				clusters_KOs[extracted_clusters[i]+":"+extracted_KOs[record_count-1]]=float(record[i+1])
		else:
			extracted_clusters=record[1:]
		record_count=record_count+1
   	ins.close()


	clusters_modules={}
	extracted_modules=[]
	for i in extracted_clusters:
		ind=1
		record_string=[]
		for j in extracted_KOs:
			if (clusters_KOs[i+":"+j]>0.0):
				record_string.append(i+"_"+str(ind)+"\t"+j)
				ind=ind+1
		returned_modules={}
		print_time_stamp("Uploading KOs from " + i + " to http://www.genome.jp/kegg-bin/find_module_object" )
		if(debug):
			print_time_stamp("Uploaded \n"+"\n".join(record_string))
		returned_modules=generate_modules_blocks_missing("\n".join(record_string),debug)
		print_time_stamp("Extracted Modules for " + i) 

		for key in returned_modules.keys():
			clusters_modules[i+":"+key]=returned_modules[key]
			extracted_modules.append(key)
	extracted_modules=list(set(extracted_modules))
	extracted_modules_total_blocks={}
	print_time_stamp("Resolving definitions for returned modules")
	for i in extracted_modules:
		tmp=""  
                try:
                	tmp=urllib.urlopen('http://togows.dbcls.jp/entry/orthology/'+i+'/definition').read().rstrip('\n')
                        if(debug):
				print_time_stamp("http://togows.dbcls.jp/entry/orthology/"+i+"/definition" +"\n"+tmp)
                except urllib2.HTTPError, error:
                        print "ERROR: code=%s message=%s" % (error.code, error.msg)
                        sys.exit(1)
                # The regular expression given below calculates total blocks for a given module
                # The M number entry is defined by a logical expression of K numbers (and other M numbers), 
                # allowing automatic evaluation of whether the gene set is complete, i.e., the module is 
                # present, in a given genome. A space or a plus sign represents an AND operation, and a 
                # comma sign represents an OR operation in this expression. A plus sign is used for a 
                # molecular complex and a minus sign designates an optional item in the complex.
                                
                extracted_modules_total_blocks[i]=len(re.sub(r"\([\w\+\-\,\s]+?\)","AND",re.sub(r" \(.*?\)"," AND",re.sub(r"\(.*?\) ","AND ",re.sub(r" \(.*?\) "," AND ",re.sub(r"\([\w\+\-\,\s]+?\)","AND",re.sub(r" \([\w\+\-\,]+?\)"," AND",re.sub(r"\([\w\+\-\,]+?\) ","AND ",re.sub(r" \([\w\-\+\,]+?\) "," AND ",tmp)))))))).split(" "))


	print_time_stamp("Saving "+output_file)
	out=open(output_file,'w')
	out.write("Clusters,"+",".join(extracted_clusters)+"\n")
	for j in extracted_modules:
		out.write(j)
		for i in extracted_clusters:
			if clusters_modules.get(i+":"+j,None)==None:
				out.write(",0.0")
			else:
				out.write(","+str((-clusters_modules.get(i+":"+j,0.0)+float(extracted_modules_total_blocks.get(j,0.0)))/float(extracted_modules_total_blocks.get(j,0.0))))	
		out.write("\n")
	out.close()

def print_time_stamp(message):
    sys.stderr.write(datetime.datetime.fromtimestamp(time.time()).strftime('[%Y-%m-%d %H:%M:%S] ')+message+"\n")

def generate_modules_blocks_missing(record,debug):
	url = 'http://www.genome.jp/kegg-bin/find_module_object'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	post_data={}
	post_data['unclassified']=record
	post_data['mode']="complete+ng1+ng2"
	headers = { 'User-Agent' : user_agent }
	data = urllib.urlencode(post_data)
	req = urllib2.Request(url, data, headers)
	response=""

	try:
		response = urllib2.urlopen(req)
   	except urllib2.HTTPError, error:
		print "ERROR: code=%s message=%s" % (error.code, error.msg)
		sys.exit(1)

	the_page = response.read()
	soup = BeautifulSoup(the_page)
	modules_found=[]
	for i in soup.findAll(href=re.compile("/kegg-bin/show_module")):
		modules_found.append(i.string.encode('ascii','ignore'))

	modules_block_missing=[]
	returned_data={}
	ind=0
	for i in soup.findAll(text=re.compile('\)\xa0\xa0\(')):
		if re.match('.*complete.*',i):
			modules_block_missing.append(0)
		else:
			modules_block_missing.append(int(re.match('.*([1-2]) block.*',i).groups(1)[0].encode('ascii','ignore')))
		if(debug):
			print_time_stamp("Missing "+str(modules_block_missing[-1])+ " blocks for " + modules_found[ind])
		returned_data[modules_found[ind]]=modules_block_missing[-1]
		ind=ind+1

	return returned_data

		
if __name__ == '__main__':
	main(sys.argv[1:])
