"""Cartoon_ePiframe: cartoon-like style of the photo (ePiframe Plugin API v2).

The photo is processed by ImageMagick before ePiframe converts it for the
display (``preprocess_photo``). Based on the cartoon script of Fred's ImageMagick
Scripts: http://www.fmwconcepts.com/imagemagick
"""

from pathlib import Path

from epiframe.config.property import ConfigProperty, PropertyType
from epiframe.plugins.base import PhotoFile
from epiframe.plugins.base import Plugin as PluginBase


def cartoon_arguments(
    photo: Path, width: int, height: int, edges_width: int, edges_strength: int
) -> list[str]:
    """ImageMagick ``convert`` arguments turning ``photo`` into a cartoon in place.

    The photo is scaled down to the display size first: the effect is slow on a
    Raspberry Pi and the display can't show more detail anyway.
    """
    return [
        str(photo),
        "-resize",
        f"{width}x{height}",
        # posterized colors: lightness channel separated in HCL
        "(", "-clone", "0", "-colorspace", "HCL", "-separate", "+channel", ")",
        "(", "-clone", "3", ")",
        "(", "-clone", "1", "-clone", "2", "-clone", "4",
        "-set", "colorspace", "HCL", "-combine", "-colorspace", "sRGB",
        "-define", "modulate:colorspace=hcl", ")",
        "-delete", "1-4",
        # edges: difference of the gray image and its sharpened copy
        "(", "-clone", "0", "-set", "colorspace", "RGB", "-colorspace", "gray", ")",
        "(", "-clone", "2", "-unsharp", f"0x{edges_width}", ")",
        "(", "-clone", "2", "-clone", "3", "+swap", "-compose", "minus",
        "-composite", "-evaluate", "multiply", str(edges_strength), "-negate", ")",
        "-delete", "0,2,3",
        "-compose", "multiply", "-composite",
        str(photo),
    ]  # fmt: skip


class Plugin(PluginBase):
    name = "Cartoon"
    author = "MikeGawi"
    description = "Photo cartoon-like style preprocessing"
    site = "https://github.com/MikeGawi/cartoon_ePiframe"
    info = "Based on a great work of http://www.fmwconcepts.com/imagemagick"

    def settings(self) -> list[ConfigProperty]:
        # the entries of config.cfg / default/config.default with their validation
        return [
            *super().settings(),  # is_enabled
            ConfigProperty(
                "edges_width",
                PropertyType.INTEGER,
                dependency="is_enabled",
                min_value=1,
            ),
            ConfigProperty(
                "edges_strength",
                PropertyType.INTEGER,
                dependency="is_enabled",
                min_value=1,
            ),
        ]

    def preprocess_photo(self, photo: PhotoFile) -> None:
        # photo.image_magick raises ImageMagickError (with ImageMagick's message)
        # when the conversion fails; ePiframe logs it
        photo.image_magick.run(
            cartoon_arguments(
                photo.path,
                photo.width,
                photo.height,
                self.config.getint("edges_width"),
                self.config.getint("edges_strength"),
            )
        )
