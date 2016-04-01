# --------- Online TV for Kodi - official release ---------
# Copyright 2016 Pierre Severin.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# --------- Importation of Python modules ---------
# These modules are needed as they contains functions that will be used later
import sys
import os
import urlparse
import urllib
import webbrowser
import xbmcaddon
import xbmcgui
import xbmcplugin
# ---------- End of importation of Python modules ---------

#-------------- Debug tool ---------------
# !!ATTENTION : IF YOU MODIFY THE CODE OF THE PRESENT PROGRAM, IT MAY APPEARS
# THAT KODI TELLS YOU THAT IT CANNOT IMPORT THE EXTENSION. THIS CAN APPEARS
# WHEN THE ZIPPED FILE IS LOCATED IN A FOLDER IN WHICH YOU HAVE ALREADY
# IMPORTED A ZIPPED FILE IN KODI. JUST RENAME THE FOLDER AND THE ZIPPED FILE
# COULD BE ADDED. IF NOT, THIS SHOULD MEAN THAT THERE IS A BUG EITHER IN THE
# PYTHON FILE OF THE ADD-ON OR IN THE XML FILE OF THE ADD-ON !!

# In case you need to debug a modification you want to add,
# don't hesitate to use the dialog box provided in the tools of
# XBMC (old name of Kodi) : (copy-paste the 6 command lines here under
# where you need in the program, just delete the '#' signs at the beginning
# of each line and modify the text. You cannot use more than 3 lines)
#addon         = xbmcaddon.Addon('plugin.video.onlinetv')
#addonname   = addon.getAddonInfo('name')
#line1 = 'ok'
#line2 = 'ok2'
#line3 = 'ok3'
#xbmcgui.Dialog().ok(addonname, line1, line2, line3)
#-------------- End of debug tool ----------------

# ---------- Definitions of auxiliary functions -----------
# Gets the url created by Kodi for the plugin
base_url = sys.argv[0]

# Informs to the operating system that the data will be in 
# Universal Character Set Transformation Format - 8 bits
UTF8          = 'utf-8'

# Adds the plugin (synonymous of add-on) code to Kodi code (Kodi old name was XBMC)
addon         = xbmcaddon.Addon('plugin.video.onlinetv')

# Gets the real path of the plugin
home          = addon.getAddonInfo('path').decode(UTF8)

# Gets the identification number automatically provided to the plugin
addon_handle = int(sys.argv[1])

# Split the argument value number 2 if it exists, in several arguments
# with associated value.
# This argument value number 2 does not exist at the launch of the plugin 
# and it is created when the channel menu is created in a first loop.
args = urlparse.parse_qs(sys.argv[2][1:])

# Tells to Kodi (old name: XBMC) the type of content of the plugin
xbmcplugin.setContent(addon_handle, 'tvshows')

# Gets the name of the addon
addonname   = addon.getAddonInfo('name')

# Define a function that will create an additional url for each channel
# when the channel menu will be created. This url will contain arguments
# such as the Internet url that will be used later by other functions
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

# Retrieve the value of the argument named 'mode'. If this argument does not
# exist (as it is the case when the plugin is launched), returns None as
# default value.
mode = args.get('mode', None)

# Retrieve the value of the argument named 'livestreamurl'. If this argument
# does not exist (as it is the case when the plugin is launched), returns
# None as default value. The 'livestreamurl' argument will be the Internet
# url and this argument will be used by the web browser when opening Internet
live = args.get('livestreamurl', None)

# ---------- End of definitions of auxiliary functions ---------

# ---------- Creation of the list that will contains the channel info --------
# Creates a list named 'CHANNELS' that will contain all the 'Channel' objects
CHANNELS = list()

# Defines a generic 'Channel' object that will store:
# _ the opening method of the channel : method
#    By default, it is the Internet url of the channel website
# _ the name of the channel as it will appear in the menu : menulabel
# _ the name of the picture to be used as the icon of the channel
#    in the menu : iconpicture
#    If you need to change an icon, Kodi needs a picture of 256x256 pixels
#    and in .png format. Place the icon picture in the subfile 'logos' of
#    the file 'resources'
# _ the Internet url of the channel website : livestreamurl
class Channel(object):
    def __init__(self, method, menulabel, iconpicture, livestreamurl):
        self.method = method
        self.menulabel = menulabel
        self.iconpicture = iconpicture
        self.livestreamurl = livestreamurl
		# Adds the Channel object to the CHANNELS list
        CHANNELS.append(self)

# ---------- End of creation of the list ----------

