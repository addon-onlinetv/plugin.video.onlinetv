#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2015 Pierre Severin.
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
Channel(method = 'alarabiya.tv',
        menulabel = 'Help: (ar,en,fr,...) = channel language',
		iconpicture = '00helpchannellanguage.png',
		livestreamurl = '')
	
# Other language
Channel(method = 'alarabiya.tv',
        menulabel = 'Help: (de - en) = sometime in another language',
		iconpicture = '00helpchannelanotherlanguage.png',
		livestreamurl = '')
	
# Part-time broadcasting
Channel(method = 'alarabiya.tv',
        menulabel = 'Help: (..) (pb) = daily part-time Internet broadcasting',
		iconpicture = '00helpparttimebroadcasting.png',
		livestreamurl = '')
	
# Geographical restricted area
Channel(method = 'alarabiya.tv',
        menulabel = 'Help: (..) (ra) = sometime restricted area',
		iconpicture = '00helprestrictedarea.png',
		livestreamurl = '')
	
# ----- Arabic (ar) speaking broadcasting ------	
# Al Arabiya
Channel(method = 'alarabiya.tv',
        menulabel = 'Al Arabiya (ar)',
		iconpicture = 'alarabiya.png',
		livestreamurl = 'http://livestream5.alarabiya.tv/i/live_1@141854/index_1_av-p.m3u8')
	
# Al Asr TV
Channel(method = 'livestream.com',
        menulabel = 'Al Asr TV (ar)',
		iconpicture = 'alasrtv.png',
		livestreamurl = 'http://xtvalasrx.api.channel.livestream.com/3.0/playlist.m3u8')

# Al Hadath
Channel(method = 'alarabiya.tv',
        menulabel = 'Al Hadath (ar)',
		iconpicture = 'alhadath.png',
		livestreamurl = 'http://livestream7.alarabiya.tv/i/live_1@187753/index_1_av-p.m3u8')
	
# Al Hurra
Channel(method = 'akamaihd.net',
        menulabel = 'Al Hurra (ar)',
		iconpicture = 'alhurra.png',
		livestreamurl = 'http://mbnhls-lh.akamaihd.net/i/MBN_1@118619/master.m3u8')
		
# Al Jazeera arabic
Channel(method = 'edgecastcdn.net',
        menulabel = 'Al Jazeera Arabic (ar)',
		iconpicture = 'aljazeera.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/aljazeera_ar/ls_satlink/b_,264,528,828,.m3u8')
	
# i24 News arabic
Channel(method = 'akamaihd.net',
        menulabel = 'i24 News (ar)',
		iconpicture = 'i24news.png',
		livestreamurl = 'http://bcoveliveios-i.akamaihd.net/hls/live/215102/master_arabic/391/master.m3u8')

# BBC Arabic
Channel(method = 'edgecastcdn.net',
        menulabel = 'BBC Arabic (ar)',
		iconpicture = 'bbcarabic.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/bbc_ar/ls_satlink/b_,264,528,828,.m3u8')
	
# Dubai Television
Channel(method = 'endavomedia.com',
        menulabel = 'Dubai Television (ar)',
		iconpicture = 'dubaitv.png',
		livestreamurl = 'http://cdnedvrdubaitv.endavomedia.com/smil:dmilivedubaitvhls.smil/playlist.m3u8')
		
# France 24 Arabic
Channel(method = 'yacast.net',
        menulabel = 'France 24 Arabic (ar)',
		iconpicture = 'france24arabic.png',
		livestreamurl = 'http://vipwowza.yacast.net/f24_hlslive_ar/smil:ipad.fr24ar.smil/playlist.m3u8')
		
# Funoon TV
Channel(method = 'edgecastcdn.net',
        menulabel = 'Funoon TV (ar)',
		iconpicture = 'funoontv.png',
		livestreamurl = 'http://wpc.C56B.edgecastcdn.net/hls-live/20C56B/default/ThompsanECWTV/tsecwatanfunoonmed.m3u8')
		
# RT Arabic
Channel(method = 'octoshape.net',
        menulabel = 'RT Arabic (ar)',
		iconpicture = 'rt.png',
		livestreamurl = 'http://odna.octoshape.net/f3f5m2v4/cds/smil:ch3_auto.smil/playlist.m3u8')
		
# ----- German (de) speaking broadcasting ------		
# Alex
#Channel(method = 'website',
  #      menulabel = 'Alex (de) (web)',
	#	iconpicture = 'alex.png',
	#	livestreamurl = 'http://alex-berlin.de/tv/livestream/popup.html')
	
# Arte Deutschland
Channel(method = 'lldns.net',
        menulabel = 'Arte (de)',
		iconpicture = 'arte.png',
		livestreamurl = 'http://delive.artestras.cshls.lldns.net/artestras/delive/delive.m3u8')
		
# Deutsche Welle
Channel(method = 'metafilegenerator.de',
        menulabel = 'Deutsche Welle (de)',
		iconpicture = 'deutschewelle.png',
		livestreamurl = 'http://www.metafilegenerator.de/DWelle/tv/ios/master.m3u8')
	
# Deutsche Welle Europa
Channel(method = 'metafilegenerator.de',
        menulabel = 'Deutsche Welle Europa (de - en)',
		iconpicture = 'deutschewelle.png',
		livestreamurl = 'http://www.metafilegenerator.de/DWelle/tv-europa/ios/master.m3u8')

# Deutsche Welle North America
Channel(method = 'metafilegenerator.de',
        menulabel = 'Deutsche Welle North America (de - en)',
		iconpicture = 'deutschewelle.png',
		livestreamurl = 'http://www.metafilegenerator.de/DWelle/tv-northamerica/ios/master.m3u8')		
