# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-09-17"

#
# run SAFIR through Python shell
# 

#####################
## REFERENCE PATHS ##
#####################
# Note: these should be read/readable from a reference document, e.g. *.yaml

## system path SAFIR executable ##
SAFIRpath="C:/SAFIR/SAFIR.exe"
## working dir ##
workDir_default="C:\\Users\\rvcoile\\Workers" # should be set in separate file and read at start of calculation?

####################
## MODULE IMPORTS ##
####################

# standard module reads
import os
import subprocess
import shutil
from time import time,sleep

##############
## FUNCTION ##
##############

def SAFIR_run(file,path=SAFIRpath,SW_removeItem=False,workDir=None):
	# run SAFIR *.in file
	#	November 2018: SAFIR calculation performed in TMPdir to avoid path length issues

	# canonical path
	file=os.path.realpath(file)

	## check type of SAFIR calcuation
	SAFIRtype=SAFIR_type(file)

	## Directories ##
	Dir=os.path.dirname(file) # original directory
	TMPdir=createTMPdir(workDir) # temporary calculation directory
	tmpfile=copyFileToDir(file,TMPdir) # copy to TMPdir to avoid path length issues
	os.chdir(TMPdir)

	## Run calculation ##
	if SAFIRtype=='Thermal2D':
		## if Thermal2D ==> run calculation
		print("\n###########################################\n## Activate SAFIR Thermal 2D calculation ##\n###########################################\n")
		SAFIR_exe(path,tmpfile) # run SAFIR in TMPdir
		cleanPostCalc(tmpfile,TMPdir,Dir,SAFIRtype)
	else:
		## else (Structural calculation) ==> determine and copy *.tem file to Python dir
		## move *.tem file to SAFIRpy working directory
		temfilepath,temname=SAFIR_TEMinIN(file) # determine *.tem file (full path - *.in directory assumed)
		temtargetpath=TMPdir+'\\'+temname
		if temtargetpath!=temfilepath: shutil.copy(temfilepath,temtargetpath) # copy *.tem file to SAFIRpy working directory
		## run SAFIR
		SAFIR_exe(path,tmpfile)
		cleanPostCalc(tmpfile,TMPdir,Dir,SAFIRtype)

	

def cleanPostCalc(tmpfile,TMPdir,Dir,SAFIRtype):
	# copy output files to original folder and remove TMPdir

	# copy files
	outfile=tmpfile[0:-3]+'.out'; copyFileToDir(outfile,Dir) # *.out file
	xmlfile=tmpfile[0:-3]+'.XML'; copyFileToDir(xmlfile,Dir) # *.XML file
	if SAFIRtype=='Thermal2D': temfile=tmpfile[0:-3]+'.tem'; copyFileToDir(temfile,Dir) # *.TEM file

	# return to original directory
	os.chdir(Dir)
	
	# remove folder
	shutil.rmtree(TMPdir)
	# # remove folder - with retry
	# try: 
	# 	shutil.rmtree(TMPdir)
	# except:
	# 	sleep(5)
	# 	print("Second trial to remove TMPdir")
	# 	try: os.rmdir(TMPdir)
	# 	except: pass

def createTMPdir(workDir):
	if workDir is None: workDir=workDir_default
	if not os.path.isdir(workDir): 
		try: os.mkdir(workDir) # check of workDir_default exists
		except: print("workDir could not be generated")

	# create TMPdir based on current time
	TMPdir=workDir+'\\'+"{0}".format(time())[-5:] # TMPdir=workDir+'\\'+"TEST" # code for testing
	
	# create TMPdir
	while os.path.isdir(TMPdir):
		print("Existing")
		TMPdir+='x' # is supposed to allow for multiprocessing - avoiding clash of TMP folders - to be confirmed
	os.mkdir(TMPdir) # create directory

	return TMPdir

def copyFileToDir(infile,Dir):
	# copy file to tmp directory

	targetfile=Dir+'\\'+infile.split('\\')[-1]
	shutil.copy(infile,targetfile)

	return targetfile

def SAFIR_exe(path,file):

	## remove *.in extension
	file=file[0:-3] 

	## run through subprocess
	subprocess.call([path,file])

def SAFIR_type(file):
	# returns type of *.in file: Thermal2D, Structural2D, Structural3D
	# assumes standard *.in format (GiD) with analysis type on 2nd line

	with open(file) as f:
		line=f.readline() # first line
		line=f.readline().rstrip() # second line and remove newline indication

	if line == 'Safir_Thermal_Analysis': return 'Thermal2D'
	if line == 'Safir_Static_2D_Analysis': return 'Structural2D'
	if line == 'Safir_Static_3D_Analysis': return 'Structural3D'

def SAFIR_TEMinIN(file):
	# returns name *.TEM file referenced in *.IN file

	with open(file) as f:
		line=f.readline()
		while len(line)>0:
			line=f.readline() # read line
			if '.tem' in line:
				line=line.rstrip() # remove newline character
				infolderpath='\\'.join(file.split('\\')[0:-1]) # path to folder of *.in file
				temfilepath=infolderpath+'\\'+line
				return temfilepath,line # returns full path and name only of *.tem file


#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == "__main__": 

	########################
	## SWITCH FOR TESTING ##
	########################

	SW_testcase=6
	SW_debug=False



	## SWITCH ##
	if not SW_debug:

	###############
	## EXECUTION ##
	###############

		## *.in file without extension ##
		# NOTES
		# *.in file path should not include a "."
		if SW_testcase==1:
			# temperature calculation - steel profile
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\3DsteelbeamPy\\w21x44"
			# success confirmed
			infile+=".in" # add *.in extension
		if SW_testcase==2:
			# 3D structural calculation - frame (concrete columns, steel beam) example case JHU training
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\3Dframe_mod\\3dframe"
			# seemingly limitation on *.in file path length
			# *.tem files should be copied to directory SAFIRpy
			# TO DO
			# - check if run refers to structural calc or thermal calc
			# - copy *.tem files in case of structural calc to SAFIRpy directory
			infile+=".in" # add *.in extension
		if SW_testcase==3:
			# 2D structural calculation - concrete column - testcase ISO WI Probab
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\2Dcc\\6MN_0mm0"
			infile+=".in" # add *.in extension
		# trial from alternative path
		if SW_testcase==4:
			# 2D structural calculation - concrete column - testcase ISO WI Probab
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\modfileTest\\6MN_0mm0.in"
		if SW_testcase==5:
			# tmp test long path
			infile="C:\\Users\\rvcoile\\Google Drive\\UGent\\Teaching\\2018-2019\\FEM\\projectSAFIR\\students\\G11-12\\G11\\1029_issue\\rerun\\slab170x1000.in"
		if SW_testcase==6:
			# tmp test 
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\trials\\infileGen\\Test01.in"
			print(infile)

		## execution ##
		SAFIR_run(infile)

	###########
	## DEBUG ##
	###########

	# temporary codes for debugging - activate as needed

	else:

		# tmp test long path
		infile="C:\\Users\\rvcoile\\Documents\\Workers\\Test02\\00000_0001.in"

		## execution ##
		SAFIR_run(infile,workDir="C:\\Users\\rvcoile\\Documents\\Workers")