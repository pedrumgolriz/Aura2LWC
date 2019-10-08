#!/usr/bin/env python3

# Written by Pedrum Golriz
# Convert Aura Component to LWC with this lightweight tool

import os
import argparse
from pyquery import PyQuery
import re
import ast
from elevate import elevate
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
args = parser.parse_args()
path = args
files = []

lwcPath = ""

print "######"
print path.input
print path.output
print "######"

for r, d, f in os.walk(path.input):
	for file in f:
		if '.cmp' in file or '.js' in file or '.css' in file:
			print("Adding file "+file)
			files.append(os.path.join(r, file))
			#create folder LWC if not already exists
		
lwcpath = path.output +"/lwc/"
os.umask(0002)
print "Checking if lwc folder exists: " + str(os.path.exists(lwcpath)) 
#elevate()
if not os.path.exists(lwcpath):
	os.mkdir(lwcpath)

#implements attribute on aura:component
targets = []
targetsRgx = "implements"
#apex
apex = ""
apexRgx = "controller"
#global attribute on aura:component
access = ""
accessRgx = "access"
#aura:attributes
attributes = []
attributesRgx = ""
#aura:handlers
handlers = []
handlersRgx = ""
#html dom tree
html = ""
htmlRgx = ""
#start with c:
partials = []
partialsRgx = ""
#has default @api recordid
recordId = False
#start conversion file by file
files.sort()
for file in files:
	print "Converting " + file + " from Aura to LWC"
	#conversion of cmp
	if file.endswith('.cmp'):
		with open(file, "r") as comp:
			pq = PyQuery(str(comp.read()))
			#store the following in targets
			if pq('component').attr(targetsRgx):
				targets = pq('component').attr(targetsRgx).split(',')
			fixedTargets = []
			for target in targets:
				if(target.strip() == 'force:appHostable'):
					fixedTargets.append("lightning__AppPage")
				elif(target.strip() == 'flexipage:availableForRecordHome'):
					fixedTargets.append("lightning__HomePage")
				elif(target.strip() == 'force:hasRecordId'):
					recordId = True
				elif(target.strip() == 'flexipage:availableForAllPageTypes'):
					fixedTargets.append("lightning__RecordPage")
				elif(target.strip() == "forceCommunity:availableForAllPageTypes"):
					fixedTargets.append('lightningCommunity__Page')
			targets = fixedTargets
				
			print 'Targets: '+str(targets)
			#store apex controller
			if pq('component').attr(apexRgx):
				apex = pq('component').attr(apexRgx)
			#store the folloiwing in access
			if pq('component').attr(accessRgx):
				access = pq('component').attr(accessRgx).lower()
			print 'Access type: '+access 
			#store the following in attributes
			if pq('attribute'):
				attributesArray = pq('attribute')
				for attribute in attributesArray.items():
					attributeName = ""
					attributeType = ""
					attributeAccess = ""
					attributeDefault = ""
					attributeRequired = ""
					attributeDescription = ""
					if attribute.attr('name'):
						attributeName = attribute.attr('name')
					if attribute.attr('type'):
						attributeType = attribute.attr('type')
					if attribute.attr('access'):
						attributeAccess = attribute.attr('access')
					if attribute.attr('default'):
						attributeDefault = attribute.attr('default')
					if attribute.attr('required'):
						attributeRequired = attribute.attr('required')
					if attribute.attr('description'):
						attributeDescription = attribute.attr('description')
					print "Attribute Name: " + str(attributeName)
					print "Attribute Type: " + str(attributeType)
					print "Attribute Access: " + str(attributeAccess)
					print "Attribute Default: " + str(attributeDefault)
					print "Attribute Required: " + str(attributeRequired)
					print "Attribute description: " + str(attributeDescription)
					print "\n"
					attributes.append({'name': attributeName, 'type': attributeType, 'access': attributeAccess, 'default': attributeDefault, 'required': attributeRequired, 'description': attributeDescription})

			if pq('handler'):
				handlerArray = pq('handler')
				for handler in handlerArray.items():
					handlerName = ""
					handlerValue = ""
					handlerAction = ""
					if handler.attr('name'):
						handlerName = handler.attr('name')
					if handler.attr('value'):
						handlerValue = handler.attr('value')
					if handler.attr('action'):
						handlerAction = handler.attr('action')
					print "Handler Name: " + str(handlerName)
					print "Handler Value: " + str(handlerValue)
					print "Handler Action: " + str(handlerAction)
					print "\n"
					handlers.append({'name': handlerName, 'value': handlerValue, 'action': handlerAction})

			#known html elements
			html = ["a","abbr","address","area","article","aside","audio","b","bdi","bdo","blockquote","body","br","button","canvas","caption","cite","code","col","colgroup","command","datalist","dd","del","details","dfn","div","dl","dt","em","embed","fieldset","figcaption","figure","footer","form","h1","h2","h3","h4","h5","h6","header","hr","html","i","iframe","img","input","ins","kbd","keygen","label","legend","li","main","map","mark","menu","meter","nav","object","ol","optgroup","option","output","p","param","pre","progress","q","rp","rt","ruby","s","samp","section","select","small","source","span","strong","sub","summary","sup","table","tbody","td","textarea","tfoot","th","thead","time","tr","track","u","ul","var","video","wbr"]
			#known lightning elements (should work as is)
			knownLightningElements = ["buttonGroup", "buttonIcon", "buttonIconStateful", "buttonMenu", "menuItem", "menuDivider", "menuSubheader", "buttonStateful", "insertImageButton", "inputAddress", "checkboxGroup", "compbox", "dualListbox", "fileUpload", "fileCard", "input", "inputField", "inputName", "inputLocation", "radioGroup", "slider", "inputRichText", "formattedAddress", "clickToDial", "formattedDateTime", "formattedEmail", "formattedLocation", "formattedName", "formattedNumber", "outputField", "formattedPhone", "formattedRichText", "formattedText", "formattedTime", "formattedUrl", "relativeDateTime", "recordEditForm", "recordForm", "recordViewForm", "accordion", "accordionSection", "card", "carousel", "layout", "layoutItem", "tab", "tabset", "tile", "breadcrumb", "breadcrumbs", "navigation", "tree", "verticalNavigation", "verticalNavigationItem", "verticalNavigationItemBadge", "verticalNavigationItemIcon", "verticalNavigationOverflow", "verticalNavigationSection", "avatar", "badge", "datatable", "dynamicIcon", "helptext", "icon", "listView", "overlayLibrary", "notificationsLibrary", "path", "picklistPath", "pill", "pillContainer", "progressBar", "progressIndicator", "treeGrid", "spinner"]
			#aura elements
			knownAuraElements = ["if", "set", "iteration", "renderIf", "template", "text", "unescapedHtml", "component", "attribute", "handler"]

			# start the conversion process
			view = str(pq)
			view = re.sub(r'<component(.|\n)*?>','',view)
			view = re.sub(r'<attribute(.|\n)*?>','',view)
			view = re.sub(r'<handler(.|\n)*?>','',view)
			view = re.sub(r'\s+', ' ', view)
			view = re.sub(r':', '-', view)
			controllerAttrs = list(re.finditer(r'\"{!(.*?)*..|}\"', view))
			for sub in controllerAttrs:
				if sub.group(0).find('{') > -1:
					view = re.sub(sub.group(0), '{', view, 1)
				else:
					view = re.sub(sub.group(0), '}', view, 1)
			
			for el in pq('*'):
				if not el.tag in html and not el.tag in knownLightningElements and not el.tag in knownAuraElements:
					view = re.sub(el.tag, 'c-'+el.tag, view)

			view = re.sub(r'</component>', '', view)
			view = "<template>"+view+"</template>"
			print "LWC View Successfully generated!"
				
			#make the new html file
			numDir = file.split('/', 100)
			dirName = (numDir[-1].split('.')[0])[0].lower() + (numDir[-1].split('.')[0])[1:]
			if not os.path.exists(lwcpath+dirName):
				os.mkdir(lwcpath+dirName)
			with open(lwcpath+dirName+'/'+dirName+'.html', 'w') as filed:
				filed.write(BeautifulSoup(view, "html.parser").prettify())
	#conversion of css
	if file.endswith('.css'):
		with open(file, "r") as comp:
			comp = re.sub(r'.THIS', '', str(comp.read()))
		numDir = file.split('/', 100)
		dirName = (numDir[-1].split('.')[0])[0].lower() + (numDir[-1].split('.')[0])[1:]
		if not os.path.exists(lwcpath+dirName):
				os.mkdir(lwcpath+dirName)
		with open(lwcpath+dirName+'/'+dirName+'.css', 'w') as fileCss:
				fileCss.write(comp)
		print "LWC CSS Generated Successfully!"
	if ("controller.js" in file.lower()):
		controllerjs = ""
		#import any apex page needed
		controllerjs += "import { LightningElement, api, track, wire } from 'lwc'\n"
		controllerjs += "export default class "+dirName[0].upper()+dirName[1:]+" extends LightningElement {\n"

		# TODO: before we can add apex, we need to find any cmp.get('c.') and add the method to the import
		with open(file, "r") as comp:
			comp = str(comp.read())
			comp = comp.replace(comp[0:2], '[')
			comp = comp.replace(comp[-2:], ']')
			comp = re.sub(r":..*(function)(?=\()(.*)(?=\))(\))", ':', comp)
			comp = re.sub("\n", '', comp)
			comp = re.sub(' +', ' ',comp)
			#comp = ast.literal_eval(comp)
			#print comp
			#print comp.strip('][').split(', ') 

		for attr in attributes:
			if(attr['description'] != ""):
				controllerjs += "\t// "+attr['description'] + '\n'
			controllerjs += "\t@track "+attr['name']
			if(attr['default'] != ""):
				controllerjs += " = "+attr['default'] + ";\n"
			else:
				controllerjs += ";\n"
		if recordId:
			controllerjs += "\t@api recordId;\n"
		for hndlr in handlers:
			if hndlr['name'].strip() == 'init':
				controllerjs += "\tconnectedCallback(){}\n"
			if hndlr['name'].strip() == 'render':
				controllerjs += "\trenderedCallback(){}\n"

		print "####APEX####"
		print apex

		controllerjs += "}"

		numDir = file.split('/', 100)
		dirName = (numDir[-1].split('.')[0])[0].lower() + (numDir[-1].split('.')[0])[1:].split('Controller')[0]
		if not os.path.exists(lwcpath+dirName):
				os.mkdir(lwcpath+dirName)
		#if controller exists, we must append functions
		with open(lwcpath+dirName+'/'+dirName+'.js', 'w') as fileCss:
				fileCss.write(controllerjs)
		print "LWC Controller Generated Successfully!"

	#if ("helper.js" in file.lower()):
	#create the meta
	if not os.path.exists(lwcpath+dirName):
		os.mkdir(lwcpath+dirName)
	meta = ""
	#add meta lines
	meta += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
	meta += "<LightningComponentBundle xmlns=\"http://soap.sforce.com/2006/04/metadata\" fqn=\""+dirName+"\">\n"
	meta += "\t<apiVersion>46.0</apiVersion>\n"
	if access != "":
		meta += "\t<isExposed>true</isExposed>\n"
	else:
		meta += "\t\t<isExposed>true</isExposed>\n"
	meta += "\t<targets>\n"
	for target in targets:
		meta += "\t\t<target>"+target+"</target>\n"
	meta += "\t</targets>\n"
	meta += "</LightningComponentBundle>"
	with open(lwcpath+dirName+'/'+dirName+'.js-meta', 'w') as fileCss:
				fileCss.write(meta)
	
	#### Create the jsconfig.json
	if not os.path.exists(lwcpath+"jsconfig.json"):
		jsconfig = ""
		jsconfig += "{\n\t\"compilerOptions\": {\n\t\t\"baseUrl\": \".\",\n\t\t\"paths\": {\n"
		jsconfig += "\t\t\t\"c/"+dirName+"\":[\""+dirName+"/"+dirName+".js\"],\n"
		jsconfig += "\t\t},\n\t\t\"experimentalDecorators\": true\n\t},\n"
		jsconfig += "\t\"include\": [\n\t\t\"**/*\",\n\t\t\"../../../../.sfdx/typings/lwc/**/*.d.ts\"\n\t]\n}"
		with open(lwcpath+"jsconfig.json", 'w') as fileJSConfig:
			fileJSConfig.write(jsconfig)