# Nrwision
#Channel(method = 'website',
   #     menulabel = 'Nrwision (de) (web)',
	#	iconpicture = 'nrwision.png',
	#	livestreamurl = 'https://www.nrwision.de/programm/livestream.html')
		
# Servus TV
#Channel(method = 'website',
   #     menulabel = 'Servus TV (de) (web)',
	#	iconpicture = 'servustv.png',
	#	livestreamurl = 'http://www.servustv.com/at/Live')

# Tagesschau
Channel(method = 'akamaihd.net',
        menulabel = 'Tagesschau (de) (pb)',
		iconpicture = 'tagesschau.png',
		livestreamurl = 'http://tagesschau-lh.akamaihd.net/i/tagesschau_1@119231/master.m3u8')
		
# TeleBarn
Channel(method = 'infomaniak.ch',
        menulabel = 'TeleBarn (de)',
		iconpicture = 'telebarn.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/barntele/playlist.m3u8')

# TeleBielingue
Channel(method = 'infomaniak.ch',
        menulabel = 'TeleBielingue (de - fr)',
		iconpicture = 'telebielingue.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/telebielinguech/playlist.m3u8')
		
# Tirol TV
#Channel(method = 'website',
    #    menulabel = 'Tirol TV (de) (web)',
	#	iconpicture = 'tiroltv.png',
	#	livestreamurl = 'http://www.tiroltv.at/livestream-von-tiroltv/')

# TVO
Channel(method = 'infomaniak.ch',
        menulabel = 'TVO (de)',
		iconpicture = 'tvo.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/tvo/playlist.m3u8')
		
# W24
#Channel(method = 'website',
     #   menulabel = 'W24 (de) (web)',
	#	iconpicture = 'w24.png',
	#	livestreamurl = 'http://www.w24.at/TV-Live')

# WDR
Channel(method = 'metafilegenerator.de',
        menulabel = 'WDR (de) (pb)',
		iconpicture = 'wdr.png',
		livestreamurl = 'http://www.metafilegenerator.de/WDR/WDR_FS/m3u8/wdrfernsehen.m3u8')
		
# ----- Danish (dk) speaking broadcasting ------
# Lorry
#Channel(method = 'website',
   #     menulabel = 'Lorry (dk) (web)',
	#	iconpicture = 'lorry.png',
	#	livestreamurl = 'http://www.tv2lorry.dk/livestream?stream=tv2lorry')
		
# ----- English (en) speaking broadcasting ------
# A-PAC
#Channel(method = 'website',
   #     menulabel = 'Australia Public Affairs Channel (en) (web)',
	#	iconpicture = 'a-pac.png',
	#	livestreamurl = 'http://www.a-pac.tv/')

# ABC News
Channel(method = 'abcnews.com',
        menulabel = 'ABC News (en)',
		iconpicture = 'abcnews.png',
		livestreamurl = 'http://abclive.abcnews.com/i/abc_live4@136330/master.m3u8?b=500,300,700,900,1200')	

# Al Jazeera
Channel(method = 'edgecastcdn.net',
        menulabel = 'Al Jazeera (en)',
		iconpicture = 'aljazeera.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/aljazeera_en/ls_satlink/b_,264,528,828,.m3u8')#http://www.aljazeera.com/watch_now/')

# Arirang
Channel(method = 'arirang.co.kr',
        menulabel = 'Arirang (en)',
		iconpicture = 'arirang.png',
		livestreamurl = 'http://worldlive-ios.arirang.co.kr/arirang/arirangtvworldios.mp4.m3u8')
		
# BBC World
Channel(method = 'edgecastcdn.net',
        menulabel = 'BBC World (en)',
		iconpicture = 'bbcworld.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/bbc_world/ls_satlink/b_,264,528,828,.m3u8')
		
# Bloomberg Asia
Channel(method = 'edgesuite.net',
        menulabel = 'Bloomberg Asia (en)',
		iconpicture = 'bloomberg.png',
		livestreamurl = 'http://live.bltvios.com.edgesuite.net/tv/asia/master.m3u8') #http://www.bloomberg.com/live/asia')
		
# Bloomberg Europe
Channel(method = 'edgesuite.net',
        menulabel = 'Bloomberg Europe (en)',
		iconpicture = 'bloomberg.png',
		livestreamurl = 'http://live.bltvios.com.edgesuite.net/tv/eu/master.m3u8') #http://www.bloomberg.com/live/europe')

# Bloomberg U.S.
Channel(method = 'edgesuite.net',
        menulabel = 'Bloomberg U.S. (en)',
		iconpicture = 'bloomberg.png',
		livestreamurl = 'http://live.bltvios.com.edgesuite.net/tv/us/master.m3u8') #http://www.bloomberg.com/live')
		
# CBS News
Channel(method = 'akamaihd.net',
        menulabel = 'CBS News (en)',
		iconpicture = 'cbsn.png',
		livestreamurl = 'http://cbsnewshd-lh.akamaihd.net/i/CBSNDC_4@199302/index_4000_av-b.m3u8?sd=10&rebase=on')#'http://cbsn.cbsnews.com/')

# CCTV News english
Channel(method = 'streamprovider.net',
        menulabel = 'CCTV News (en)',
		iconpicture = 'cctvnewsenglish.png',
		livestreamurl = 'http://origin2.live.web.tv.streamprovider.net/streams/877ba7a57aa68fd898b838f58d51a69f/index.m3u8')
		
# CNBC
Channel(method = 'streamprovider.net',
        menulabel = 'CNBC (en)',
		iconpicture = 'cnbc.png',
		livestreamurl = 'http://origin2.live.web.tv.streamprovider.net/streams/3bc166ba3776c04e987eb242710e75c0/index.m3u8')
		
