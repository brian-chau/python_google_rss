#!/usr/bin/python3
import os
import re
import urllib.request
from   xml.etree      import cElementTree as ET

import trafilatura    as     article

def download_url( url: str ) -> str:
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    f = urllib.request.urlopen( req )
    html = f.read( ).decode( 'utf-8' )
    return html

def disp_rss( ) -> list:
    html = download_url( 'https://news.google.com/rss' )

    root = ET.fromstring( html.replace( '\n', '' ) )
    urls = []
    for page in list( root ):
        for i, item in enumerate( page.findall( 'item' ) ):
            title = item.find( 'title' ).text
            url   = item.find( 'link' ).text
            urls.append( ( title, url ) )
            print( f'{i} {title}' )

    return urls

def disp_article( title: str, url: str ):
    os.system('cls||clear')

    print( title )
    print( '--------------------------' )
    print( )

    html = article.fetch_url( url )
    result = article.extract( html )

    # Resolve Google RSS redirect
    pattern = 'https://.*'
    match = re.search( pattern, result )
    url = match.group( 0 )
    html = article.fetch_url( url )
    result = article.extract( html )
    print( result )

if __name__ == '__main__':
    urls = disp_rss( )
    selection = int( input( '> ' ) )

    title, url = urls[ selection - 1 ]
    disp_article( title, url )
