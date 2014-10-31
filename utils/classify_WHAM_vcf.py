#!/usr/bin/python
import argparse, csv, os, sys, re #std python imports
import numpy as np
from sklearn.ensemble import RandomForestClassifier

#########################
#Args
#########################

parser=argparse.ArgumentParser(description="Runs RandomForest classifier on WHAM output VCF files to classify structural variant type. Appends WC and WP flags for user to explore structural variant calls. The output is a VCF file written to standard out.")
parser.add_argument("VCF", type=str, help="User supplied VCF with WHAM variants; VCF needs AT field data")
parser.add_argument("training_matrix", type=str, help="training dataset for classifier derived from simulated read dataset")
arg=parser.parse_args()


#########################
#Functions
#########################

#parse the targets for ML. converts text list of classified data
#into a numerical dataset with links to the classified names
def parse_targets( target ):
	"""
	target = list of factors to be turned into numerical classifiers. 
	"""
	target = np.array(target) #convert to np array for ease in processing
	names = np.unique( target ) #unique names. 

	#now iterate through and classify to an integer.
	cnt = 0
	target_numerical = np.zeros( target.shape[0] ) #generate empty dataset
	for name in names:
		idx = np.where( name == target )
		target_numerical[ idx ] = cnt
		cnt += 1

	#setup return data structure
	RV = {'names': names, 'target': target_numerical}
	return( RV )


#method to run observed data through the trained model to output
#a vcf friendly return of classified variant call and the prediction
#probabilities for each call
def classify_data( _x, clf, names ):
	"""
	_x = pass the col 8 from vcf
	clf = machine learning object
	names = string names, zero indexed of variant calls. 
	"""
	_x = np.array(_x)
	class_idx = int( clf.predict(_x) )#predict classifier. can link back to dataset['target_names']
	prediction = names[ class_idx ] #lookup text based name for classification

	class_probs = clf.predict_proba(_x)[0] #gives weights for your predictions 1:target_names
	#convert back to text comma separated list
	class_str = ",".join( [ str(i) for i in class_probs ] )

	#parse the two data fields into a string so they can be appended to the vcf file. 
	return_str = "WC=" + prediction + ";WP=" + class_str 
	return( return_str )


#A general parser that takes the data in VCF flag field and parses it into a 
#dictionary data structure. Can then obtain whatever data needed by using
# RV['key']; ie. RV['GT'] ...
def parse_vcf_data( vdat ):
	"""
	vdat = string; column 8 from VCF file with INFO fields. 
	"""
	#start by parsing the vcf data into a dictionary structure
	#will be keyed by ["XX="] =  data 
	dict = {}
	vdat = vdat.split(";")
	for v in vdat:
		try:
			v = v.split("=")
		except:
			print "not valid VCF file"
		dict[ v[0] ] = v[1] #setup dict struct

	#return the dictionary structure data
	return( dict )





#########################
#MAIN
#########################



###########
#import and assign training data
###########
#all sklearn data will be in 2D array [ nsamples X nfeatures]

#iterate over training file. select outthe numerical and classifier data
data  = []
target = []
with open(arg.training_matrix) as t:
#with open("/Users/ej/Desktop/WHAM_classifier/ml_edit.txt") as t:
        for line in csv.reader(t,delimiter='\t'):
        	target.append( line[-1] )
        	d = [ float(i) for i in line[0:-1] ]
        	data.append( d )


#populate the training dataset in sciKitLearn friendly structure. 
dataset = {} #empty data
dataset[ 'data' ] = np.array( data )

#turn our target list into integers and return target names
target_parse = parse_targets( target )
dataset[ 'target' ] = np.array( target_parse['target'] )
dataset[ 'target_names' ] = np.array( target_parse['names'] )





###########
#random forest classification
###########

#setup inital params
clf = RandomForestClassifier(n_estimators=250)
#run RFC on dataset with target classifiers; runs the model fit
clf = clf.fit( dataset['data'], dataset['target'] )



######
#prediction and output
######

#loop over VCF and stream the modified results to STDOUT with print

with open(arg.VCF) as t:
	info_boolean = False #need a boolean to trigger to append new INFO
	#data for new information appended. 
	for line in csv.reader(t,delimiter='\t'):
		if line[0][0] == '#': #skip over VCF header lines.
			if re.search("##FORMAT", line[0]) and info_boolean == False: #first instance of ##FORMAT..
				print '##INFO=<ID=WC,Number=1,Type=String,Description="WHAM classifier vairant type">'
				print '##INFO=<ID=WP,Number=4,Type=Float,Description="WHAM probability estimate for each structural variant classification from RandomForest model">'
				info_boolean = True #reset boolean to 
			print "\t".join( line ) #print results to stdout 
		else: #skip over VCF header lines. 
                      	#print line ##remove
			vdat = parse_vcf_data( line[7] ) #parse all of vcf appended data
			_x = vdat[ 'AT' ].split(",") #create list from data in 'AT' field 
			results = classify_data( _x, clf, dataset['target_names'] )
				
			line[7] = line[7] + ";" + results #append data to correct vcf column
			print "\t".join( line ) #print results to stdout