# CNN International
Channel(method = 'streamprovider.net',
        menulabel = 'CNN International (en)',
		iconpicture = 'cnninternational.png',
		livestreamurl = 'http://wpc.c1a9.edgecastcdn.net/hls-live/20C1A9/cnn/ls_satlink/b_,264,528,828,.m3u8')
	
# Deutsche Welle Arabia
Channel(method = 'metafilegenerator.de',
        menulabel = 'Deutsche Welle Arabia (en - ar)',
		iconpicture = 'deutschewelle.png',
		livestreamurl = 'http://www.metafilegenerator.de/DWelle/tv-arabia/ios/master.m3u8')
	
# Deutsche Welle Asia
Channel(method = 'metafilegenerator.de',
        menulabel = 'Deutsche Welle Asia (en)',
		iconpicture = 'deutschewelle.png',
		livestreamurl = 'http://www.metafilegenerator.de/DWelle/tv-asia/ios/master.m3u8')
		
# Djing
Channel(method = 'djing.com',
        menulabel = 'Djing (en)',
		iconpicture = 'djing.png',
		livestreamurl = 'http://cdn.djing.com/tv/live.m3u8')
		
# eNCA
Channel(method = 'edgecastcdn.net',
        menulabel = 'eNCA (en)',
		iconpicture = 'enca.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/enca/ls_satlink/b_,264,528,828,.m3u8')
		
# Euronews
Channel(method = 'edgecastcdn.net',
        menulabel = 'Euronews (en)',
		iconpicture = 'euronews.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/euronews_en/ls_satlink/b_,264,528,828,.m3u8')	
		
# Fashion TV
#Channel(method = 'website',
    #    menulabel = 'Fashion TV (en) (web)',
	#	iconpicture = 'fashiontv.png',
	#	livestreamurl = 'http://www.fashiontv.com/live')

# Fox Sport
Channel(method = 'akamaihd.net',
        menulabel = 'Fox Sport (en)',
		iconpicture = 'foxsport.png',
		livestreamurl = 'http://foxsportshdhls-lh.akamaihd.net/i/fsnewshls_0@136427/index_1096_av-p.m3u8')
		
# France 24 english
Channel(method = 'yacast.net',
        menulabel = 'France 24 (en)',
		iconpicture = 'france24english.png',
		livestreamurl = 'http://vipwowza.yacast.net/f24_hlslive_en/smil:ipad.fr24en.smil/playlist.m3u8') #'http://www.france24.com/en/')

# Fun Channel America
Channel(method = 'streamhoster.com',
        menulabel = 'Fun Channel America (en)',
		iconpicture = 'funchannelamerica.png',
		livestreamurl = 'http://fss27.streamhoster.com/lv_funchannelf1/broadcast1/playlist.m3u8')

# i24 News english
Channel(method = 'akamaihd.net',
        menulabel = 'i24 News (en)',
		iconpicture = 'i24news.png',
		livestreamurl = 'http://bcoveliveios-i.akamaihd.net/hls/live/215102/master_english/398/master.m3u8')
		
# Mtunes
Channel(method = 'akamaihd.net',
        menulabel = 'Mtunes (en)',
		iconpicture = 'mtunes.png',
		livestreamurl = 'http://hlshinextra-lh.akamaihd.net/i/ams4_mtunes@124572/master.m3u8')
		
# NASA Television
Channel(method = 'nasa.gov',
        menulabel = 'NASA Television (en)',
		iconpicture = 'nasa.png',
		livestreamurl = 'http://www.nasa.gov/multimedia/nasatv/NTV-Public-IPS.m3u8') #'http://www.nasa.gov/multimedia/nasatv/')
		
# NHK World
Channel(method = 'nhk.or.jp',
        menulabel = 'NHK World (en)',
		iconpicture = 'nhkworld.png',
		livestreamurl = 'http://plslive-w.nhk.or.jp/nhkworld/app/live.m3u8') #http://www3.nhk.or.jp/nhkworld/w/movie/')

# RT America
Channel(method = 'octoshape.net',
        menulabel = 'RT America (en)',
		iconpicture = 'rtamerica.png',
		livestreamurl = 'http://odna.octoshape.net/f3f5m2v4/cds/smil:ch4_auto.smil/playlist.m3u8')	
		
# RT Documentaries
Channel(method = 'octoshape.net',
        menulabel = 'RT Documentaries (en)',
		iconpicture = 'rtdocumentaries.png',
		livestreamurl = 'http://odna.octoshape.net/f3f5m2v4/cds/smil:ch5_auto.smil/playlist.m3u8')	

# RT UK
Channel(method = 'octoshape.net',
        menulabel = 'RT UK (en)',
		iconpicture = 'rt.png',
		livestreamurl = 'http://odna.octoshape.net/f3f5m2v4/cds/smil:ch6_auto.smil/playlist.m3u8')	
		
# Sky News
Channel(method = 'edgecastcdn.net',
        menulabel = 'Sky News (en)',
		iconpicture = 'skynews.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/skynews/ls_satlink/b_,264,528,828,.m3u8')	
		
# Vevo 1
Channel(method = 'level3.net',
        menulabel = 'Vevo 1 (en)',
		iconpicture = 'vevo.png',
		livestreamurl = 'http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch1/06/prog_index.m3u8')	

# Vevo 2
Channel(method = 'level3.net',
        menulabel = 'Vevo 2 (en)',
		iconpicture = 'vevo.png',
		livestreamurl = 'http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch2/06/prog_index.m3u8')	

