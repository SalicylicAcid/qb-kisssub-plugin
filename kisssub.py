# -*- coding: utf-8 -*-
#VERSION: 1.1
#AUTHORS: GitHub Copilot
#LICENSE: MIT

import xml.etree.ElementTree as ET
import re
import html
import email.utils
try:
    from urllib.parse import quote, unquote
except ImportError:
    from urllib import quote, unquote

# import qBT modules
try:
    from novaprinter import prettyPrinter
    from helpers import retrieve_url
except ImportError:
    pass

class kisssub(object):
    """Class used by qBittorrent to search for torrents on Kisssub."""
    
    url = 'https://kisssub.org'
    name = 'Kisssub'
    supported_categories = {'all': '0'}
    
    def search(self, what, cat='all'):
        # Construct RSS URL
        # Format: https://kisssub.org/rss-<keyword1>+<keyword2>.xml
        # If empty search, use default rss.xml
        
        if not what:
            query_url = "https://kisssub.org/rss.xml"
        else:
            # Ensure "what" is properly URL encoded but not double-encoded
            # qBittorrent might pass encoded strings, or raw strings
            # Safest bet: Try to unquote then quote
            try:
                decoded_what = unquote(what)
            except:
                decoded_what = what
            
            query = quote(decoded_what)
            query_url = "https://kisssub.org/rss-{}.xml".format(query)
            
        try:
            # Download the XML data
            xml_data = retrieve_url(query_url)
            
            # Sanitize XML: Fix unescaped ampersands common in RSS feeds
            # This replaces '&' with '&amp;' unless it is already part of an entity
            if xml_data:
                xml_data = re.sub(r'&(?!(?:amp|lt|gt|quot|apos);)', '&amp;', xml_data)
            
            # Parse XML
            root = ET.fromstring(xml_data)
            
            # Navigate to items
            # RSS structure: <rss><channel><item>...
            items = root.findall('./channel/item')
            
            for item in items:
                res = {}
                
                # Title
                title_node = item.find('title')
                if title_node is not None:
                    res['name'] = html.unescape(title_node.text)
                else:
                    continue

                # Publish Date
                pub_date_node = item.find('pubDate')
                if pub_date_node is not None and pub_date_node.text:
                    try:
                        dt = email.utils.parsedate_to_datetime(pub_date_node.text)
                        res['pub_date'] = int(dt.timestamp())
                    except Exception as e:
                        # Try alternative date formats if standard parsing fails
                        date_str = pub_date_node.text.strip()
                        # Try common formats: YYYY-MM-DD HH:MM:SS, YYYY/MM/DD, etc.
                        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', 
                                   '%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y'):
                            try:
                                import datetime
                                dt = datetime.datetime.strptime(date_str, fmt)
                                res['pub_date'] = int(dt.timestamp())
                                break
                            except ValueError:
                                continue

                # Download Link (in enclosure tag)
                # <enclosure url="..." type="application/x-bittorrent" />
                enclosure = item.find('enclosure')
                if enclosure is not None:
                    # check if it is a hash link and convert to magnet
                    url = enclosure.attrib.get('url')
                    match = re.search(r'hash=([a-fA-F0-9]{40})', url)
                    if match:
                        # Add multiple trackers to increase connectivity
                        trackers = [
                            "http://open.acgtracker.com:1096/announce",
                            "udp://tracker.opentrackr.org:1337/announce",
                            "udp://open.stealth.si:80/announce"
                        ]
                        magnet = "magnet:?xt=urn:btih:" + match.group(1)
                        for tr in trackers:
                            magnet += "&tr=" + quote(tr)
                        res['link'] = magnet
                    else:
                        res['link'] = url
                else:
                    # Fallback to magnet or other link if enclosure is missing
                    # But Kisssub RSS seems to rely on enclosure for the DL link
                    continue
                
                # Description Link (Details page)
                link_node = item.find('link')
                if link_node is not None:
                    res['desc_link'] = link_node.text
                else:
                    res['desc_link'] = self.url
                
                # Size, Seeds, Leech are not available in this RSS feed
                # Setting them to default values indicating unknown
                res['size'] = "Unknown"
                res['seeds'] = "-1"
                res['leech'] = "-1"
                res['engine_url'] = self.url
                
                # Output the result
                prettyPrinter(res)
                
        except Exception:
            pass