#---------- Creates a Channel object for each TV channel ----------
# The TV channels are classified by spoken language. As a same TV channel
# can broadcast in several languages, a same channel can be found several
# times, one time for each language proposed.
# If you want to add or modify a TV channel in the 'Online TV' plugin,
# you are in the right section of the program !
# If you need to modify an existing channel:
# 	_ just modify the property value after the '=' sign. It must stay
#     a string, so be sure the property value is written between
#     the two '' signs. Also check that there is a comma at the end
#     of the line or a parenthesis (check with another Channel object)
# If you want to add a new channel:
#	_ copy the 4 command lines of the last Channel object
#	_ paste the copy after the command lines of the last Channel object
#	_ modify the property values: refer to the explanations of the definition
#	  the generic Channel object here above for more information
#	  on each property
# 	
# Don't forget to write '.png' at the end of the name of the icon picture !!
#
# ----- Preliminary acronym explanations -----
# Language
Channel(method = 'akamaihd.net',
        menulabel = 'Help: (ar,en,fr,...) = channel language',
		iconpicture = '00helpchannellanguage.png',
		livestreamurl = '')
	
# Other language
Channel(method = 'akamaihd.net',
        menulabel = 'Help: (de - en) = sometime in another language',
		iconpicture = '00helpchannelanotherlanguage.png',
		livestreamurl = '')
	
# Part-time broadcasting
Channel(method = 'akamaihd.net',
        menulabel = 'Help: (..) (pb) = daily part-time Internet broadcasting',
		iconpicture = '00helpparttimebroadcasting.png',
		livestreamurl = '')
	
# Geographical restricted area
Channel(method = 'akamaihd.net',
        menulabel = 'Help: (..) (ra) = sometime restricted area',
		iconpicture = '00helprestrictedarea.png',
		livestreamurl = '')
	
# ----- Arabic (ar) speaking broadcasting ------	
# Al Hurra
Channel(method = 'akamaihd.net',
        menulabel = 'Al Hurra (ar)',
		iconpicture = 'alhurra.png',
		livestreamurl = 'http://mbnhls-lh.akamaihd.net/i/MBN_1@118619/master.m3u8')
		
# i24 News arabic
Channel(method = 'akamaihd.net',
        menulabel = 'i24 News (ar) (pb)',
		iconpicture = 'i24news.png',
		livestreamurl = 'http://bcoveliveios-i.akamaihd.net/hls/live/215102/master_arabic/391/master.m3u8')

# ----- German (de) speaking broadcasting ------		
# Tagesschau
Channel(method = 'akamaihd.net',
        menulabel = 'Tagesschau (de) (pb)',
		iconpicture = 'tagesschau.png',
		livestreamurl = 'http://tagesschau-lh.akamaihd.net/i/tagesschau_1@119231/master.m3u8')
		
# ----- Danish (dk) speaking broadcasting ------
# ----- English (en) speaking broadcasting ------
# i24 News english
Channel(method = 'akamaihd.net',
        menulabel = 'i24 News (en) (pb)',
		iconpicture = 'i24news.png',
		livestreamurl = 'http://bcoveliveios-i.akamaihd.net/hls/live/215102/master_english/398/master.m3u8')
		
# Mtunes
Channel(method = 'akamaihd.net',
        menulabel = 'Mtunes (en)',
		iconpicture = 'mtunes.png',
		livestreamurl = 'http://hlshinextra-lh.akamaihd.net/i/ams4_mtunes@124572/master.m3u8')
		
# ----- Spanish (es) speaking broadcasting ------
# ----- French (fr) speaking broadcasting ------
# BFM Business
Channel(method = 'akamaihd.net',
        menulabel = 'BFM Business (fr)',
		iconpicture = 'bfmbusiness.png',
		livestreamurl = 'http://bfmlive-i.akamaihd.net/hls/live/218341/876450612001/bfmbusiness/index.m3u8')
		
# BFM TV
Channel(method = 'akamaihd.net',
        menulabel = 'BFM TV (fr)',
		iconpicture = 'bfmtv.png',
		livestreamurl = 'http://bfmlive2-i.akamaihd.net/hls/live/214427/bfmtv/index.m3u8')

# ----- Greek (gr) speaking broadcasting ------
# Alpha
Channel(method = 'akamaihd.net',
        menulabel = 'Alpha (gr)',
		iconpicture = 'alpha.png',
		livestreamurl = 'http://alfakanali-lh.akamaihd.net/i/live_1@90368/master.m3u8')

# Mega
Channel(method = 'akamaihd.net',
        menulabel = 'Mega (gr) (pb)',
		iconpicture = 'mega.png',
		livestreamurl = 'http://megahdlive1-f.akamaihd.net/i/live_1@105260/master.m3u8')
		