# Vevo 3
Channel(method = 'level3.net',
        menulabel = 'Vevo 3 (en)',
		iconpicture = 'vevo.png',
		livestreamurl = 'http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch3/06/prog_index.m3u8')	
		
# ----- Spanish (es) speaking broadcasting ------
# Canal 24 horas
#Channel(method = 'website',
    #    menulabel = 'Canal 24 horas (es) (web)',
	#	iconpicture = 'canal24horas.png',
	#	livestreamurl = 'http://www.rtve.es/directo/canal-24h/')

# Deutsche Welle Latino America
Channel(method = 'metafilegenerator.de',
        menulabel = 'Deutsche Welle Latino America (es)',
		iconpicture = 'deutschewelle.png',
		livestreamurl = 'http://www.metafilegenerator.de/DWelle/tv-latinoamerica/ios/master.m3u8')
		
# Kiss TV
#Channel(method = 'website',
    #    menulabel = 'Kiss TV (es) (web)',
	#	iconpicture = 'kisstv.png',
	#	livestreamurl = 'http://www.kisstelevision.es/')

# La 1
#Channel(method = 'website',
   #     menulabel = 'La 1 (es) (web)',
	#	iconpicture = 'la1.png',
	#	livestreamurl = 'http://www.rtve.es/directo/la-1/')
		
# La 2
#Channel(method = 'website',
    #    menulabel = 'La 2 (es) (web)',
	#	iconpicture = 'la2.png',
	#	livestreamurl = 'http://www.rtve.es/directo/la-2/')
		
# RT Spanish
Channel(method = 'octoshape.net',
        menulabel = 'RT Spanish (es)',
		iconpicture = 'rt.png',
		livestreamurl = 'http://odna.octoshape.net/f3f5m2v4/cds/smil:ch2_auto.smil/playlist.m3u8')
		
# TeleCinco	
#Channel(method = 'website',
   #     menulabel = 'TeleCinco (es) (web)',
	#	iconpicture = 'telecinco.png',
	#	livestreamurl = 'http://www.telecinco.es/endirecto/#')

# ----- French (fr) speaking broadcasting ------
# 6ter
Channel(method = 'sfr.net',
        menulabel = '6ter (fr)',
		iconpicture = '6ter.png',
		livestreamurl = 'http://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/six_ter_hls_aes/six_ter_hls_aes_856.m3u8')

# 8 Mont Blanc
#Channel(method = 'website',
   #     menulabel = '8 Mont Blanc (fr) (web)',
	#	iconpicture = '8montblanc.png',
	#	livestreamurl = 'http://8montblanc.fr/regardez-8-mont-blanc/')

# Alsace 20
Channel(method = 'alsace20.fr',
        menulabel = 'Alsace 20 (fr)',
		iconpicture = 'alsace20.png',
		livestreamurl = 'http://live.alsace20.fr/live/alsace20/ngrp:alsace20_all/playlist.m3u8')

# Antenne Centre
Channel(method = 'akamaihd.net',
        menulabel = 'Antenne Centre (fr)',
		iconpicture = 'antennecentre.png',
		livestreamurl = 'http://vm109.imust.org:1935/live/livestream/playlist.m3u8')
		
# Arte france
Channel(method = 'lldns.net',
        menulabel = 'Arte (fr)',
		iconpicture = 'arte.png',
		livestreamurl = 'http://frlive.artestras.cshls.lldns.net/artestras/frlive/frlive.m3u8')
		
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

# Canal C
Channel(method = 'akamaihd.net',
        menulabel = 'Canal C (fr)',
		iconpicture = 'canalc.png',
		livestreamurl = 'http://streaming06.axeweb.be:1935/canalc_live/_definst_/live.stream/playlist.m3u8')
		
# Canal Zoom
Channel(method = 'akamaihd.net',
        menulabel = 'Canal Zoom (fr)',
		iconpicture = 'canalzoom.png',
		livestreamurl = 'http://streaming06.axeweb.be:1935/canalzoom_live/_definst_/live.stream/playlist.m3u8')
		
# CCTV french
#Channel(method = 'website',
 #       menulabel = 'CCTV (fr) (web)',
#		iconpicture = 'cctvfrench.png',
#		livestreamurl = 'http://fr.cntv.cn/live/index.shtml')

# Delta TV
Channel(method = 'infomaniak.ch',
        menulabel = 'Delta TV (fr)',
		iconpicture = 'deltatv.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/deltatv/playlist.m3u8')
		
# France 24 french
Channel(method = 'yacast.net',
        menulabel = 'France 24 (fr)',
		iconpicture = 'france24.png',
		livestreamurl = 'http://vipwowza.yacast.net/f24_hlslive_fr/smil:ipad.fr24fr.smil/playlist.m3u8') #'http://www.france24.com/fr/tv-en-direct-chaine-live/')

# Grand Lille TV
Channel(method = 'yacast.net',
        menulabel = 'Grand Lille TV (fr) (pb)',
		iconpicture = 'grandlilletv.png',
		livestreamurl = 'http://str81.creacast.com/grandlilletv/smil:grandlilletv.smil/playlist.m3u8')
		
# i24 News french
Channel(method = 'akamaihd.net',
        menulabel = 'i24 News (fr)',
		iconpicture = 'i24news.png',
		livestreamurl = 'http://bcoveliveios-i.akamaihd.net/hls/live/215102/master_french/412/master.m3u8')
		
# i Tele
Channel(method = 'canal-plus.com',
        menulabel = 'i Tele (fr)',
		iconpicture = 'itele.png',
		livestreamurl = 'http://hls-live-m2-l3.canal-plus.com/live/hls/itele-clair-v3-sd-andr7/and-sd-clair/index.m3u8')
		
