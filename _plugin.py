from modules.base.pluginbase import pluginbase
from modules.base.configbase import configbase
from misc.configprop import configprop
from misc.constants import constants
import sys, os, subprocess

class plugin(pluginbase):
	
	name = 'Cartoon'
	author = 'MikeGawi'
	description = 'Photo cartoon-like style preprocessing'
	site = 'https://github.com/MikeGawi/Cartoon-ePiframe'
	info = 'Based on a great work of http://www.fmwconcepts.com/imagemagick'
	
	#ImageMagick convert code template
	__CONVERT_CODE = '{} {} -resize {}x{} ( -clone 0 -colorspace HCL -separate +channel ) ( -clone 3 ) ( -clone 1 -clone 2 -clone 4 -set colorspace HCL -combine -colorspace sRGB -define modulate:colorspace=hcl ) -delete 1-4 ( -clone 0 -set colorspace RGB -colorspace gray ) ( -clone 2 -unsharp 0x{} ) ( -clone 2 -clone 3 +swap -compose minus -composite -evaluate multiply {} -negate ) -delete 0,2,3 -compose multiply -composite {}'	
	
	class configmgr (configbase):
		#building settings according to config.default file
		def load_settings(self):
			self.SETTINGS = [
				configprop('is_enabled', self, prop_type=configprop.BOOLEAN_TYPE),
				configprop('edges_width', self, dependency='is_enabled', minvalue=1, prop_type=configprop.INTEGER_TYPE),
				configprop('edges_strength', self, dependency='is_enabled', minvalue=1, prop_type=configprop.INTEGER_TYPE),
			]
	
	def __init__ (self, path, pidmgr, logging, globalconfig):
		super().__init__(path, pidmgr, logging, globalconfig) #default constructor
	
	def __subproc (self, arg):
		#method to start process with arguments. 
		#it needs a list of arguments
		args = arg.split()
		process = subprocess.Popen(args, stdout=subprocess.PIPE)
		process.wait()
		out, err = process.communicate()
		return out, err 
	
	def preprocess_photo (self, orgphoto, is_horizontal, convertmgr):
		#formatting the conversion code
		#notice that image will be converted to target display size as this will speed up the processing 
		code = self.__CONVERT_CODE.format(self.globalconfig.get('convert_bin_path'), orgphoto, self.globalconfig.getint('image_width'), self.globalconfig.getint('image_height'), self.config.get('edges_width'), self.config.get('edges_strength'), orgphoto)
		out, err = self.__subproc(code)
		if err:	raise Exception(err) #raise if error