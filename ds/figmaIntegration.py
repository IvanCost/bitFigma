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

		#android
		dimensoes = parse.getDimensoes()
		for dimens in dimensoes:
			arr = dimens.split("=")
			className = arr[0].strip().replace(".","-").replace("-", "_").lower()
			f.write("<dimen name = " + "\"" + className +"\"" + ">" + arr[1] + "</dimen>"";\n")
		
		#web
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

		f.write("</resources>")
		f.close()
		g.close()
		h.close()
	

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
	

		#whatever
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
		f.write("<resources> \n\n")
		for componente in componentesList:

			#escrevendo XML de styles
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

			#escrevendo XML de cada componente
			path = "drawable"
			try:
				if not os.path.exists(path):
					os.mkdir(path)
			except OSError:
				print ("Creation of the directory %s failed" % path)
			else:
				print ("Successfully created the directory %s " % path)

			token_componente = arr[0].split("=")[1].replace(" / ", "_").replace(" ", "").lower() + ".xml"
			g = open(os.path.join(path, token_componente),"w+")
			g.write("<?xml version=" + "\"" + "1.0" +"\"" + " encoding="  + "\"" + "utf-8" +"\"" "?>\n\n")
			g.write("<shape xmlns:android=" + "\""+ "http://schemas.android.com/apk/res/android" + "\""+ ">" + "\n\n")
			g.write("<solid\n")
			g.write("android:color=" + "\"" + arr[1].split("=")[1] + "\"" + ">" +"\n")
			g.write("</solid>\n\n")
			g.write("<stroke\n")
			g.write("android:width=" + "\"" + "1dp" + "\"" + "\n")
			g.write("android:color=" + "\"" + arr[8].split("=")[1] + "\"" + ">" +"\n")
			g.write("</stroke>\n")
			g.write("<corners\n")
			g.write("android:radius=" + "\"" + arr[4].split("=")[1].split(".")[0] + "dp"  + "\"" + ">" +"\n")
			g.write("</corners>\n")
			g.write("</shape>")
			g.close()

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
		objFontFamily = "Roboto"
		objFontSize = "12"
		corDaFonte = "#0000"
		colorStroke = "#00212429"
		colorFill = "#00212429"
		if frame["name"].lower() == "componentes":
			
			for component in frame["children"]:
				if "children" in component:
					child = component["children"]
					
					for obj in child:

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
					for group2 in group["children"]:

						if "children" in group2:

							for group3 in group2["children"]:

								if "children" in group3:

									for group4 in group3["children"]:

										if "children" in group4:
									
											for color in group4["children"]:

												if color["type"].lower() == "rectangle":
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
		if frame["name"].lower() == "shadow":
			for group in frame["children"]:
				if group["type"].lower() == "group":
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
									abc.shadows.append("Shadow." + obj["name"] + " =  Blur: " + blur + ", x: " + x + ", y: " + y + ", color: " + str(rgba))
	
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
									if element["type"].lower() == "text":
										valores = element["name"]
									token_component = component["name"]
									abc.shadows.append(str(token_component) + "=" + str(value_component))


	def getPalletes(abc):
		return abc.colors

	def getBorderWeights(abc):
		return abc.borderWeights

	def getBorderRadius(abc):
		return abc.borderRadius

	def getShadow(abc):
		return abc.shadows

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