# La Deux
Channel(method = 'infomaniak.ch',
        menulabel = 'La Deux (fr) (ra, pb)',
		iconpicture = 'ladeux.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/ladeux/playlist.m3u8')
		
# La Tele
Channel(method = 'infomaniak.ch',
        menulabel = 'La Tele (fr)',
		iconpicture = 'latele.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/latele/playlist.m3u8')
		
# La Une
Channel(method = 'infomaniak.ch',
        menulabel = 'La Une (fr) (ra, pb)',
		iconpicture = 'laune.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/laune/playlist.m3u8')
		
# M6
Channel(method = 'sfr.net',
        menulabel = 'M6 (fr)',
		iconpicture = 'm6.png',
		livestreamurl = 'http://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/m6_hls_aes/m6_hls_aes_856.m3u8')
		
# M6 Music
Channel(method = 'sfr.net',
        menulabel = 'M6 Music (fr)',
		iconpicture = 'm6music.png',
		livestreamurl = 'http://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/m6_music_hits_hls_aes/m6_music_hits_hls_aes_856.m3u8')

# MAtele		
Channel(method = 'akamaihd.net',
        menulabel = 'MAtele (fr)',
		iconpicture = 'matele.png',
		livestreamurl = 'http://streaming06.axeweb.be:1935/matele_live/_definst_/live.stream/playlist.m3u8')	
		
# Mirabelle TV
Channel(method = 'creacast.com',
        menulabel = 'Mirabelle TV (fr)',
		iconpicture = 'mirabelle.png',
		livestreamurl = 'http://str81.creacast.com/mirabelletv/smil:mirabelletv.smil/playlist.m3u8') #http://www.mirabelle.tv/')
		
# OM 5
Channel(method = 'playmedia.fr',
        menulabel = 'OM 5 (fr)',
		iconpicture = 'om5.png',
		livestreamurl = 'http://ec.playmedia.fr/om5-tv/live/playlist.m3u8')
		
# Rouge TV
Channel(method = 'infomaniak.ch',
        menulabel = 'Rouge TV (fr)',
		iconpicture = 'rougetv.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/rougetv/playlist.m3u8')	#'http://www.rougetv.ch/live')

# RTC Liege
Channel(method = 'infomaniak.ch',
        menulabel = 'RTC Liege (fr)',
		iconpicture = 'rtcliege.png',
		livestreamurl = 'http://media01.webtvlive.eu/rtc/_definst_/smil:live.smil/playlist.m3u8')

# Tele Bruxelles
Channel(method = 'akamaihd.net',
        menulabel = 'Tele Bruxelles (fr)',
		iconpicture = 'telebruxelles.png',
		livestreamurl = 'http://37.187.156.238:1935/live/live.sdp/playlist.m3u8')
		
# Tele MB
Channel(method = 'akamaihd.net',
        menulabel = 'Tele MB (fr)',
		iconpicture = 'telemb',
		livestreamurl = 'http://vm109.imust.org:1935/live/telemb-live/playlist.m3u8')
		
# Telesambre
Channel(method = 'infomaniak.ch',
        menulabel = 'Telesambre (fr)',
		iconpicture = 'telesambre.png',
		livestreamurl = 'http://vm109.imust.org:1935/live/telesambre-live/playlist.m3u8')
		
# TV5 Monde
Channel(method = 'akamaihd.net',
        menulabel = 'TV5 Monde (fr)',
		iconpicture = 'tv5monde.png',
		livestreamurl = 'http://uneapple-i.akamaihd.net/hls/live/206412/grupoune_st11@206412/st11_index.m3u8')

# TV Fil 78
Channel(method = 'infomaniak.ch',
        menulabel = 'TV Fil 78 (fr)',
		iconpicture = 'tvfil78.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/tvfil78/playlist.m3u8')

# TVM 3
Channel(method = 'infomaniak.ch',
        menulabel = 'TVM3 (fr)',
		iconpicture = 'tvm3.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/tvm3/playlist.m3u8')
		
# TV Rennes 35
Channel(method = 'infomaniak.ch',
        menulabel = 'TV Rennes 35 (fr)',
		iconpicture = 'tvrennes35.png',
		livestreamurl = 'http://streaming1.interactivplatform.fr/tvrennes35-live/_definst_/smil:tvrennes35mob.smil/playlist.m3u8')
		
# Vitamine TV
Channel(method = 'infomaniak.ch',
        menulabel = 'Vitamine TV (fr)',
		iconpicture = 'vitaminetv.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/vitatv/playlist.m3u8')
		
# Weo
Channel(method = 'creacast.com',
        menulabel = 'Weo (fr)',
		iconpicture = 'weo.png',
		livestreamurl = 'http://str81.creacast.com/weo/smil:weo.smil/playlist.m3u8')
		
# W9
Channel(method = 'sfr.net',
        menulabel = 'W9 (fr)',
		iconpicture = 'w9.png',
		livestreamurl = 'http://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/w9_hls_aes/w9_hls_aes_856.m3u8')
		
# Yvelines Premiere
Channel(method = 'infomaniak.ch',
        menulabel = 'Yvelines Premiere (fr)',
		iconpicture = 'yvelinespremiere.png',
		livestreamurl = 'http://rtmp.infomaniak.ch/livecast/yveline1/playlist.m3u8')

# ----- Greek (gr) speaking broadcasting ------
# 4E
Channel(method = 'tv4e.gr',
        menulabel = '4E (gr)',
		iconpicture = '4e.png',
		livestreamurl = 'http://mail.tv4e.gr:1935/live/myStream.sdp/playlist.m3u8')

