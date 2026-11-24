<img align="right" src="https://github.com/MikeGawi/cartoon_ePiframe/blob/master/assets/cart.gif" width="400">

# Cartoon_ePiframe

Photo cartoon-like style preprocessing plugin for [ePiframe](https://github.com/MikeGawi/ePiframe)

This plugin has been created with [ePiframe_plugin](https://github.com/MikeGawi/ePiframe_plugin) template.

Based on a great work of [Fred's ImageMagick Scripts](http://www.fmwconcepts.com/imagemagick)

## Requirements

* [ePiframe](https://github.com/MikeGawi/ePiframe) 2.0 or newer (Plugin API v2). For ePiframe 1.x use the version
  of this plugin from before ePiframe 2.0.

## How it works

* The effect is made with ImageMagick on the photo scaled down to the display size; on a Raspberry Pi Zero it takes a few seconds per photo.
* Settings: `edges_width` (how much the edges are enhanced) and `edges_strength`.

## Installation

On working ePiframe:

* Clone to ePiframe plugins path:
	```
	cd <ePiframe path>/plugins
	git clone https://github.com/MikeGawi/cartoon_ePiframe cartoon_ePiframe
	```

OR

* Download and extract:
	```
	cd <ePiframe path>/plugins
	wget -q https://github.com/MikeGawi/cartoon_ePiframe/archive/master.zip -O cartoon_ePiframe.zip
	unzip cartoon_ePiframe.zip
	mv cartoon_ePiframe-master cartoon_ePiframe
	rm cartoon_ePiframe.zip
	```

## Configuration

* Configure with the file [*config.cfg*](https://github.com/MikeGawi/cartoon_ePiframe/blob/master/config.cfg) inside *ePiframe_path/plugins/cartoon_ePiframe*

OR

* In ePiframe WebUI (if enabled) under *Plugins - Cartoon*

Check the configuration with `./ePiframe.py --check-config` (in the ePiframe folder).

The plugin folder name must stay a valid Python name (letters, digits, `_`), e.g. `cartoon_ePiframe`: ePiframe
skips plugins in folders with dashes or dots.
