import requests
import json
import math
import subprocess
import inspect, os

class ParseDS:

	baseApi = "https://api.figma.com/v1/"
	FIGMA_ACCESS_TOKEN = "26523-6cf5fee4-bb86-4800-b1da-af3c6d2d1509"
	colors = []
	borderWeights = []
	borderRadius = []
	borders = []
	shadows = []
	shadowsAndroid = []
	fontSizes = []
	fontFamilies = []
	opacitys = []
	insets = []
	squishs = []
	lineHeights = []
	spacingStacks = []
	spacingInlines = []
	svgpaths = []
	imagens = []
	componentes = []
	dimensoes = []
	spacings = []
	gradientColors = []
	autocompletes = []
	radioButtons = []
	toogles = []
	sliders = []
	progressbar = []
	search = []
	tooltips = []
	chips = []
	textArea = []
	overflowMenu = []
	navigationBar = []
	datePicker = []
	timePicker = []
	dropDown = []
	cards = []

	#Listas dos componentes:
	buttons = []
	checkBoxes = []

	print("-------------------------------------------")
	print("Escolha um sistema:\n\n")
	print("1. Atech\n")
	print("2. Makron\n")
	print("3. Okto\n")
	print("4. Arkhe\n")
	print("5. design tokens\n\n")
	


	def __init__(abc,figmaID, figmaApiKey):
		abc.figmaId = figmaId
		abc.figmaApiKey = figmaApiKey
		abc.getDS()

	def getDS(abc):

		escolha = input()

		if(escolha == "1"):
			sistema = "atech"
		if(escolha == "2"):
			sistema = "makron" 
		if(escolha == "3"): 
			sistema = "okto"
		if(escolha == "4"): 
			sistema = "arkhe"
		if(escolha == "5"): 
			sistema = "design tokens"

		response = requests.get(abc.baseApi + 'files/' + abc.figmaId, headers={"x-figma-token": abc.figmaApiKey})
		items = json.loads(response.text)
		for obj in items["document"]["children"]:
			if obj["name"].lower() == sistema or obj["name"].lower() == "components":
				for frame in obj["children"]:
					abc.detectFrames(frame)

	def exportToCSS(abc):
		
		f = open("tokens.scss","w+")

		f.write("/*=========== Colors Palletes =============*/\n\n")

		palletes = parse.getPalletes()
		for color in palletes:
			arr = color.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$color-" + className + ":" + arr[1].strip() + ";\n")
		

		f.write("\n\n/*=========== Font Families =============*/\n\n")

		fontFamilies = parse.getFontFamilies()
		for family in fontFamilies:
			arr = family.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		f.write("\n\n/*=========== Font Sizes =============*/\n\n")

		fontSizes = parse.getFontSizes()
		for size in fontSizes:
			arr = size.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + str(int(float(arr[1].strip()))) + "px;\n")


		f.write("\n\n/*=========== Border Width =============*/\n\n")

		borderWeights = parse.getBorderWeights()
		for weight in borderWeights:
			arr = weight.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		f.write("\n\n/*=========== Border Radius =============*/\n\n")

		radius = parse.getBorderRadius()
		for radius in radius:
			arr = radius.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		f.write("\n\n/*=========== Opacities =============*/\n\n")

		opacitys = parse.getOpacitys()
		for opacity in opacitys:
			arr = opacity.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + '%.2f'%(float(arr[1].strip())) + ";\n")




		f.write("\n\n/*=========== Insets =============*/\n\n")

		insets = parse.getInsets()
		for inset in insets:
			arr = inset.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")



		f.write("\n\n/*=========== Squishs =============*/\n\n")

		squishs = parse.getSquishs()
		for squish in squishs:
			arr = squish.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		f.write("\n\n/*=========== Line Height =============*/\n\n")

		lineHeights = parse.getLineHeights()
		for lineHeight in lineHeights:
			arr = lineHeight.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		f.write("\n\n/*=========== Spacing stack =============*/\n\n")

		spacingStacks = parse.getSpacingStacks()
		for spacingStack in spacingStacks:
			arr = spacingStack.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")

		spacingInlines = parse.getSpacingInlines()
		for spacingInline in spacingInlines:
			arr = spacingInline.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		f.close()

		directory = "./"
		subprocess.call("sass " + directory + "components.scss:" + directory + "components.css", shell=True)

		print("Exported CSS to tokens.scss file")
		
	def exportToPlist(abc):
		
		f = open("Tokens.plist","w+")
		
		f.write("""
			<?xml version="1.0" encoding="UTF-8"?>
			<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
			<plist version="1.0">
			<dict>
				<key>Pallete</key>
				<dict>
		""")

		palletes = parse.getPalletes()
		for color in palletes:
			arr = color.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>color-" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")
		

		f.write("""
				</dict>
				<key>FontFamily</key>
				<dict>
		""")

		fontFamilies = parse.getFontFamilies()
		for family in fontFamilies:
			arr = family.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")


		f.write("""
				</dict>
				<key>FontSize</key>
				<dict>
		""")

		fontSizes = parse.getFontSizes()
		for size in fontSizes:
			arr = size.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + str(int(float(arr[1].strip()))) + "</string>\n")

		f.write("""
				</dict>
				<key>BorderWidth</key>
				<dict>
		""")

		borderWeights = parse.getBorderWeights()
		for weight in borderWeights:
			arr = weight.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
				<key>BorderRadius</key>
				<dict>
		""")

		
		radius = parse.getBorderRadius()
		for radius in radius:
			arr = radius.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
				<key>Opacity</key>
				<dict>
		""")
		

		opacitys = parse.getOpacitys()
		for opacity in opacitys:
			arr = opacity.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + '%.2f'%(float(arr[1].strip())) + "</string>\n")


		f.write("""
				</dict>
				<key>SpacingInset</key>
				<dict>
		""")	


		insets = parse.getInsets()
		for inset in insets:
			arr = inset.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
				<key>SpacingSquish</key>
				<dict>
		""")	

		squishs = parse.getSquishs()
		for squish in squishs:
			arr = squish.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
				<key>LineHeight</key>
				<dict>
		""")	

		lineHeights = parse.getLineHeights()
		for lineHeight in lineHeights:
			arr = lineHeight.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
				<key>SpacingStack</key>
				<dict>
		""")	

		spacingStacks = parse.getSpacingStacks()
		for spacingStack in spacingStacks:
			arr = spacingStack.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
				<key>SpacingInline</key>
				<dict>
		""")	

		spacingInlines = parse.getSpacingInlines()
		for spacingInline in spacingInlines:
			arr = spacingInline.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("		<key>" + className + "</key>\n<string>" + arr[1].strip() + "</string>\n")

		f.write("""
				</dict>
			</dict>
		</plist>
		""")

		f.close()

	def exportToXML(abc):

		print ("----------------------------------------------------")
		print("escolha um tipo de recurso para exportar: \n\n")
		print ("1. cores\n")
		print ("2. fontes\n")
		print ("3. dimensões\n")
		print ("4. styles\n")
		print ("5. ícones\n\n")

		
		#colors
		palletes = parse.getPalletes()
		path = "colors"
		file_name = "colors.xml"
		file_scss = "colors.scss"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		f = open(os.path.join(path, file_name),"w+")
		g = open(os.path.join(path, file_scss),"w+")

		f.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
		f.write("<resources> \n\n")
		for color in palletes:
			arr = color.split("=")
			className = arr[0].strip().replace(".","_").replace("-", "_").replace("generic", "").replace("specific", "").replace("colors_", "").lower().replace(" ", "_")
			f.write("<color name = " + "\"" + className +"\"" + ">" + arr[1].strip() + "</color>"";\n")
			g.write("$" + className + ":" + arr[1] + ";" + "\n")

		f.write("\n\n</resources>")
		f.close()
	
		#gradients 
		gradients = parse.getGradientColors()
		for colorGrad in gradients:
			arr = colorGrad.split("=")
			colorName = arr[0].replace("/", "_")
			colorStart = arr[1]
			colorEnd = arr[2]

			fileGrad = colorName + ".xml"
			h = open(os.path.join(path, fileGrad),"w+")

			h.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			h.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			h.write("<gradient\n")
			h.write("android:startColor=" + "\"" +colorStart + "\"" +"\n")
			h.write("android:endColor=" + "\"" +colorEnd + "\"" + ">" +"\n")
			h.write("</gradient>\n")
			h.write("</shape>")
			h.close()

			g.write("$" + colorName+":"+ "(" + colorStart +"," + colorEnd + ")" + ";\n")
		g.close()


		#fonts
		fontFamilies = parse.getFontFamilies()
		path = "fonts"
		arquivo = "fonts.xml"
		file_scss = "fonts.scss"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		g = open(os.path.join(path, arquivo),"w+")
		h = open(os.path.join(path, file_scss),"w+")


		g.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
		g.write("<font-family xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ "\n\n")

		for family in fontFamilies:
			arr = family.split("=")

			#arquivo geral de fontes

			#android
			g.write("<font\n")
			g.write("android:font=" + "\"" + arr[2] + "\"" + "/>" + "\n")

			className = arr[2]
			file_name = className + ".ttf"
			f = open(os.path.join(path, file_name),"w+")
			f.write(arr[0] + arr[1]+ arr[2])
			
			#web
			h.write("@font_face {\n")
			h.write("  font-family: " + className + "\n")
			h.write("  src: url(path_da_font);\n")
			h.write("  font-weight:" + arr[4] +";\n")
			h.write("}\n\n")

			h.write("." + arr[0] + "{" + "\n")
			h.write("  font-family: " + className + "\n")
			h.write("  font-weight:" + arr[4] +";\n")
			h.write("  font-size:" + arr[3].split(".")[0] + "px" +";\n")
			h.write("  line-height:" + arr[5].split(".")[0] + "px" +";\n")
			h.write("}\n\n")

			f.close()
		g.write("</font-family>")
		h.close()
	

		#dimens
		path = "dimens"
		file_name = "dimens.xml"
		file_scss = "spacing.scss"
		file_scss_borders = "borders.scss"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		f = open(os.path.join(path, file_name),"w+")
		g = open(os.path.join(path, file_scss),"w+")
		h = open(os.path.join(path, file_scss_borders),"w+")
		f.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
		f.write("<resources> \n\n")		

		#android dimens
		dimensoes = parse.getDimensoes()
		for dimens in dimensoes:
			dimenValue = "0px"
			arr = dimens.split("=")
			className = arr[0].strip().replace(".","-").replace("-", "_").lower()
			if arr[1] == "0":
				dimenValue == arr[1] + "px"
			else:
				dimenValue = arr[1]
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + dimenValue + "</dimen>"";\n")
		
		#web dimens 
		bordersDimens = parse.getBorders()
		for borders in bordersDimens:
			arr = borders.split("=")
			className = arr[0].strip().replace(".","-").replace("-", "_").lower()
			h.write("$" + className + ":" + arr[1] + ";" +  "\n")

		spacingsValues = parse.getSpacings()
		for spacing in spacingsValues:
			arr = spacing.split("=")
			className = arr[0].strip().replace(".","-").replace("-", "_").lower()
			g.write("$" + className + ":" + arr[1] + ";" +  "\n")

		shadowValuesAndroid = parse.getShadowAndroid()
		for shadows in shadowValuesAndroid:
			arr = shadows.split("=")
			tokenShadow = arr[0].replace("-","_").replace(" ", "")
			if arr[1] == "0":
				elevation = "0"
				f.write("<dimen name = " + "\"" + tokenShadow +"\"" + ">" + elevation + "</dimen>"";\n")
			else:
				elevation = arr[1]
				f.write("<dimen name = " + "\"" + tokenShadow +"\"" + ">" + elevation + "</dimen>"";\n")

		f.write("</resources>")
		f.close()
		g.close()
		h.close()

		shadowValues = parse.getShadows()
		file_shadow = "shadows.scss"
		i = open(os.path.join(path, file_shadow),"w+")
		for shadows in shadowValues:
			arr = shadows.split("=")
			tokenShadow = arr[0]
			if arr[1] == "0":
				elevation = "0"
				i.write("$" + tokenShadow + ":" + elevation  + ";" + "\n")
			else:
				elevation = arr[1]
				i.write("$" + tokenShadow + ":" + elevation + ";" + "\n")
		i.close()

		#oldDimens
		path = "ata"
		file_name = "ata.xml"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		f = open(os.path.join(path, file_name),"w+")
		f.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
		f.write("<resources> \n\n")		

		fontSizes = parse.getFontSizes()
		for size in fontSizes:
			arr = size.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + str(int(float(arr[1].strip()))) + "dp" + "</dimen>"";\n")


		borderWeights = parse.getBorderWeights()
		for weight in borderWeights:
			arr = weight.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + arr[1].strip() + "dp" + "</dimen>"";\n")
		

		radius = parse.getBorderRadius()
		for radius in radius:
			arr = radius.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + arr[1].strip() + "dp" + "</dimen>"";\n")


		lineHeights = parse.getLineHeights()
		for lineHeight in lineHeights:
			arr = lineHeight.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + arr[1].strip() + "dp" + "</dimen>"";\n")


		spacingStacks = parse.getSpacingStacks()
		for spacingStack in spacingStacks:
			arr = spacingStack.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + arr[1].strip() + "dp" + "</dimen>"";\n")

		spacingInlines = parse.getSpacingInlines()
		for spacingInline in spacingInlines:
			arr = spacingInline.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + arr[1].strip() + "dp" + "</dimen>"";\n")

		f.write("</resources>")
		f.close()
	

		#whatever (remover)
		path = "whatever"
		file_name = "whatever.xml"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		f = open(os.path.join(path, file_name),"w+")
		f.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
		f.write("<resources> \n\n")

		opacitys = parse.getOpacitys()
		for opacity in opacitys:
			arr = opacity.split("=")
			className = arr[0].strip().replace(".","").lower()
			f.write("<style name = " + "\"" + className +"\"" + ">\n")
			f.write("$" + className + ":" + '%.2f'%(float(arr[1].strip())) + ";\n")


		insets = parse.getInsets()
		for inset in insets:
			arr = inset.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")


		squishs = parse.getSquishs()
		for squish in squishs:
			arr = squish.split("=")
			className = arr[0].strip().replace(".","-").lower()
			f.write("$" + className + ":" + arr[1].strip() + ";\n")

		f.write("</resources>")
		f.close()

		#iconografia
		svgpaths = parse.getSvgPath()
		path = "icons xml"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		for pathSVG in svgpaths:
			arr = pathSVG.split("=")
			file_name = arr[0] + ".xml"
			f = open(os.path.join(path, file_name),"w+")
			f.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			f.write("<vector xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ "\n\n")
			f.write("android:viewportWidth=" + "\"" +"200" + "\"\n")
			f.write("android:viewportHeight=" + "\"" +"200" +"\""+ "\n" )
			f.write("android:width=" + "\"" +"108dp" + "\"\n")
			f.write("android:height=" + "\"" +"108dp" +"\""+ ">" + "\n\n")
			f.write("<path\n")
			f.write("android:pathData=" + arr[1] + "\n")
			f.write("android:fillColor=" + "\"" + "#008577" + "\"")

			f.write("/>\n")
			f.write("</vector>")

			f.close()

		#imagens
		svgList = parse.getSvgPath()
		path = "icons svg"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)
		
		for imagem in svgList:
			arr = imagem.split("=")
			file_name = arr[0] + ".svg"
			f = open(os.path.join(path, file_name),"w+")
			f.write("<svg " + "width=" + "\"" + "500" + "\"" +  " height=" + "\"" + "300" + "\"" + " viewBox=" + "\"" + "0 0 500 300" + "\"" + " fill=" + "\"" + "none" + "\"")
			f.write(" xmlns=" + "\""+ "http://www.w3.org/2000/svg" + "\"" + ">" + "\n\n")
			f.write("<path d=" + arr[1])
			f.write(" fill=" + "\"" + "#008577" + "\"")
			f.write("/>\n")
			f.write("</svg>")

			f.close()
	
		#componentes
		
		componentesList = parse.getComponentes()
		checkBoxList = parse.getCheckBoxes()
		autocompleteList = parse.getAutocompletes()
		radioButtonsList = parse.getRadioButtons()
		tooglesLits = parse.getToogles()
		slidersList = parse.getSliders()
		progressBarList = parse.getProgressBar()
		searchList = parse.getSearch()
		tooltipList = parse.getTooltips()
		chipsList = parse.getChips()
		textAreaList = parse.getTextArea()
		overFlowMenuList = parse.getOverflowMenu()
		navigationBarList = parse.getNavigationBar()
		datePickerList = parse.getDatePicker()
		timePickerList = parse.getTimePicker()
		buttonList = parse.getButtons()
		cardList = parse.getCards()
		dropDownList = parse.getDropDown()

		path = "values"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s " % path)

		file_name = "styles.xml"
		f = open(os.path.join(path, file_name),"w+")
		f.seek(0)
		f.truncate()
		f.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
		f.write("<resources xmlns:tools=" + "\"" + "http://schemas.android.com/tools" + "\"" + "> \n\n")

		path = "drawable"
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
				print ("Creation of the directory %s failed" % path)
		else:
				print ("Successfully created the directory %s " % path)

		for buttons in buttonList:
			arr = buttons.split("-")
			token_componente = arr[0].split("=")[1].lower() + ".xml"
			backgroundColor = arr[1].split("=")[1]
			strokeColor = arr[5].split("=")[1]

			if backgroundColor.lower() == "#000000" or backgroundColor.lower() == "":
				backgroundColor = "#00000000"
			
			if strokeColor.lower() == "#000000" or strokeColor.lower() == "":
				strokeColor = "#00000000"

			g = open(os.path.join(path, token_componente),"w+")
			g.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			g.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			g.write("<solid\n")
			g.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			g.write("</solid>\n\n")
			g.write("<stroke\n")
			g.write("android:width=" + "\"" + "1dp" + "\"" + "\n")
			g.write("android:color=" + "\"" + strokeColor + "\"" + ">" +"\n")
			g.write("</stroke>\n")
			g.write("<corners\n")
			g.write("android:radius=" + "\"" + arr[2].split("=")[1].split(".")[0] + "dp"  + "\"" + ">" +"\n")
			g.write("</corners>\n")
			g.write("</shape>")
			g.close()

			f.write("<style name = " + "\"" + token_componente.split(".")[0] +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:background" +"\"" + ">" + "@drawable/" + token_componente.split(".")[0] + "</item>""\n")
			f.write("<item name = " + "\"" + "android:textSize" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + "12" + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + "android:fontFamily" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + "Roboto"+ "</item>""\n")
			f.write("<item name = " + "\"" + "android:textColor" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + "#FFFF" + "</item>""\n")			
			f.write("</style>\n\n")

		for componente in componentesList:

			arr = componente.split("-")
			f.write("<style name = " + "\"" + arr[0].split("=")[1].replace("/", "_").replace(" ", "").lower() +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:background" +"\"" + ">" + "@drawable/" + arr[0].split("=")[1].replace("/", "_").replace(" ", "").lower() + "</item>""\n")
			f.write("<item name = " + "\"" + arr[2].split("=")[0] +"\"" + ">" + arr[2].split("=")[1].split(".")[0] + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + arr[3].split("=")[0] +"\"" + ">" + arr[3].split("=")[1].split(".")[0] + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + arr[4].split("=")[0] +"\"" + ">" + arr[4].split("=")[1].split(".")[0] + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + arr[5].split("=")[0] +"\"" + ">" + arr[5].split("=")[1].split(".")[0] +  "</item>""\n")
			f.write("<item name = " + "\"" + arr[6].split("=")[0] +"\"" + ">" + arr[6].split("=")[1].split(".")[0] + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + arr[7].split("=")[0] +"\"" + ">" + arr[7].split("=")[1] + "</item>""\n")
			f.write("</style>\n\n")
		
		for checkboxes in checkBoxList:
			arr = checkboxes.split("-")
			f.write("<style name = " + "\"" + arr[0].split("=")[1].replace("/", "_").replace(" ", "") +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:colorControlNormal" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "#FFF" + "</item>""\n")
			f.write("<item name = " + "\"" + "android:colorControlActivated" +"\"" + " tools:targetApi=" +  "\"" + "lollipop" +  "\"" + ">" + arr[1].split("=")[1] + "</item>""\n")
			f.write("<item name = " + "\"" + "android:textSize" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + arr[2].split("=")[1].split(".")[0] + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + "android:fontFamily" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + arr[3].split("=")[1]+ "</item>""\n")
			f.write("</style>\n\n")

		for autocomplete in autocompleteList:
			arr = autocomplete.split("-")
			f.write("<style name = " + "\"" + "listViewStyle" + "\"" + " parent=" +  "\"" + "Widget.AppCompat.ListView.DropDown" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:background" + "\"" + ">" + arr[0].split("=")[1] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:selectableItemBackground" + "\"" + ">" + arr[1].split("=")[1] + "</item>" + "\n")
			f.write("</style>\n\n")

			f.write("<style name = " + "\"" + "dropDownStyle" + "\""  + " parent=" +  "\"" + "Widget.AppCompat.DropDownItem.Spinner" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\"" + ">" + "#000000" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\"" + ">" + "16dp" + "</item>"+"\n")
			f.write("</style>\n\n")

			f.write("<style name = " + "\"" + "autocompleteStyle" + "\""  + " parent=" +  "\"" + "Widget.AppCompat" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\"" + ">" + "#000000" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\"" + ">" + "16dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:dropDownItemStyle" + "\"" + ">" + "@style/dropDownStyle" + "</item>" + "\n")
			f.write("<item name = " + "\"" + "android:dropDownListViewStyle" + "\"" + ">" + "@style/listViewStyle" + "</item>"+"\n")
			f.write("</style>\n\n")

		for radioButton in radioButtonsList:
			arr = radioButton.split("-")
			f.write("<style name = " + "\"" + arr[0].split("=")[1] + "\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:colorControlNormal" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "#FFFF" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:colorControlActivated" + "\""  " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[1].split("=")[1] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColorPrimaryDisableOnly" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[1].split("=")[1] + "</item>" + "\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[1].split("=")[1] + "</item>" + "\n")
			f.write("<item name = " + "\"" + "android:buttonTint" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[2].split("=")[1] + "</item>" + "\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("</style>\n\n")

		for toogles in tooglesLits:
			arr = toogles.split("-")
			situation = arr[0].split("=")[1]

			f.write("<style name = " + "\"" +situation + "\"" + ">" + "\n")

			if situation.lower()=="toogle_off":
				colorDisabled = arr[1].split("-")[1]
				f.write("<item name = " + "\"" + "android:colorControlNormal" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + colorDisabled + "</item>"+"\n")
			
			if situation.lower() == "toogle_on":
				colorEnabled = arr[1].split("-")[1]
				f.write("<item name = " + "\"" + "android:colorControlActivated" + "\""  " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + colorEnabled + "</item>"+"\n")

		
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[1].split("=")[1] + "</item>" + "\n")
			f.write("<item name = " + "\"" + "android:strokeColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[2].split("=")[1] + "</item>" + "\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("</style>\n\n")

		for slider in slidersList:
			arr = slider.split("-")
			colorBackground = arr[0].split("=")[1]
			colorProgress =  arr[1].split("=")[1]
			name = arr[2].split("=")[1]

			f.write("<style name = " + "\"" + name +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:progressBackgroundTint" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + colorBackground + "</item>""\n")
			f.write("<item name = " + "\"" + "android:progressTint" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + colorProgress+ "</item>""\n")
			f.write("<item name = " + "\"" + "android:colorControlActivated" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" +colorProgress + "</item>""\n")			
			f.write("</style>\n\n")		

		for progressbar in progressBarList:
			arr = progressbar.split("-")
			f.write("<style name = " + "\"" + arr[0].split("=")[1].replace(" ", "") + "\"" + " parent=" +  "\"" + "Widget.AppCompat.ProgressBar.Horizontal" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:progressTint" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[1].split("=")[1] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:progressBackgroundTint" + "\""  " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[2].split("=")[1] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("</style>\n\n")

		for search in searchList:

			iconfile = "searchicon.xml"

			arr = search.split("-")
			tokenComponente = arr[0].split("=")[1] + ".xml"
			backgroundColor = arr[1].split("=")[1]
			colorIcon = arr[2].split("=")[1]
			radius = arr[3].split("=")[1].split(".")[0]
			pathIcon = "M15.5,14h-0.79l-0.28,-0.27C15.41,12.59 16,11.11 16,9.5 16,5.91 13.09,3 9.5,3S3,5.91 3,9.5 5.91,16 9.5,16c1.61,0 3.09,-0.59 4.23,-1.57l0.27,0.28v0.79l5,4.99L20.49,19l-4.99,-5zM9.5,14C7.01,14 5,11.99 5,9.5S7.01,5 9.5,5 14,7.01 14,9.5 11.99,14 9.5,14z"

			h = open(os.path.join(path, iconfile),"w+")
			h.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			h.write("<vector xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ "\n\n")
			h.write("android:viewportWidth=" + "\"" +"24.0" + "\"\n")
			h.write("android:viewportHeight=" + "\"" +"24.0" +"\""+ "\n" )
			h.write("android:width=" + "\"" +"24dp" + "\"\n")
			h.write("android:height=" + "\"" +"24dp" +"\""+ ">" + "\n\n")
			h.write("<path\n")
			h.write("android:pathData=" + "\"" + pathIcon + "\"" + "\n")
			h.write("android:fillColor=" + "\"" + colorIcon + "\"")
			h.write("/>\n")
			h.write("</vector>")
			h.close()


			d = open(os.path.join(path, token_componente),"w+")
			d.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			d.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			d.write("<solid\n")
			d.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			d.write("</solid>\n\n")
			d.write("<corners\n")
			d.write("android:radius=" + "\"" + radius + "dp"  + "\"" + ">" +"\n")
			d.write("</corners>\n")
			d.write("</shape>")
			d.close()


			f.write("<style name = " + "\"" + arr[0].split("=")[1].replace(" ", "") + "\"" + " parent=" +  "\"" + "Widget.AppCompat.SearchView" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:background" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" "@drawable/" + token_componente.split(".")[0] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:searchIcon" + "\""  + " tools:ignore=" +  "\"" + "NewApi" +"\"" + ">" + "@drawable/" + iconfile.split(".")[0] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "10dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "#A4AAAC" + "</item>"+"\n")
			f.write("</style>\n\n")

		for tooltip in tooltipList:
			arr = tooltip.split("-")
			token_componente = arr[0].split("=")[1].lower() + ".xml"
			backgroundColor = arr[1].split("=")[1]
			corners = arr[2].split("=")[1]

			x = open(os.path.join(path, token_componente),"w+")
			x.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			x.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			x.write("<solid\n")
			x.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			x.write("</solid>\n\n")
			x.write("<stroke\n")
			x.write("android:width=" + "\"" + "1dp" + "\"" + "\n")
			x.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			x.write("</stroke>\n")
			x.write("<corners\n")
			x.write("android:radius=" + "\"" + corners + "dp"  + "\"" + ">" +"\n")
			x.write("</corners>\n")
			x.write("</shape>")
			x.close()

			f.write("<style name = " + "\"" + token_componente.split(".")[0] + "\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:colorBackground" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + arr[1].split("=")[1] + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "#FFFF" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:fontSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "12dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:lineSpacingExtra" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "12dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:cornerRadius" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "15dp" + "</item>"+"\n")
			f.write("</style>\n\n")

		for chips in chipsList:
			
			arr = chips.split("-")

			backgroundColor = arr[0].split("=")[1]
			closeIconColor = arr[1].split("=")[1]

			f.write("<style name = " + "\"" + "chip_contact_photo_icon" + "\"" + " parent=" +  "\"" + "Widget.MaterialComponents.Chip.Entry" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "chipBackgroundColor" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + backgroundColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "iconEndPadding" + "\""  " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "10dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "chipIconSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "32dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "iconStartPadding" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "-4dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "12dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + closeIconColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "closeIconTint" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + closeIconColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "enforceTextAppearance" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "false" + "</item>"+"\n")
			f.write("</style>\n\n")

			f.write("<style name = " + "\"" + "chip_contact_photo" + "\"" + " parent=" +  "\"" + "Widget.MaterialComponents.Chip.Action" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "chipBackgroundColor" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + backgroundColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "iconEndPadding" + "\""  " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "10dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "chipIconSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "32dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "iconStartPadding" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "-4dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "12dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + closeIconColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "enforceTextAppearance" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "false" + "</item>"+"\n")
			f.write("</style>\n\n")

			f.write("<style name = " + "\"" + "chip_text_icon" + "\"" + " parent=" +  "\"" + "Widget.MaterialComponents.Chip.Entry" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "chipBackgroundColor" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + backgroundColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "12dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + closeIconColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "enforceTextAppearance" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "false" + "</item>"+"\n")
			f.write("</style>\n\n")

			f.write("<style name = " + "\"" + "chip_text" + "\"" + " parent=" +  "\"" + "Widget.MaterialComponents.Chip.Choice" +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "chipBackgroundColor" + "\"" + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + backgroundColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textSize" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "12dp" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:textColor" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + closeIconColor + "</item>"+"\n")
			f.write("<item name = " + "\"" + "android:fontFamily" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "Roboto" + "</item>"+"\n")
			f.write("<item name = " + "\"" + "enforceTextAppearance" + "\""  + " tools:targetApi=" +  "\"" + "lollipop" +"\"" + ">" + "false" + "</item>"+"\n")
			f.write("</style>\n\n")

		for textArea in textAreaList:
			arr = textArea.split("-")
			token_componente = arr[0].split("=")[1].lower() + ".xml"
			backgroundColor = arr[1].split("=")[1]
			corners = arr[2].split("=")[1]

			u = open(os.path.join(path, token_componente),"w+")
			u.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			u.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			u.write("<solid\n")
			u.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			u.write("</solid>\n\n")
			u.write("<stroke\n")
			u.write("android:width=" + "\"" + "1dp" + "\"" + "\n")
			u.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			u.write("</stroke>\n")
			u.write("<corners\n")
			u.write("android:radius=" + "\"" + corners + "dp"  + "\"" + ">" +"\n")
			u.write("</corners>\n")
			u.write("</shape>")
			u.close()

			f.write("<style name = " + "\"" + token_componente.split(".")[0] +"\"" + ">" + "\n")
			f.write("<item name = " + "\"" + "android:background" +"\"" + ">" + "@drawable/" + token_componente.split(".")[0] + "</item>""\n")
			f.write("<item name = " + "\"" + "android:textSize" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + "12" + "dp" + "</item>""\n")
			f.write("<item name = " + "\"" + "android:fontFamily" +"\"" + " tools:targetApi="+   "\"" + "lollipop" +"\"" + ">" + "Roboto"+ "</item>""\n")			
			f.write("</style>\n\n")

		for overflowMenu in overFlowMenuList:
			arr = overflowMenu.split("=")
			colorBackgroundMenu = ""
			colorIconSelected = ""
			colorTextSelected = ""
			colorItemSelected = ""
			colorTextNormal = ""
			tokenComponente = ""
			corners = ""

		for navigationBar in navigationBarList: 
			arr = navigationBar.split("-")
			colorToolbar = arr[0].split("=")[1]
			colorStatusBar = arr[1].split("=")[1]
			colorTittle = arr[2].split("=")[1]
			name = arr[3].split("=")[1]

		for datePicker in datePickerList:
			arr = datePicker.split("-")
			datePickerColor = arr[0].split("=")[1]
		
		for timePicker in timePickerList:
			arr = timePicker.split("-")
			timePickerColor = arr[0].split("=")[1]

		for cards in cardList:
			arr = cards.split("-")
			nome = arr[0].split("=")[1]
			backgroundColor = arr[1].split("=")[1]
			radius = arr[2].split("=")[1].split(".")[0]
			arquivo = nome + ".xml"

			d = open(os.path.join(path, arquivo),"w+")
			d.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			d.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			d.write("<solid\n")
			d.write("android:color=" + "\"" + backgroundColor + "\"" + ">" +"\n")
			d.write("</solid>\n\n")
			d.write("<corners\n")
			d.write("android:radius=" + "\"" + radius + "dp"  + "\"" + ">" +"\n")
			d.write("</corners>\n")
			d.write("</shape>")
			d.close()

		for dropDown in dropDownList:
			arr = dropDown.split("-")
			iconfile = "arrowdown.xml"
			tokenComponente = "selectbackground.xml"
			colorDivider = arr[0].split("=")[1]
			colorListOptions = arr[1].split("=")[1]
			colorSelectBackground = arr[2].split("=")[1]
			pathIcon = "M16.59,8.59L12,13.17 7.41,8.59 6,10l6,6 6,-6z"
			colorIcon = arr[3].split("=")[1]
			radius = arr[4].split("=")[1].split(".")[0]

			h = open(os.path.join(path, iconfile),"w+")
			h.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			h.write("<vector xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ "\n\n")
			h.write("android:viewportWidth=" + "\"" +"24.0" + "\"\n")
			h.write("android:viewportHeight=" + "\"" +"24.0" +"\""+ "\n" )
			h.write("android:width=" + "\"" +"24dp" + "\"\n")
			h.write("android:height=" + "\"" +"24dp" +"\""+ ">" + "\n\n")
			h.write("<path\n")
			h.write("android:pathData=" + "\"" + pathIcon + "\"" + "\n")
			h.write("android:fillColor=" + "\"" + colorIcon + "\"")
			h.write("/>\n")
			h.write("</vector>")
			h.close()

			d = open(os.path.join(path, tokenComponente),"w+")
			d.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			d.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			d.write("<solid\n")
			d.write("android:color=" + "\"" + colorSelectBackground + "\"" + ">" +"\n")
			d.write("</solid>\n\n")
			d.write("<corners\n")
			d.write("android:radius=" + "\"" + radius + "dp"  + "\"" + ">" +"\n")
			d.write("</corners>\n")
			d.write("</shape>")
			d.close()


		f.write("\n\n</resources>")
		f.close()

		print("-----------------------------------------------")
		print("Arquivos Android exportados com sucesso!\n\n")


	def detectFrames(abc,frame):
		
		abc.detectColors(frame)
		abc.detectBorderWidth(frame)
		abc.detectBorderRadius(frame)
		abc.detectShadow(frame)
		abc.detectFontFamily(frame)
		abc.detectFontSize(frame)
		abc.detectOpacity(frame)
		abc.detectSpacing(frame)
		abc.detectLineHeight(frame)
		abc.detectSvgPath(frame)
		abc.detectImagens(frame)
		abc.detectComponents(frame)

	def detectComponents(abc,frame):
		if frame["name"].lower() == "componentes_atech": #frame
			if "children" in frame:
				frame_content = frame["children"]
				for group_component in frame_content: #grupo de componentes
					groupName = group_component["name"]
					corners = ""
					height= ""
					name = ""
					color = ""
					strokeColor = ""
					strokeWeight = ""
					colorProgress = ""
					colorBackgroundProgress = ""
					iconColor = ""
					backgroundColor = ""
					closeIconColor = ""
					selectedItemColor = ""
					selectedIconColor = ""
					colorToolbar = ""
					colorStatusBar = ""
					titlleColor = ""
					colorDatePicker = ""
					colorTimePicker = ""
					colorDivider = ""
					colorListOptions = ""
					item_list = ""
					colorBackground = ""

					if groupName.lower() == "checkbox-group":
						print("entrou no checkboxes")
						fontFamily = ""
						fontSize = ""
						if "children" in group_component:
								subgroup = group_component["children"]
								for subgroup2 in subgroup:
									if "children" in subgroup2:
										subgroup3 = subgroup2["children"]
										for subgroup4 in subgroup3:
											
											if subgroup4 ["type"].lower() == "text":
												print("nome do textview = " + subgroup4["name"])

												if "style" in subgroup4:
													style = subgroup4["style"]
													fontFamily = style["fontFamily"]
													fontSize = style["fontSize"]

											if subgroup4["type"].lower() == "rectangle":
												#print(element["name"])

												strokeColor = ""

												color = subgroup4["fills"][0]["color"]
												r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
												g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
												b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
												color = '#%02x%02x%02x' % ( r, g, b)

												corners = subgroup4["cornerRadius"]
												height = subgroup4["absoluteBoundingBox"]["height"]
												width = subgroup4["absoluteBoundingBox"]["width"]
												name = subgroup2["name"]

												if "strokes" in subgroup4 and len(subgroup4["strokes"]) > 0:
													strokeColor = subgroup4["strokes"][0]["color"]
													r =  255 if strokeColor["r"] >= 1.0  else 0 if strokeColor["r"] <= 0.0 else round(strokeColor["r"] * 255.0)
													g =  255 if strokeColor["g"] >= 1.0  else 0 if strokeColor["g"] <= 0.0 else round(strokeColor["g"] * 255.0)
													b =  255 if strokeColor["b"] >= 1.0  else 0 if strokeColor["b"] <= 0.0 else round(strokeColor["b"] * 255.0)
													strokeColor = '#%02x%02x%02x' % ( r, g, b)

												strokeWeight = subgroup4["strokeWeight"]

												abc.checkBoxes.append("name=" + name  + "-" + "color=" + color + "-" +  "fontSize=" +str(fontSize) + "-" + "fontFamily=" + str(fontFamily) + "-" +  "strokeColor=" + str(strokeColor))

												print("name: " + name + "\n" + "color: " + color +"\n" + "corners: " +str(corners) + "\n" + "height: " +str(height) + "\n" + "width: " + str(width) + "\n" +  "strokeColor: " + str(strokeColor))


											if "children" in subgroup4:
												subgroup5 = subgroup4["children"]
												for element in subgroup5:
								
													if "children" in element:
														subgroup6 = element["children"]
														for obj in subgroup6:
															print(obj["name"])

															if obj["type"].lower() == "rectangle":

																name = subgroup2["name"]
																strokeColor = ""

																color = obj["fills"][0]["color"]
																r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
																g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
																b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
																color = '#%02x%02x%02x' % ( r, g, b)

																if "strokes" in obj and len(obj["strokes"]) > 0:
																	strokeColor = obj["strokes"][0]["color"]
																	r =  255 if strokeColor["r"] >= 1.0  else 0 if strokeColor["r"] <= 0.0 else round(strokeColor["r"] * 255.0)
																	g =  255 if strokeColor["g"] >= 1.0  else 0 if strokeColor["g"] <= 0.0 else round(strokeColor["g"] * 255.0)
																	b =  255 if strokeColor["b"] >= 1.0  else 0 if strokeColor["b"] <= 0.0 else round(strokeColor["b"] * 255.0)
																	strokeColor = '#%02x%02x%02x' % ( r, g, b)

																height = obj["absoluteBoundingBox"]["height"]
																width = obj["absoluteBoundingBox"]["width"]

																corners = obj["cornerRadius"]
																abc.checkBoxes.append("name=" + name  + "-" + "color=" + color + "-" +  "fontSize=" +str(fontSize) + "-" + "fontFamily=" + str(fontFamily) + "-" +  "strokeColor=" + str(strokeColor))


																print(str(color) + "\n" + str(height) + "\n" + str(width) + "\n" + str(corners) + "\n" + str(strokeColor) +  "\n")

															if obj ["type"].lower() == "text":
																print("amém")
													
													else:
														print(element["name"])

														if element["type"].lower() == "rectangle":

															name = subgroup2["name"]

															color = element["fills"][0]["color"]
															r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
															g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
															b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
															color = '#%02x%02x%02x' % ( r, g, b)

															if "strokes" in element and len(element["strokes"])>0:
																strokeColor = element["strokes"][0]["color"]
																r =  255 if strokeColor["r"] >= 1.0  else 0 if strokeColor["r"] <= 0.0 else round(strokeColor["r"] * 255.0)
																g =  255 if strokeColor["g"] >= 1.0  else 0 if strokeColor["g"] <= 0.0 else round(strokeColor["g"] * 255.0)
																b =  255 if strokeColor["b"] >= 1.0  else 0 if strokeColor["b"] <= 0.0 else round(strokeColor["b"] * 255.0)
																strokeColor = '#%02x%02x%02x' % ( r, g, b)

															height = element["absoluteBoundingBox"]["height"]
															width = element["absoluteBoundingBox"]["width"]

															corners = element["cornerRadius"]

															abc.checkBoxes.append("name=" + name  + "-" + "color=" + color + "-" +  "fontSize=" +str(fontSize) + "-" + "fontFamily=" + str(fontFamily) + "-" +  "strokeColor=" + str(strokeColor))

															print(str(color) + "\n" + str(height) + "\n" + str(width) + "\n" + str(corners) + "\n" + str(strokeColor) +  "\n")
				
					if groupName.lower() == "button-group":
						print("entrou no button-group")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:
												if element["type"].lower() == "rectangle":
													#print(element["name"])

													color = ""
												
													if "fills" in element and len(element["fills"]) > 0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														color = '#%02x%02x%02x' % ( r, g, b)


													if "cornerRadius" in element:
														corners = element["cornerRadius"]
													
													height = element["absoluteBoundingBox"]["height"]
													width = element["absoluteBoundingBox"]["width"]
													name = subgroup2["name"].replace("-", "_").replace(" ", "_")

													if "strokes" in element and len(element["strokes"])>0:
														strokeColor = element["strokes"][0]["color"]
														r =  255 if strokeColor["r"] >= 1.0  else 0 if strokeColor["r"] <= 0.0 else round(strokeColor["r"] * 255.0)
														g =  255 if strokeColor["g"] >= 1.0  else 0 if strokeColor["g"] <= 0.0 else round(strokeColor["g"] * 255.0)
														b =  255 if strokeColor["b"] >= 1.0  else 0 if strokeColor["b"] <= 0.0 else round(strokeColor["b"] * 255.0)
														strokeColor = '#%02x%02x%02x' % ( r, g, b)

													strokeWeight = element["strokeWeight"]

													abc.buttons.append("name=" + name  + "-" + "color=" + color + "-" + "corners=" +str(corners) + "-" +  "height=" +str(height) + "-" + "width=" + str(width) + "-" +  "strokeColor=" + str(strokeColor))

													print("______coisas do group_button_______\n" + str(name)+"\n"+str(color)+"\n"+str(corners)+"\n"+str(height)+"\n"+str(width)+"\n"+str(strokeColor))

					if groupName.lower() == "autocomplete-group":
							print("entrou no autocomplete")
							colorBackground = ""
							colorSelected = ""
							if "children" in group_component:
								subgroup = group_component["children"]
								for subgroup2 in subgroup:
									if "children" in subgroup2:
										listSubGroup2 = subgroup2["children"]
										for obj in listSubGroup2:
											if "children" in obj:
												listObj = obj["children"]
												for component in listObj:
													if "children" in component:
														subgroup3 = component["children"]
														for element in subgroup3:
															print(element["name"])
															if element["type"].lower()=="rectangle" and component["name"].lower()=="select-open":

																if element["name"].lower() == "box-shadow-1":
																	color = element["fills"][0]["color"]
																	r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
																	g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
																	b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
																	colorBackground = '#%02x%02x%02x' % ( r, g, b)

																else: 

																	color = element["fills"][0]["color"]
																	r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
																	g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
																	b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
																	colorSelected = '#%02x%02x%02x' % ( r, g, b)

																abc.autocompletes.append("corBackground=" + str(colorBackground) + "-" + "corSelecionado=" + str(colorSelected))

																print("cor do background: " + str(colorBackground))
																print("cor do elemento selecionado: " + str(colorSelected))

					if groupName.lower() == "radio-group":
						print("entrou no radiobutton")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:
												if element["type"].lower() == "rectangle":


													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														color = '#%02x%02x%02x' % ( r, g, b)

													if "strokes" in element and len(element["strokes"])>0:
														strokeColor = element["strokes"][0]["color"]
														r =  255 if strokeColor["r"] >= 1.0  else 0 if strokeColor["r"] <= 0.0 else round(strokeColor["r"] * 255.0)
														g =  255 if strokeColor["g"] >= 1.0  else 0 if strokeColor["g"] <= 0.0 else round(strokeColor["g"] * 255.0)
														b =  255 if strokeColor["b"] >= 1.0  else 0 if strokeColor["b"] <= 0.0 else round(strokeColor["b"] * 255.0)
														strokeColor = '#%02x%02x%02x' % ( r, g, b)
													
													name = subgroup2["name"].replace("/", "_").replace(" ", "")

													height = element["absoluteBoundingBox"]["height"]
													width = element["absoluteBoundingBox"]["width"]

													corners = element["cornerRadius"]

													item_list = "nome=" + str(name) + "-" + "color=" + str(color) + "-" + "stroke=" + str(strokeColor) + "-" + "height=" + str(height) + "-" + "width=" + str(width) + "-" + "corners=" + str(corners)
													
													if str(item_list) in abc.radioButtons:
														print("")
													else:
														abc.radioButtons.append(str(item_list))

													print("itens do radiobutton" + str(color) +"\n" + str(strokeColor) + "\n" + str(height) + "\n" + str(width) + "\n" + str(corners))
	
					if groupName.lower() == "toogles":
						print("entrou no toogles")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:
												if element["type"].lower() == "rectangle":


													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														color = '#%02x%02x%02x' % ( r, g, b)

													if "strokes" in element and len(element["strokes"])>0:
														strokeColor = element["strokes"][0]["color"]
														r =  255 if strokeColor["r"] >= 1.0  else 0 if strokeColor["r"] <= 0.0 else round(strokeColor["r"] * 255.0)
														g =  255 if strokeColor["g"] >= 1.0  else 0 if strokeColor["g"] <= 0.0 else round(strokeColor["g"] * 255.0)
														b =  255 if strokeColor["b"] >= 1.0  else 0 if strokeColor["b"] <= 0.0 else round(strokeColor["b"] * 255.0)
														strokeColor = '#%02x%02x%02x' % ( r, g, b)

													name = subgroup2["name"].replace("/", "_").replace(" ", "")
													height = element["absoluteBoundingBox"]["height"]
													width = element["absoluteBoundingBox"]["width"]

													corners = element["cornerRadius"]

													abc.toogles.append("nome=" + str(name) + "-" + "color=" + str(color) + "-" + "stroke=" + str(strokeColor) + "-" + "height=" + str(height) + "-" + "width=" + str(width) + "-" + "corners=" + str(corners))

													print("itens do toogles" + str(color) +"\n" + str(strokeColor) + "\n" + str(height) + "\n" + str(width) + "\n" + str(corners))
	
					if groupName.lower() == "slider-group":
						print("entrou no sliders")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:

												name = subgroup4["name"].replace("-", "_")

												if element["name"].lower() == "ellipse":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorProgress = '#%02x%02x%02x' % ( r, g, b)

												if element["type"].lower() == "rectangle" and element["name"].lower() == "backgroundprogress" and element["type"].lower() != "text":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorBackground = '#%02x%02x%02x' % ( r, g, b)

												
												item_list = "backgroundProgress=" + str(colorBackground) + "-" + "colorProgress=" + str(colorProgress) + "-" + "name=" +str(name)
										
												if str(item_list) in abc.sliders:
													print("")
												else:
													abc.sliders.append(str(item_list))							

					if groupName.lower() == "progressbar-group":
						print("entrou no progressbar")
						if "children" in group_component:
							subgroup = group_component["children"]
							for group in subgroup:
								if "children" in group:
									subgroup2 = group["children"]
									for element in subgroup2:

										list_itens = abc.progressbar
									
										token_component = group["name"].lower().replace("-","_")

										if element["type"].lower() == "rectangle" and element["name"].lower() == "progress":

											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											colorProgress = '#%02x%02x%02x' % ( r, g, b)

										if element["type"].lower() == "rectangle" and element["name"].lower() == "background_progress":

											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											colorBackgroundProgress = '#%02x%02x%02x' % ( r, g, b)	
										
										item_list = "nome=" + str(token_component) + "-" + "colorProgress=" + str(colorProgress) + "-" + "colorBackgroundProgress=" + str(colorBackgroundProgress)
										
										if str(item_list) in abc.progressbar:
											print("")
										else:
											abc.progressbar.append(str(item_list))
								
					if groupName.lower() == "search-group":
						print("entrou no search")
						if "children" in group_component:
							subgroup = group_component["children"]
							for group in subgroup:
								if "children" in group:
									subgroup2 = group["children"]
									for element in subgroup2:

										name = "seach_style"

										if element["type"].lower() == "vector" and element["name"].lower() == "search bg" and element["type"].lower() != "text":
											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											backgroundColor = '#%02x%02x%02x' % ( r, g, b)

											if "cornerRadius" in element:
												corners = element["cornerRadius"]

											print(str(backgroundColor))

										if "strokes" in element and len(element["strokes"]) > 0:

											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											strokeColor = '#%02x%02x%02x' % ( r, g, b)

											print(str(strokeColor))

										if "children" in element:
											frameIcon = element["children"]
											for icon in frameIcon:
												color = icon["fills"][0]["color"]
												r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
												g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
												b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
												iconColor = '#%02x%02x%02x' % ( r, g, b)
										
										item_list = "name=" + str(name) + "-" + "backgroundColor=" + str(backgroundColor) + "-" + "iconColor=" + str(iconColor) + "-" + "corners=" + str(corners)
										
										if str(item_list) in abc.search:
											print("")
										else:
											abc.search.append(str(item_list))

					if groupName.lower() == "tooltip-group":
						print("entrou no tooltips")
						if "children" in group_component:
							subgroup = group_component["children"]
							for group in subgroup:
								if "children" in group:
									subgroup2 = group["children"]
									for element in subgroup2:
										if element["type"].lower() == "vector" and element["type"].lower() != "text":

											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											backgroundColor = '#%02x%02x%02x' % ( r, g, b)

											if "cornerRadius" in element:
												corners = element["cornerRadius"]

											item_list = "name=" + "tooltipStyle" + "-" + "backgroundColor=" + str(backgroundColor) + "-" + "cornerRadius=" + str(corners)
										
											if str(item_list) in abc.tooltips:
												print("")
											else:
												abc.tooltips.append(str(item_list))

					if groupName.lower() == "chips-group":
						print("entrou no chips")
						if "children" in group_component:
							subgroup = group_component["children"]
							for group in subgroup:
								if "children" in group:
									subgroup2 = group["children"]
									for element in subgroup2:

										if element["type"].lower() == "rectangle" and element["type"].lower() != "text" and element["name"].lower() == "chip-bg":
											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											backgroundColor = '#%02x%02x%02x' % ( r, g, b)

										if element["type"].lower() == "vector" and element["type"].lower() != "text" and element["name"].lower() == "subtract":
											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											closeIconColor = '#%02x%02x%02x' % ( r, g, b)

										item_list = "backgroundColor=" + str(backgroundColor) + "-" + "closeIconColor=" + str(closeIconColor)
										
										if str(item_list) in abc.chips:
											print("")
										else:
											abc.chips.append(str(item_list))
										
										print("corBakcground= " + str(backgroundColor) + "\n" + "corCloseIcon= " + str(closeIconColor))

					if groupName.lower() == "textarea-group":
						print("entrou no textarea")
						if "children" in group_component:
							subgroup = group_component["children"]
							for group in subgroup:
								if "children" in group:
									subgroup2 = group["children"]
									for element in subgroup2:
										if element["type"].lower() == "rectangle" and element["type"].lower() != "text":

											name = group["name"]

											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											backgroundColor = '#%02x%02x%02x' % ( r, g, b)

											if "cornerRadius" in element:
												corners = element["cornerRadius"]

											item_list = "name=" + name + "-" + "backgroundColor=" + str(backgroundColor) + "-" + "cornerRadius=" + str(corners)
										
											if str(item_list) in abc.textArea:
												print("")
											else:
												abc.textArea.append(str(item_list))

					if groupName.lower() == "overflow-menu-group":
						print("entrou no overflow")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:

												name = subgroup4["name"].replace("-", "_")

												if subgroup4["name"].lower() == "overflow-menu" and element["type"].lower() == "rectangle" and element["name"].lower() == "background-overflow":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorBackground = '#%02x%02x%02x' % ( r, g, b)

													if "cornerRadius" in element:
														corners = element["cornerRadius"]
												
												if subgroup4["name"].lower() == "overflow-menu" and element["type"].lower() == "rectangle" and element["name"].lower() == "selected-item":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														selectedItemColor = '#%02x%02x%02x' % ( r, g, b)
												
												if subgroup4["name"].lower() == "overflow-menu" and element["type"].lower() == "vector" and element["name"].lower() == "vector-selected":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														selectedIconColor = '#%02x%02x%02x' % ( r, g, b)
													
												
												item_list = "colorBackground=" + str(colorBackground) + "-" + "selectedItemColor=" + str(selectedItemColor) + "-" + "selectedIconColor=" +str(selectedIconColor) + "-" + "corners=" + str(corners) + "-" + "name=" + str(name)
										
												if str(item_list) in abc.overflowMenu:
													print("")
												else:
													abc.overflowMenu.append(str(item_list))							

					if groupName.lower() == "navigationbar-group":
						print("entrou no navigation-bar")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:

												name = subgroup4["name"].replace("-", "_")

												if subgroup4["name"].lower() == "appheader" and element["type"].lower() == "rectangle" and element["name"].lower() == "toolbar":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorToolbar = '#%02x%02x%02x' % ( r, g, b)

												
												if subgroup4["name"].lower() == "status-bar" and element["type"].lower() == "rectangle" and element["name"].lower() == "statusbar":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorStatusBar = '#%02x%02x%02x' % ( r, g, b)
												
												if subgroup4["name"].lower() == "appheader" and element["type"].lower() == "text":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														titlleColor = '#%02x%02x%02x' % ( r, g, b)
												
												item_list = "colorToolbar=" + str(colorToolbar) + "-" + "colorStatusBar=" + str(colorStatusBar) + "-" + "titlleColor=" +str(titlleColor) + "-"  + "name=" + str(name)
										
												if str(item_list) in abc.navigationBar:
													print("")
												else:
													abc.navigationBar.append(str(item_list))							

					if groupName.lower() == "datepicker-group":
						print("entrou no datepicker")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:

												name = subgroup4["name"].replace("-", "_")

												if element["type"].lower() == "vector" and element["name"].lower() == "datepicker-icon":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorDatePicker = '#%02x%02x%02x' % ( r, g, b)
												
												item_list = "colorDatePicker=" + str(colorDatePicker)
												print(str(item_list))
										
												if str(item_list) in abc.datePicker:
													print("")
												else:
													abc.datePicker.append(str(item_list))	
					
					if groupName.lower() == "timepicker-group":
						print("entrou no timepicker")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:

												name = subgroup4["name"].replace("-", "_")

												if element["type"].lower() == "vector" and element["name"].lower() == "vector":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorTimePicker = '#%02x%02x%02x' % ( r, g, b)
												
												item_list = "colorTimePicker=" + str(colorTimePicker)
												print(str(item_list))
										
												if str(item_list) in abc.timePicker:
													print("")
												else:
													abc.timePicker.append(str(item_list))	
					
					if groupName.lower() == "select":
						print("entrou no select")
						if "children" in group_component:
							subgroup = group_component["children"]
							for subgroup2 in subgroup:
								if "children" in subgroup2:
									subgroup3 = subgroup2["children"]
									for subgroup4 in subgroup3:
										if "children" in subgroup4:
											subgroup5 = subgroup4["children"]
											for element in subgroup5:

												name = subgroup4["name"].replace("-", "_")

												if element["name"].lower() == "divider":
													if "strokes" in element and len(element["strokes"])>0:
														color = element["strokes"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorDivider = '#%02x%02x%02x' % ( r, g, b)
												
												if element["name"].lower() == "listoptions":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorListOptions = '#%02x%02x%02x' % ( r, g, b)

												if element["name"].lower() == "selectbackground":
													if "fills" in element and len(element["fills"])>0:
														color = element["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														colorSelectBackground = '#%02x%02x%02x' % ( r, g, b)

														if "cornerRadius" in element:
															corners = element["cornerRadius"]
													
												if "children" in element:
													frameIcon = element["children"]
													for icon in frameIcon:
														color = icon["fills"][0]["color"]
														r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
														g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
														b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
														iconColor = '#%02x%02x%02x' % ( r, g, b)
												
												if colorDivider.lower() != "" and colorListOptions.lower() != "" and colorSelectBackground != "" and iconColor != "":
													item_list = "colorDivider=" + str(colorDivider) + "-" + "colorListOptions=" + str(colorListOptions) + "-" + "colorSelectBackground=" + str(colorSelectBackground) + "-" + "iconColor=" + str(iconColor) + "-" + "corners=" + str(corners)
													print(str(item_list))
											
													if str(item_list) in abc.dropDown:
														print("")
													else:
														abc.dropDown.append(str(item_list))	

					if groupName.lower() == "cards-group":
						print("entrou no cards")
						if "children" in group_component:
							subgroup = group_component["children"]
							for group in subgroup:
								if "children" in group:
									subgroup2 = group["children"]
									for element in subgroup2:
										if element["type"].lower() == "rectangle" and element["type"].lower() != "text":

											color = element["fills"][0]["color"]
											r =  255 if color["r"] >= 1.0  else 0 if color["r"] <= 0.0 else round(color["r"] * 255.0)
											g =  255 if color["g"] >= 1.0  else 0 if color["g"] <= 0.0 else round(color["g"] * 255.0)
											b =  255 if color["b"] >= 1.0  else 0 if color["b"] <= 0.0 else round(color["b"] * 255.0)
											backgroundColor = '#%02x%02x%02x' % ( r, g, b)

											if "cornerRadius" in element:
												corners = element["cornerRadius"]

											item_list = "name=" + "cardbackground" + "-" + "backgroundColor=" + str(backgroundColor) + "-" + "cornerRadius=" + str(corners)
										
											print("card=  " + str(item_list))
											if str(item_list) in abc.cards:
												print("")
											else:
												abc.cards.append(str(item_list))
		
					
	def _detectComponents(abc,frame):
		return
		objFontFamily = "Roboto"
		objFontSize = "12"
		corDaFonte = "#0000"
		colorStroke = "#00212429"
		colorFill = "#00212429"
		if frame["name"].lower() == "componentes-flavio":
			
			for component in frame["children"]:
				if "children" in component:
					child = component["children"]
					
					for obj in child["children"]:

						if obj["type"].lower() == "frame":
							frame = obj["name"]

						if obj["type"].lower() == "group":
							group = obj["children"]
							for element in group:
								if element["type"].lower() == "text": 


									objFontFamily = obj["style"]["fontFamily"]
									objFontSize = obj["style"]["fontSize"]

									fills = element["fills"][0]["color"]
									r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
									g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
									b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
									corDaFonte = '#%02x%02x%02x' % ( r, g, b)

								else:

									nome = component["name"].lower().replace("/", "_")

									height = element["absoluteBoundingBox"]["height"]
									width = element["absoluteBoundingBox"]["width"]
									cornerRadius = element["cornerRadius"]

									if element["effects"]:
										radius = element["effects"][0]["radius"]
										Type = element["type"]

									
									if "strokes" in element:
										if len(element["strokes"]) > 0:
											strokes = element["strokes"]
											fills = strokes[0]["color"]
											r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
											g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
											b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
											colorStroke = '#%02x%02x%02x' % ( r, g, b)
									else:
										if len(element["fills"]) > 0:
											fills = element["fills"][0]["color"]
											r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
											g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
											b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
											colorFill = '#%02x%02x%02x' % ( r, g, b)
											colorStroke = colorFill 

									if len(element["fills"]) > 0:
										fills = element["fills"][0]["color"]
										r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
										g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
										b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
										colorFill = '#%02x%02x%02x' % ( r, g, b)
									
									else:
										colorFill = "#00212429"


						if obj["type"].lower() == "text":
							objFontFamily = obj["style"]["fontFamily"]
							objFontSize = obj["style"]["fontSize"]

							fills = obj["fills"][0]["color"]
							r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
							g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
							b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
							corDaFonte = '#%02x%02x%02x' % ( r, g, b)

							
						if obj['type'].lower().split(" ")[0] == "rectangle":
							nome = component["name"].lower().replace("/", "_")

							if "strokes" in obj:
								if len(obj["strokes"]) > 0:
									strokes = obj["strokes"]
									fills = strokes[0]["color"]
									r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
									g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
									b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
									colorStroke = '#%02x%02x%02x' % ( r, g, b)
							else:
								if len(obj["fills"]) > 0:
									fills = obj["fills"][0]["color"]
									r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
									g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
									b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
									colorFill = '#%02x%02x%02x' % ( r, g, b)
									colorStroke = colorFill 

							if len(obj["fills"]) > 0:
								fills = obj["fills"][0]["color"]
								r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
								g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
								b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
								colorFill = '#%02x%02x%02x' % ( r, g, b)
							
							else:
								colorFill = "#00212429"


							height = obj["absoluteBoundingBox"]["height"]
							width = obj["absoluteBoundingBox"]["width"]
							cornerRadius = obj["cornerRadius"]

							if obj["effects"]:
								radius = obj["effects"][0]["radius"]
								Type = obj["type"]

					componenteTotal = "nome=" + nome + "-" + "android:background=" + colorFill + "-" + "android:layout_height=" + str(height) + "-" + "android:layout_width=" + str(width) + "-" +  "android:radius=" + str(cornerRadius) + "-" + "android:fontFamily=" + objFontFamily + "-" + "android:textSize=" + str(objFontSize) + "-" + "android:textColor=" + corDaFonte + "-" + "borderColor=" + colorStroke
					abc.componentes.append(componenteTotal)

	def detectButton(abc, component):
		for obj in component["children"]:
			if obj["type"].lower() == "rectangle":
				weight = obj["strokeWeight"]
				abc.borderWeights.append("Border.Width." + obj["name"] + " = " + str(weight) + "px" )

	def detectColors(abc,frame): 
		if frame["name"].lower() == "colors":
			for group in frame["children"]:
				if group["type"].lower() == "group":
					groupName = group["name"]
					if groupName.lower() == "gradient colors":
						for gradientGroup in group["children"]:
							if "children" in gradientGroup:
								for gradient in gradientGroup["children"]:
									if "children" in gradient:
										for obj in gradient["children"]:
												if obj["type"].lower() == "rectangle":
													if len(obj["fills"]) > 0:
														for cor in obj["fills"]:

															colorName = obj["name"]

															corUm = obj["fills"][0]["gradientStops"][0]["color"]
															r =  255 if corUm["r"] >= 1.0  else 0 if corUm["r"] <= 0.0 else round(corUm["r"] * 255.0)
															g =  255 if corUm["g"] >= 1.0  else 0 if corUm["g"] <= 0.0 else round(corUm["g"] * 255.0)
															b =  255 if corUm["b"] >= 1.0  else 0 if corUm["b"] <= 0.0 else round(corUm["b"] * 255.0)
															startColor = '#%02x%02x%02x' % ( r, g, b)

															corDois = obj["fills"][0]["gradientStops"][1]["color"]
															r =  255 if corDois["r"] >= 1.0  else 0 if corDois["r"] <= 0.0 else round(corDois["r"] * 255.0)
															g =  255 if corDois["g"] >= 1.0  else 0 if corDois["g"] <= 0.0 else round(corDois["g"] * 255.0)
															b =  255 if corDois["b"] >= 1.0  else 0 if corDois["b"] <= 0.0 else round(corDois["b"] * 255.0)
															endColor = '#%02x%02x%02x' % ( r, g, b)

															abc.gradientColors.append(colorName + "="  + startColor + "=" + endColor)

									else:
										if gradient["type"].lower() == "rectangle":
											if len(gradient["fills"]) > 0:
												for cor in gradient["fills"]:

													colorName = gradient["name"]

													corUm = gradient["fills"][0]["gradientStops"][0]["color"]
													r =  255 if corUm["r"] >= 1.0  else 0 if corUm["r"] <= 0.0 else round(corUm["r"] * 255.0)
													g =  255 if corUm["g"] >= 1.0  else 0 if corUm["g"] <= 0.0 else round(corUm["g"] * 255.0)
													b =  255 if corUm["b"] >= 1.0  else 0 if corUm["b"] <= 0.0 else round(corUm["b"] * 255.0)
													startColor = '#%02x%02x%02x' % ( r, g, b)

													corDois = gradient["fills"][0]["gradientStops"][1]["color"]
													r =  255 if corDois["r"] >= 1.0  else 0 if corDois["r"] <= 0.0 else round(corDois["r"] * 255.0)
													g =  255 if corDois["g"] >= 1.0  else 0 if corDois["g"] <= 0.0 else round(corDois["g"] * 255.0)
													b =  255 if corDois["b"] >= 1.0  else 0 if corDois["b"] <= 0.0 else round(corDois["b"] * 255.0)
													endColor = '#%02x%02x%02x' % ( r, g, b)

													abc.gradientColors.append(colorName + "="  + startColor + "=" + endColor)
					else:
						for group2 in group["children"]:

							if "children" in group2:

								for group3 in group2["children"]:

									if "fills" in group3:
										if len(group3["fills"]) > 0:
											fills = group3["fills"][0]["color"]
											r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
											g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
											b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
											rgb = '#%02x%02x%02x' % ( r, g, b)
											abc.colors.append(group3["name"] + " = " + rgb.upper())

									if "children" in group3:

										for group4 in group3["children"]:

											if group4["type"].lower() == "rectangle":
												if "fills" in group4:
													if len(group4["fills"]) > 0:
														fills = group4["fills"][0]["color"]
														r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
														g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
														b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
														rgb = '#%02x%02x%02x' % ( r, g, b)
														abc.colors.append(group4["name"] + " = " + rgb.upper())

											if "children" in group4:
										
												for color in group4["children"]:

													if color["type"].lower() == "rectangle":
														if "fills" in color:
															if len(color["fills"]) > 0:
																fills = color["fills"][0]["color"]
																r =  255 if fills["r"] >= 1.0  else 0 if fills["r"] <= 0.0 else round(fills["r"] * 255.0)
																g =  255 if fills["g"] >= 1.0  else 0 if fills["g"] <= 0.0 else round(fills["g"] * 255.0)
																b =  255 if fills["b"] >= 1.0  else 0 if fills["b"] <= 0.0 else round(fills["b"] * 255.0)
																rgb = '#%02x%02x%02x' % ( r, g, b)
																abc.colors.append(color["name"] + " = " + rgb.upper())		

	def detectFontFamily(abc,frame):
		nomeDaFonte = ""
		conteudoFonte = ""
		if frame["name"].lower() == "tipografia":
			for obj in frame["children"]:
				if obj["type"].lower() == "text":
					if "style" in obj:
						style = obj["style"]
						font = style["fontFamily"]
						fontWeight = style["fontWeight"]
						fontSize = style["fontSize"]
						nomeDaFonte = obj["name"]
						conteudoFonte = obj["characters"]
						lineHeight = style["lineHeightPx"]
						abc.fontFamilies.append(nomeDaFonte + "=" + conteudoFonte + "=" + font + "=" + str(fontSize) + "=" + str(fontWeight) + "=" + str(lineHeight)) 
				else:
					if obj["type"].lower == "group":
						medida = obj["name"]

	def detectFontSize(abc,frame):
		if frame["name"].lower() == "font size":
			for groups in frame["children"]:			
				
				for obj in groups["children"]:
					
					if obj["type"].lower() == "text":

						if "fontSize" in obj:
							size = obj["fontSize"]
							if not "Font.Size." + obj["name"] + " = " + str(size) in abc.fontSizes:
								abc.fontSizes.append("Font.Size." + obj["name"] + " = " + str(size))
						elif "style" in obj:
							style = obj["style"]
							size = style["fontSize"]
							if not "Font.Size." + obj["name"] + " = " + str(size) in abc.fontSizes:
								abc.fontSizes.append("Font.Size." + obj["name"] + " = " + str(size))

	#iconografia está aqui
	def detectSvgPath(abc,frame):
		if frame["name"].lower() == "iconografia":
			for group in frame["children"]:
				if "children" in group:
					for obj in group["children"]:
						if obj["type"].lower() == "text":
							path = group["name"] + "=" + obj["name"]
							abc.svgpaths.append(path)

	#export svg files está aqui
	def detectImagens(abc,frame):
		if frame["name"].lower() == "iconografia":
			for group in frame["children"]:
				if "children" in group:
					for frame2 in group["children"]:
						if "children" in frame2:
							for obj in frame2:
								imagem = obj
								abc.imagens.append(imagem)
					

	def detectBorderWidth(abc,frame):
		if frame["name"].lower() == "border width":
			for group in frame["children"]:
				if group["type"].lower() == "group":
					for obj in group["children"]:
						if obj["type"].lower() == "rectangle":
							weight = obj["strokeWeight"]
							abc.borderWeights.append("Border.Width." + obj["name"] + " = " + str(weight) + "px" )


	def detectBorderRadius(abc,frame):
		if frame["name"].lower() == "border radius":
			for group in frame["children"]:
				if group["type"].lower() == "group":
					item = ""
					for obj in group["children"]:

						if obj["type"].lower() == "rectangle":
							if item == "":
								item = obj["name"]
							else:
								item = obj["name"] + item

						if obj["type"].lower() == "text":
							if "@" in obj["name"]:
								radius = obj["name"].replace("@","")
								item = item + " = " + str(radius)

					abc.borderRadius.append("Border.Radius." + item)


	def detectOpacity(abc,frame):
		if frame["name"].lower() == "opacity":
			for group in frame["children"]:
				if group["type"].lower() == "group":
					
					for obj in group["children"]:

						if obj["type"].lower() == "rectangle":
							if obj["name"].lower() != "rectangle":
								abc.opacitys.append("Opacity." + obj["name"] + " = " + str(obj["opacity"]))
							

	def detectLineHeight(abc,frame):
		if frame["name"].lower() == "line height":
			
			for group in frame["children"]:
				if group["type"].lower() == "group":
					item = ""
					for obj in group["children"]:

						if obj["type"].lower() == "text" and  obj["name"].lower() == "example":
							style = obj["style"]
							height = style["lineHeightPx"]
							#10 is default
							item = item + " = " + str(int(height) + 10) + "px"
						else:
							item = obj["name"] + item

					abc.lineHeights.append("Line.Height." + item)
							

	def detectShadow(abc,frame):
		if frame["name"].lower() == "camadas":
			for frame2 in frame["children"]:
				if "children" in frame2:
					for group in frame2["children"]:
						if group["type"].lower() == "group":
							if "children" in group:
								for obj in group["children"]:
									if obj["type"].lower() == "rectangle":
										for item in obj["effects"]:
											if item["type"].lower() == "drop_shadow":
												blur = str(item["radius"])
												x = str(item["offset"]["x"])
												y = str(item["offset"]["y"])
												r = item["color"]["r"]
												g = item["color"]["g"]
												b = item["color"]["b"]
												a = item["color"]["a"]

												rgba = "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(a) + ")"
												abc.shadowsAndroid.append(obj["name"] + " = " + blur.split(".")[0] + "px")
	
	#dimensões

	def detectSpacing(abc, frame):
		if frame["name"].lower() == "espaçamento":
			for component in frame ["children"]:
				token_espacamento = component["name"]
				valor_espacamento = component["absoluteBoundingBox"]["width"]
				strValor_space = str(valor_espacamento).split(".")[0]
				abc.dimensoes.append(token_espacamento + "=" + strValor_space   + "px")
				abc.spacings.append(token_espacamento + "=" + strValor_space   + "px")

		if frame["name"].lower() == "camadas":
			token_component = 0
			value_component = 0
			for component in frame["children"]:
				if component["name"].lower() == "border_width":
					if "children" in component:
						for obj in component["children"]:
							if "children" in obj:
									token_component = obj["name"]
									for element in obj["children"]:
										if element["type"].lower() == "text":
											value_component = element["name"]
									abc.dimensoes.append(str(token_component) + "=" + str(value_component))
									abc.borders.append(str(token_component) + "=" + str(value_component))

				if component["name"].lower() == "border_radius":
					if "children" in component:
						for obj in component["children"]:
							if "children" in obj:
								token_component = obj["name"]
								for element in obj["children"]:
									if element["type"].lower() == "text":
										value_component = element["name"]
								abc.dimensoes.append(str(token_component) + "=" + str(value_component))
								abc.borders.append(str(token_component) + "=" + str(value_component))

				if component["name"].lower() == "shadows":
					if "children" in component:
						for obj in component["children"]:
							if "children" in obj:
								for element in obj["children"]:
									if element["type"].lower() == "rectangle":
										width = element["absoluteBoundingBox"]["width"]
										height = element["absoluteBoundingBox"]["height"]
										token_component = element["name"]
									if element["type"].lower() == "text":
										value_component = element["name"]
							abc.shadows.append(str(token_component) + "=" + str(value_component))


	def getPalletes(abc):
		return abc.colors

	def getBorderWeights(abc):
		return abc.borderWeights

	def getBorderRadius(abc):
		return abc.borderRadius

	def getShadowAndroid(abc):
		return abc.shadowsAndroid

	def getFontFamilies(abc):
		return abc.fontFamilies

	def getFontSizes(abc):
		return abc.fontSizes

	def getOpacitys(abc):
		return abc.opacitys

	def getInsets(abc):
		return abc.insets

	def getSquishs(abc):
		return abc.squishs

	def getLineHeights(abc):
		return abc.lineHeights

	def getSpacingStacks(abc):
		return abc.spacingStacks

	def getSpacingInlines(abc):
		return abc.spacingInlines
	
	def getSvgPath(abc):
		return abc.svgpaths
	
	def getImagens(abc):
		return abc.imagens
	
	def getComponentes(abc):
		return abc.componentes

	def getDimensoes(abc):
		return abc.dimensoes
	
	def getBorders(abc):
		return abc.borders

	def getSpacings(abc):
		return abc.spacings

	def getShadows(abc):
		return abc.shadows

	def getGradientColors(abc):
		return abc.gradientColors
	
	def getButtons(abc):
		return abc.buttons

	def getCheckBoxes(abc):
		return abc.checkBoxes

	def getAutocompletes(abc):
		return abc.autocompletes

	def getRadioButtons(abc):
		return abc.radioButtons

	def getToogles(abc):
		return abc.toogles

	def getSliders(abc):
		return abc.sliders

	def getProgressBar(abc):
		return abc.progressbar
	
	def getSearch(abc):
		return abc.search
	
	def getTooltips(abc):
		return abc.tooltips
	
	def getChips(abc):
		return abc.chips
	
	def getTextArea(abc):
		return abc.textArea
	
	def getOverflowMenu(abc):
		return abc.overflowMenu

	def getNavigationBar(abc):
		return abc.navigationBar
	
	def getDatePicker(abc):
		return abc.datePicker

	def getTimePicker(abc):
		return abc.timePicker
	
	def getDropDown(abc):
		return abc.dropDown
	
	def getCards(abc):
		return abc.cards


figmaId = "SZNeL3NI0iQRX51kmwKwrp"
figmaApiKey = "26523-6cf5fee4-bb86-4800-b1da-af3c6d2d1509"

#figmaId = "5wj5BrfNeywou9FhrTaPJi"
#figmaApiKey = "25535-b73a0d4f-d374-4887-9d66-ca9f08c69dfa"

parse = ParseDS(figmaId,figmaApiKey)

print ("-------------------------------------------------------")
print ("escolha um formato de expoertação: ")
print ("1. Android")
print ("2. Web")

print ("3. Assets (SVG)")
print ("4. IOS\n\n")

escolha = input()

if(escolha == "1"):
	parse.exportToXML()
if(escolha == "2"):
	parse.exportToCSS()
if(escolha == "3"):
	parse.exportToXML()
	parse.exportToPlist()
	print("assets exportados com sucesso!")