# Acheloos TV
Channel(method = 'viiideo.gr',
        menulabel = 'Acheloos TV (gr)',
		iconpicture = 'acheloostv.png',
		livestreamurl = 'http://srv1.viiideo.gr:1935/videon/axeloostv/playlist.m3u8')
		
# Alpha
Channel(method = 'akamaihd.net',
        menulabel = 'Alpha (gr)',
		iconpicture = 'alpha.png',
		livestreamurl = 'http://alfakanali-lh.akamaihd.net/i/live_1@90368/master.m3u8')

# Ant1
Channel(method = 'ant1.gr',
        menulabel = 'Ant1 (gr)',
		iconpicture = 'ant.png',
		livestreamurl = 'http://wow.ant1.gr:1935/live/smil:mavani.smil/playlist.m3u8')

# Astra TV
Channel(method = 'astratv.gr',
        menulabel = 'Astra TV (gr)',
		iconpicture = 'astratv.png',
		livestreamurl = 'http://www.astratv.gr:8090/hls/livestream/index.m3u8')

# Best TV
Channel(method = 'istoikona.net',
        menulabel = 'Best TV (gr)',
		iconpicture = 'besttv.png',
		livestreamurl = 'http://smooth.istoikona.net/besttv.isml/manifest(format=m3u8-aapl).m3u8')
		
# Crete TV
Channel(method = 'cretetv.gr',
        menulabel = 'Crete TV (gr)',
		iconpicture = 'cretetv.png',
		livestreamurl = 'http://live.cretetv.gr:1935/cretetv/myStream/playlist.m3u8')

# Mega
Channel(method = 'akamaihd.net',
        menulabel = 'Mega (gr) (pb)',
		iconpicture = 'mega.png',
		livestreamurl = 'http://megahdlive1-f.akamaihd.net/i/live_1@105260/master.m3u8')
		
# Omega TV
Channel(method = 'omegatv.net',
        menulabel = 'Omega TV (gr)',
		iconpicture = 'omegatv.png',
		livestreamurl = 'http://stream2.omegatv.net/hls-live/livepkgr/_definst_/liveevent/omegatv.m3u8')
		
# Zougla
Channel(method = 'akamaihd.net',
        menulabel = 'Zougla (gr)',
		iconpicture = 'zougla.png',
		livestreamurl = 'http://zouglahd-f.akamaihd.net/i/zougla_1@56341/index_700_av-b.m3u8')
		
# ----- Italian (it) speaking broadcasting ------
# AGR TV
#Channel(method = 'website',
    #    menulabel = 'AGR TV (it) (web)',
	#	iconpicture = 'agrtv.png',
	#	livestreamurl = 'http://www.agrtv.it/')

# Class CNBC
#Channel(method = 'website',
   #     menulabel = 'Class CNBC (it) (web)',
	#	iconpicture = 'classcnbc.png',
	#	livestreamurl = 'http://video.milanofinanza.it/classcnbc/')
		
# Radio Monte-Carlo TV
Channel(method = '105.net',
        menulabel = 'Radio Monte-Carlo TV (it)',
		iconpicture = 'radiomontecarlotv.png',
		livestreamurl = 'http://wow01.105.net/live/rmc1/playlist.m3u8')
		
# Rai News
Channel(method = 'rai.it',
        menulabel = 'Rai News (it)',
		iconpicture = 'rainews.png',
		livestreamurl = 'http://httpstream2.rai.it/rn24.isml/Manifest(format=m3u8-aapl)') #http://www.rainews.it/dl/rainews/live/ContentItem-3156f2f2-dc70-4953-8e2f-70d7489d4ce9.html')
		
# Sky Tg 24
#Channel(method = 'website',
    #    menulabel = 'Sky Tg 24 (it) (web)',
	#	iconpicture = 'skytg24.png',
	#	livestreamurl = 'http://video.sky.it/news/diretta')
		
# Tirreno Sat
Channel(method = 'livestream.com',
        menulabel = 'Tirreno Sat (it)',
		iconpicture = 'tirrenosat.png',
		livestreamurl = 'http://xtirrenosatx.api.channel.livestream.com/3.0/playlist.m3u8')
		
# TV Moda
#Channel(method = 'website',
    #    menulabel = 'TV Moda (it) (web)',
	#	iconpicture = 'tvmoda.png',
	#	livestreamurl = 'http://video.milanofinanza.it/tvmoda/')

# Virgin Radio TV
Channel(method = '105.net',
        menulabel = 'Virgin Radio TV (it)',
		iconpicture = 'virginradiotv.png',
		livestreamurl = 'http://wow01.105.net/live/virgin1/playlist.m3u8')
		
# ----- Dutch (nl) speaking broadcasting ------
# NPO Nieuws
#Channel(method = 'website',
   #     menulabel = 'NPO Nieuws (nl) (web)',
	#	iconpicture = 'nponieuws.png',
	#	livestreamurl = 'http://www.npo.nl/live/npo-nieuws')

# ----- Persian (pe) speaking broadcasting ------
# BBC Persian
Channel(method = 'edgecastcdn.net',
        menulabel = 'BBC Persian (pe)',
		iconpicture = 'bbcpersian.png',
		livestreamurl = 'http://wpc.C1A9.edgecastcdn.net/hls-live/20C1A9/bbc_persian/ls_satlink/b_,264,528,828,.m3u8')

# IFilm
Channel(method = 'akamaihd.net',
        menulabel = 'IFilm (pe)',
		iconpicture = 'ifilm.png',
		livestreamurl = 'http://mtv.ashttp7.visionip.tv/live/mtv-ifilm-ifilm-live-16x9-SD/playlist.m3u8')	
		