# Zougla
Channel(method = 'akamaihd.net',
        menulabel = 'Zougla (gr)',
		iconpicture = 'zougla.png',
		livestreamurl = 'http://zouglahd-f.akamaihd.net/i/zougla_1@56341/index_700_av-b.m3u8')
		
# ----- Italian (it) speaking broadcasting ------
# ----- Dutch (nl) speaking broadcasting ------
# ----- Persian (pe) speaking broadcasting ------
# ----- Portuguese (pt) speaking broadcasting ------
# ----- Russian (ru) speaking broadcasting ------
# ----- Turkish (tr) speaking broadcasting ------
# TRT
Channel(method = 'akamaihd.net',
        menulabel = 'TRT (tr)',
		iconpicture = 'trt.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTHD_1@182045/master.m3u8')
		
# TRT 1
Channel(method = 'akamaihd.net',
        menulabel = 'TRT 1 (tr)',
		iconpicture = 'trt1.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRT1HD_1@181842/master.m3u8')	

# TRT Arapca
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Arapca (tr)',
		iconpicture = 'trtarapca.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTARAPCA_1@181945/master.m3u8')
		
# TRT Avaz
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Avaz (tr)',
		iconpicture = 'trtavaz.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTAVAZ_1@182244/master.m3u8')	

# TRT Belgesel
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Belgesel (tr)',
		iconpicture = 'trtbelgesel.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTBELGESEL_1@182145/master.m3u8')

# TRT Cocuk
Channel(method = 'akamaihd.net',
        menulabel = "TRT Cocuk (tr)",
		iconpicture = 'trtcocuk.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTCOCUK_1@181844/master.m3u8')	
		
# TRT Diyanet
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Diyanet (tr)',
		iconpicture = 'trtdiyanet.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTDIYANET_1@182344/master.m3u8')	

# TRT Haber
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Haber (tr)',
		iconpicture = 'trthaber.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTHABERHD_1@181942/master.m3u8')

# TRT Muzik
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Muzik (tr)',
		iconpicture = 'trtmuzik.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTMUZIK_1@181845/master.m3u8')

# TRT Okul
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Okul (tr)',
		iconpicture = 'trtokul.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTOKUL_1@182245/master.m3u8')	
		
# TRT Turk
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Turk (tr)',
		iconpicture = 'trtturk.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTTURK_1@182144/master.m3u8')
		
# ----- test Channel object for debug -----
# Used to test a new channel before to formally add it in the menu with its icon.
# Pay attention to use the good 'method' value !!!
#
# test
#Channel(method = 'akamaihd.net',
 #       menulabel = 'channel title',
	#	iconpicture = 'iconname.png',
	#	livestreamurl = 'http://.../urlfromakamaind.net/.../.m3u8')
		
# ---------- End of TV channel creation ----------

