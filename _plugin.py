from modules.base.pluginbase import PluginBase
from modules.base.configbase import ConfigBase
from misc.configproperty import ConfigProperty
from misc.logs import Logs
from modules.pidmanager import PIDManager
from modules.convertmanager import ConvertManager
import subprocess


class Plugin(PluginBase):
    name = "Cartoon"
    author = "MikeGawi"
    description = "Photo cartoon-like style preprocessing"
    site = "https://github.com/MikeGawi/Cartoon_ePiframe"
    info = "Based on a great work of http://www.fmwconcepts.com/imagemagick"

    # ImageMagick convert code template
    __CONVERT_CODE = "{} {} -resize {}x{} ( -clone 0 -colorspace HCL -separate +channel ) ( -clone 3 ) ( -clone 1 -clone 2 -clone 4 -set colorspace HCL -combine -colorspace sRGB -define modulate:colorspace=hcl ) -delete 1-4 ( -clone 0 -set colorspace RGB -colorspace gray ) ( -clone 2 -unsharp 0x{} ) ( -clone 2 -clone 3 +swap -compose minus -composite -evaluate multiply {} -negate ) -delete 0,2,3 -compose multiply -composite {}"

    class PluginConfigManager(ConfigBase):
        # building settings according to config.default file
        def load_settings(self):
            self.SETTINGS = [
                ConfigProperty(
                    "is_enabled", self, prop_type=ConfigProperty.BOOLEAN_TYPE
                ),
                ConfigProperty(
                    "edges_width",
                    self,
                    dependency="is_enabled",
                    minvalue=1,
                    prop_type=ConfigProperty.INTEGER_TYPE,
                ),
                ConfigProperty(
                    "edges_strength",
                    self,
                    dependency="is_enabled",
                    minvalue=1,
                    prop_type=ConfigProperty.INTEGER_TYPE,
                ),
            ]

    def __init__(
        self,
        path: str,
        pid_manager: PIDManager,
        logging: Logs,
        global_config: ConfigBase,
    ):
        super().__init__(
            path, pid_manager, logging, global_config
        )  # default constructor

    @staticmethod
    def __subproc(arguments):
        # method to start process with arguments.
        # it needs a list of arguments
        argument = arguments.split()
        process = subprocess.Popen(argument, stdout=subprocess.PIPE)
        process.wait()
        out, error = process.communicate()
        return out, error

    def preprocess_photo(
        self,
        original_photo: str,
        is_horizontal: bool,
        convert_manager: ConvertManager,
        photo,
        id_label: str,
        creation_label: str,
        source_label: str,
    ):
        # formatting the conversion code
        # notice that image will be converted to target display size as this will speed up the processing
        code = self.__CONVERT_CODE.format(
            self.global_config.get("convert_bin_path"),
            original_photo,
            self.global_config.getint("image_width"),
            self.global_config.getint("image_height"),
            self.config.get("edges_width"),
            self.config.get("edges_strength"),
            original_photo,
        )
        out, error = self.__subproc(code)
        if error:
            raise Exception(error)  # raise if error