# ----- Portuguese (pt) speaking broadcasting ------
# NBR
#Channel(method = 'website',
   #     menulabel = 'NBR (pt) (web)',
	#	iconpicture = 'nbr.png',
	#	livestreamurl = 'http://conteudo.ebcservicos.com.br/streaming/nbr')

# Rede Brasil
#Channel(method = 'website',
   #     menulabel = 'Rede Brasil (pt) (web)',
	#	iconpicture = 'redebrasil.png',
	#	livestreamurl = 'http://rbtv.com.br/')

# TV Brasil
#Channel(method = 'website',
   #     menulabel = 'TV Brasil (pt) (web)',
	#	iconpicture = 'tvbrasil.png',
	#	livestreamurl = 'http://tvbrasil.ebc.com.br/sites/_tvbrasil/wtv-embed.php?origem=capa-tvbrasilinternacional')

# ----- Russian (ru) speaking broadcasting ------
# 2x2
Channel(method = 'novotelecom.ru',
        menulabel = "2x2 (ru)",
		iconpicture = '2x2.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/2x2tv/tvrec/playlist.m3u8')	
		
# A-One
Channel(method = 'novotelecom.ru',
        menulabel = "A-One (ru)",
		iconpicture = 'a-one.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/aone/tvrec/playlist.m3u8')	
		
# Domashniy
Channel(method = 'novotelecom.ru',
        menulabel = "Domashniy (ru)",
		iconpicture = 'domashniy.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/domashny/tvrec/playlist.m3u8')	
		
# Dozhd
Channel(method = 'novotelecom.ru',
        menulabel = "Dozhd (ru)",
		iconpicture = 'dozhd.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/rain/tvrec/playlist.m3u8')	
		
# For Kids
Channel(method = 'novotelecom.ru',
        menulabel = "For Kids (ru)",
		iconpicture = 'forkids.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/forkids/tvrec/playlist.m3u8')	
		
# Friday
Channel(method = 'novotelecom.ru',
        menulabel = "Friday (ru)",
		iconpicture = 'friday.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/friday/tvrec/playlist.m3u8')	
		
# JV
Channel(method = 'novotelecom.ru',
        menulabel = "JV (ru)",
		iconpicture = 'jv.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/jv/tvrec/playlist.m3u8')	
		
# Karusel
Channel(method = 'novotelecom.ru',
        menulabel = "Karusel (ru)",
		iconpicture = 'karusel.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/karusel/tvrec/playlist.m3u8')	
		
# Mama
Channel(method = 'novotelecom.ru',
        menulabel = "Mama (ru)",
		iconpicture = 'mama.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/motherchi/tvrec/playlist.m3u8')	
		
# Mir 24
Channel(method = 'novotelecom.ru',
        menulabel = "Mir 24 (ru)",
		iconpicture = 'mir24.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/mir24/tvrec/playlist.m3u8')	
		
# Musicbox Russia
Channel(method = 'novotelecom.ru',
        menulabel = "Musicbox Russia (ru)",
		iconpicture = 'musicboxrussia.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/musboxru/tvrec/playlist.m3u8')	
		
# Musicbox TV
Channel(method = 'novotelecom.ru',
        menulabel = "Musicbox TV (ru)",
		iconpicture = 'musicboxtv.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/musboxtv/tvrec/playlist.m3u8')	
		
# Nickelodeon
Channel(method = 'novotelecom.ru',
        menulabel = "Nickelodeon (ru)",
		iconpicture = 'nickelodeon.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/nickelodeon/tvrec/playlist.m3u8')	
		
# NSK 49
Channel(method = 'novotelecom.ru',
        menulabel = "NSK 49 (ru)",
		iconpicture = 'nsk49.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/49kanal/tvrec/playlist.m3u8')	
		
# NST
Channel(method = 'novotelecom.ru',
        menulabel = "NST (ru)",
		iconpicture = 'nst.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/nstv/tvrec/playlist.m3u8')	
		
# NTV
Channel(method = 'novotelecom.ru',
        menulabel = "NTV (ru)",
		iconpicture = 'ntv.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/ntv/tvrec/playlist.m3u8')	
		
# Obraz (not sure at all of the channel name)
Channel(method = 'novotelecom.ru',
        menulabel = "Obraz (ru)",
		iconpicture = 'obraz.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/1_obraz/tvrec/playlist.m3u8')	
		
# OTS
Channel(method = 'novotelecom.ru',
        menulabel = "OTS (ru)",
		iconpicture = 'ots.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/ots/tvrec/playlist.m3u8')	
		
# Perec
Channel(method = 'novotelecom.ru',
        menulabel = "Perec (ru)",
		iconpicture = 'perec.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/perec/tvrec/playlist.m3u8')	
		
# Pervyi Kanal
Channel(method = 'novotelecom.ru',
        menulabel = "Pervyi Kanal (ru)",
		iconpicture = 'pervyikanal.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/1kanal/tvrec/playlist.m3u8')	
		
# Petersburg 5 Kanal
Channel(method = 'novotelecom.ru',
        menulabel = "Petersburg 5 Kanal (ru)",
		iconpicture = 'petersburg5kanal.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/5kanal/tvrec/playlist.m3u8')	
		
# RBK
Channel(method = 'novotelecom.ru',
        menulabel = "RBK (ru)",
		iconpicture = 'rbk.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/rbk/tvrec/playlist.m3u8')	
		
# Ren TV
Channel(method = 'novotelecom.ru',
        menulabel = "Ren TV (ru)",
		iconpicture = 'rentv.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/rentv/tvrec/playlist.m3u8')	
		