# ---------- Creation of the channel menu ----------
# 'if' condition determines if the user has just clicked to launch the plugin
# (argument 'mode' does not yet exist and thus, its default value is still
# set to None) or if the user clicked on one of the channel buttons (argument
# 'mode' now exists and its value was set to 'website').
# If the 'mode' argument value is None, the software enters in the first 'if'
# condition: it creates the channel menu and the 'mode' argument to not
# create again the menu when the user clicks on another button.
if mode is None:
	# The 'for' loop is used to add all the Channel objects of the CHANNEL
	# list in the channel menu. The 'c' argument represents each
	# Channel object of the CHANNEL list during the iterations of
	# the 'for' loop
	for c in CHANNELS:
		# Gets the properties of Channel object 'c'
		menulabel_value = c.menulabel
		iconpicture_value = c.iconpicture
		livestreamurl_value = c.livestreamurl
		# Adds 'resources/logos/' before the name of the icon and translate it
		# in an url usable for Kodi (previously named 'XBMC')
		iconurl = 'resources/logos/' + iconpicture_value
		icon = xbmc.translatePath(os.path.join(home, iconurl))
		# Line 'url = ...' : adds the 'mode' argument and the 'livestreamurl' argument to
		# the 'base_url' url
		# Line 'li = ...' : Creates a item 'li' with the name of channel and with its icon
		# and adds this item to the list of the channel menu with
		# the 'mode' and 'livestreamurl' arguments
		if c.method == 'akamaihd.net':
			url = build_url({'mode': 'akamaihd.net', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			# Tells to Kodi main software that the url is a playable media file
			li.setProperty('IsPlayable', 'true')
		elif c.method == 'edgecastcdn.net':
			url = build_url({'mode': 'edgecastcdn.net', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		elif c.method == 'abcnews.com':
			url = build_url({'mode': 'abcnews.com', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		elif c.method == 'nasa.gov':
			url = build_url({'mode': 'nasa.gov', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		elif c.method == 'infomaniak.ch':
			url = build_url({'mode': 'infomaniak.ch', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		elif c.method == 'yacast.net':
			url = build_url({'mode': 'yacast.net', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		elif c.method == 'creacast.com':
			url = build_url({'mode': 'creacast.com', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on NHK channel server
		elif c.method == 'nhk.or.jp':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Streamhoster server
		elif c.method == 'streamhoster.com':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Level3 server
		elif c.method == 'level3.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Arirang channel server
		elif c.method == 'arirang.co.kr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Streamprovider server
		elif c.method == 'streamprovider.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Octoshape server
		elif c.method == 'octoshape.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Edgesuite server
		elif c.method == 'edgesuite.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Metafile Generator server
		elif c.method == 'metafilegenerator.de':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Djing channel server
		elif c.method == 'djing.com':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Rai News channel server
		elif c.method == 'rai.it':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on 105.net channels server
		elif c.method == '105.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Livestream server
		elif c.method == 'livestream.com':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Ant channel server
		elif c.method == 'ant1.gr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on 4E channel server
		elif c.method == 'tv4e.gr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Crete TV channel server
		elif c.method == 'cretetv.gr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Istoikona server
		elif c.method == 'istoikona.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Omega TV channel server
		elif c.method == 'omegatv.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Viideo server
		elif c.method == 'viiideo.gr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Astra TV channel server
		elif c.method == 'astratv.gr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Al Arabiya channel server
		elif c.method == 'alarabiya.tv':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Endavomedia server
		elif c.method == 'endavomedia.com':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Novotelecom server
		elif c.method == 'novotelecom.ru':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on SFR server
		elif c.method == 'sfr.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on LLDNS server
		elif c.method == 'lldns.net':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Canal+ channel server
		elif c.method == 'canal-plus.com':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Playmedia server
		elif c.method == 'playmedia.fr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		# Content hosted on Alsace 20 channel server
		elif c.method == 'alsace20.fr':
			url = build_url({'mode': 'm3u8', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
			li.setProperty('IsPlayable', 'true')
		else:
			url = build_url({'mode': 'website', 'livestreamurl': livestreamurl_value})
			li = xbmcgui.ListItem(menulabel_value, iconImage=icon)
		xbmcplugin.addDirectoryItem(addon_handle, url, li)
	# Close the channel menu list and creates the menu
	xbmcplugin.endOfDirectory(addon_handle)

# ---------- End of creation of the channel menu ----------
	
# ---------- Opening of the web browser with TV channel Internet url ---------	
# If the 'mode' argument value is 'website', meaning that the user is
# already in the channel menu, the default web browser is opened with the url
# link of the selected channel. The Internet url is the argument 'live'
# created in the first loop at the creation of the channel menu
elif mode[0] == 'website':

 webbrowser.open(live[0], new=1, autoraise=True)

# ---------- End of opening of the web browser ---------

# ---------- Opening of a TV channel content provided in a file format .m3u8 ---------
elif mode[0] == 'm3u8':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening of a TV channel content provided in a file format .m3u8 ---------

# ---------- Opening of a TV channel content hosted on a server from Akamai company ---------
elif mode[0] == 'akamaihd.net':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening a channel hosted by Akamai company server ---------

# ---------- Opening of a TV channel content hosted on a server from EdgeCast Networks company ---------
elif mode[0] == 'edgecastcdn.net':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening a channel hosted by EdgeCast Networks company server ---------

# ---------- Opening of a TV channel content hosted on a server from Infomaniak company ---------
elif mode[0] == 'infomaniak.ch':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening a channel hosted by Infomaniak company server ---------

# ---------- Opening of a TV channel content hosted on a server from Yacast company ---------
elif mode[0] == 'yacast.net':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening a channel hosted by Yacast company server ---------

# ---------- Opening of a TV channel content hosted on a server from Creacast company ---------
elif mode[0] == 'creacast.com':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening a channel hosted by Creacast company server ---------

# ---------- Opening of ABC News TV channel content directly hosted on ABC News server ---------
elif mode[0] == 'abcnews.com':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening ABC News TV channel content directly hosted on its server ---------

# ---------- Opening of NASA TV channel content directly hosted on NASA server ---------
elif mode[0] == 'nasa.gov':
	# Tells to Kodi (old name: XBMC) that the listitem content is an url to be opened
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=live[0]))

# --------- End of opening NASA TV channel content directly hosted on its server ---------