import os, shutil, xml, errno;
import xml.etree.ElementTree as ET

# Constants
NEWLINE = '\n'
BUILD_DIR = 'Build'
GIT_DIRECTORY = '.git'
PROJECT_NAME = 'GMLScripts'
PROJECT_DIR = PROJECT_NAME + '.gmx'
PROJECT_PATH = os.path.join(BUILD_DIR,PROJECT_DIR,PROJECT_NAME+'.project.gmx')
EXTENSION_NAME = 'GML Scripts'
EXTENSION_PATH = os.path.join(BUILD_DIR,PROJECT_DIR,'extensions',EXTENSION_NAME+'.extension.gmx')

# Ensures that a given directory exists
def ensure_dir(dirname):
	try:
		os.makedirs(dirname)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
# Open the GameMaker project file
project_xml = ET.parse(PROJECT_PATH)
project_root = project_xml.getroot();
ext_xml = ET.parse(EXTENSION_PATH)
ext_root = ext_xml.getroot();

rootDir = '.'
outDir = os.path.join(BUILD_DIR,PROJECT_DIR,'scripts')
# Clean the project scripts directory
shutil.rmtree(outDir, ignore_errors=True)
scripts = project_root.find("scripts")
scripts.clear()
# Clean the extension exported resources
included_res = ext_root.find("IncludedResources")
included_res.clear()

# Walk the current directory and copy the scripts into
# the 'scripts' directory of the generated project
el_tree = [scripts,None,None]
for dirPath, subdirList, fileList in os.walk(rootDir):
	dirName = os.path.basename(dirPath)
	# Skip the generated directories
	if dirName == BUILD_DIR or dirName == GIT_DIRECTORY:
		print('Skipping %s directory' % dirName)
		del subdirList[:]
		continue

	if dirName != '.':
		# Read the GML files from the rest of the Repo
		print('Reading directory: %s' % dirName)
		dir_level = dirPath.count(os.sep)
		print('Dir level: %s' % dir_level)
		el_tree[dir_level] = ET.SubElement(el_tree[dir_level-1],'scripts')
		el_tree[dir_level].attrib["name"] = dirName
		ensure_dir(os.path.join(outDir,dirPath))
		for fname in fileList:
			name_no_ext, ext = os.path.splitext(fname)
			if ext == '.gml':
				print('\t%s' % fname)
				fout = os.path.join(outDir,fname)
				with open(os.path.join(dirPath,fname), 'r') as script:
				    data = script.read().splitlines(True)
				with open(fout, 'w') as dest:
				    dest.writelines(data[1:])
				script_el = ET.SubElement(el_tree[dir_level], 'script')
				script_el.text = 'scripts\\'+fname
				included_script = ET.SubElement(included_res, 'Resource')
				included_script.text = os.path.join('Scripts',dirPath,fname)


project_xml.write(PROJECT_PATH)