# Rossiya 1
Channel(method = 'novotelecom.ru',
        menulabel = "Rossiya 1 (ru)",
		iconpicture = 'rossiya1.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/rossija/tvrec/playlist.m3u8')	
		
# Rossiya 2
Channel(method = 'novotelecom.ru',
        menulabel = "Rossiya 2 (ru)",
		iconpicture = 'rossiya2.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/sport/tvrec/playlist.m3u8')	
		
# Rossiya 24
Channel(method = 'novotelecom.ru',
        menulabel = "Rossiya 24 (ru)",
		iconpicture = 'rossiya24.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/vesti/tvrec/playlist.m3u8')	
		
# Rossiya Kultura
Channel(method = 'novotelecom.ru',
        menulabel = "Rossiya Kultura (ru)",
		iconpicture = 'rossiyakultura.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/kultura/tvrec/playlist.m3u8')	
		
# Sport 1
Channel(method = 'novotelecom.ru',
        menulabel = "Sport 1 (ru)",
		iconpicture = 'sport1.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/sport1/tvrec/playlist.m3u8')	
		
# STS
Channel(method = 'novotelecom.ru',
        menulabel = "STS (ru)",
		iconpicture = 'sts.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/sts/tvrec/playlist.m3u8')	
		
# Techno 24
Channel(method = 'novotelecom.ru',
        menulabel = "Techno 24 (ru)",
		iconpicture = 'techno24.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/24techno/tvrec/playlist.m3u8')	
		
# Telekanal Futbol
Channel(method = 'novotelecom.ru',
        menulabel = "Telekanal Futbol (ru)",
		iconpicture = 'telekanalfutbol.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/futbol/tvrec/playlist.m3u8')	
		
# TV3
Channel(method = 'novotelecom.ru',
        menulabel = "TV3 (ru)",
		iconpicture = 'tv3.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/tv3/tvrec/playlist.m3u8')	
		
# TV21
Channel(method = 'novotelecom.ru',
        menulabel = "TV21 (ru)",
		iconpicture = 'tv21.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/tv21/tvrec/playlist.m3u8')	
		
# TVC
Channel(method = 'novotelecom.ru',
        menulabel = "TVC (ru)",
		iconpicture = 'tvc.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/tvc/tvrec/playlist.m3u8')	
		
# TV Zvezda
Channel(method = 'novotelecom.ru',
        menulabel = "TV Zvezda (ru)",
		iconpicture = 'tvzvezda.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/zvezda/tvrec/playlist.m3u8')	
		
# U-TV
Channel(method = 'novotelecom.ru',
        menulabel = "U-TV (ru)",
		iconpicture = 'utv.png',
		livestreamurl = 'http://hls.novotelecom.ru/streaming/utv/tvrec/playlist.m3u8')	
		
# ----- Turkish (tr) speaking broadcasting ------
# TBMM TV
Channel(method = 'akamaihd.net',
        menulabel = "TBMM TV (tr)",
		iconpicture = 'tbmmtv.png',
		livestreamurl = 'http://meclistv-lh.akamaihd.net/i/event_1@190503/master.m3u8')	
		
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

# TRT Kurdi
Channel(method = 'akamaihd.net',
        menulabel = "TRT Kurdi (tr)",
		iconpicture = 'trtkurdi.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRT6_1@181944/master.m3u8')	

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
		
# TRT Spor
Channel(method = 'akamaihd.net',
        menulabel = 'TRT Spor (tr)',
		iconpicture = 'trtspor.png',
		livestreamurl = 'http://trtcanlitv-lh.akamaihd.net/i/TRTSPOR1_1@182042/master.m3u8')
		
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
 #       menulabel = 'Test 4funtv',
	#	iconpicture = '',
	#	livestreamurl = 'http://mtv.ashttp7.visionip.tv/live/mtv-ifilm-ifilm-live-16x9-SD/playlist.m3u8')

# test 2
#Channel(method = 'akamaihd.net',
 #       menulabel = 'Test MAtele',
	#	iconpicture = '',
	#	livestreamurl = 'http://streaming06.axeweb.be:1935/matele_live/_definst_/live.stream/playlist.m3u8')	

# test 3
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test cinefil",
	#	iconpicture = '',
	#	livestreamurl = 'http://teleclub.fr/cinefil.mp4')	

# test 4
#Channel(method = 'akamaihd.net',
 #       menulabel = 'Test cinetoile',
	#	iconpicture = '',
	#	livestreamurl = 'http://teleclub.fr/cinetoile.mp4')	

# test 5
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test assemblee nationale???",
	#	iconpicture = '',
	#	livestreamurl = 'http://iwantvls-i.akamaihd.net/hls/live/202810/abscbn/master.m3u8')	
		
# test 6
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test antenne centre",
	#	iconpicture = '',
	#	livestreamurl = 'http://vm109.imust.org:1935/live/livestream/playlist.m3u8')
		
# test 7
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test tele mb",
	#	iconpicture = '',
	#	livestreamurl = 'http://vm109.imust.org:1935/live/telemb-live/playlist.m3u8')
		
# test 8
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test tele bruxelles",
	#	iconpicture = '',
	#	livestreamurl = 'http://37.187.156.238:1935/live/live.sdp/playlist.m3u8')
		
# test 9
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test canal c",
	#	iconpicture = '',
	#	livestreamurl = 'http://streaming06.axeweb.be:1935/canalc_live/_definst_/live.stream/playlist.m3u8')
		
# test 10
#Channel(method = 'akamaihd.net',
 #       menulabel = "Test canal zoom",
	#	iconpicture = '',
	#	livestreamurl = 'http://streaming06.axeweb.be:1935/canalzoom_live/_definst_/live.stream/playlist.m3u8')
		
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