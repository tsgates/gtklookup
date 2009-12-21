#! /usr/bin/env python

"""
Taesoo Kim (tsgatesv@gmail.com)

gtklookup is to lookup entries from gtk reference documentation, especially
within emacs. (http://www.gtk.org/documentation.html)

Have a fun!
"""

import pickle

from urllib        import urlopen
from os.path       import join, dirname, exists

debug = False

def fetch_page( db, root, cat ) :
    from BeautifulSoup import BeautifulSoup

    pairs = [ ( "ix01.html", "index" ),
              ( "api-index-full.html", "index" ),
              ( "index-all.html", "index" ) ]

    for ( index, div ) in pairs :
        try :
            main = BeautifulSoup( urlopen( join( root, index )  ) )
            body = main.findAll( "div", attrs={ "class" : div } )[0]
            links = body.findAll( "a" )
            break
        
        except :
            if debug :
                print "Skipped! (%s,%s)" % ( index, div )

    for link in links :
        try :
            url = link[ "href" ].strip()
        except :
            continue

        try :
            desc = link.string
            desc = desc.replace( "()", "" )
            desc = desc.replace( " ", "" ).strip()
        except :
            if debug :
                print "No link in document :", url
            continue

        url = join( root, url.strip() )
        
        db.append( ( desc.encode( "ascii", "ignore" ), 
                     url.encode( "ascii", "ignore" ),
                     cat.encode( "ascii", "ignore" ) ) )

        if debug :
            print "%-40s(%s):%s" % ( desc, cat, url )

def update_db( dbname ) :
    # clean up
    db = []
    
    # ref. http://www.gtk.org/documentation.html
    urls = { "GLib"      : "http://library.gnome.org/devel/glib/stable/",
             "GObject"   : "http://library.gnome.org/devel/gobject/stable/",
             "GIO"       : "http://library.gnome.org/devel/gio/stable/",
             "Pango"     : "http://library.gnome.org/devel/pango/stable/",
             "ATK"       : "http://library.gnome.org/devel/atk/stable/",
             "GdkPixbuf" : "http://library.gnome.org/devel/gdk-pixbuf/stable/",
             "GDK"       : "http://library.gnome.org/devel/gdk/stable/",
             "GTK"       : "http://library.gnome.org/devel/gtk/stable/" }

    root = urls[ "GLib" ]

    for (cat, url) in urls.iteritems() :
        print "Fetching %-10s : %s" % ( cat, url )
        
        fetch_page( db, url, cat )

    # sort db
    db.sort()
    
    # update database
    pickle.dump( db, open( dbname, "w" ) )

if __name__ == "__main__" :
    import optparse
    
    parser = optparse.OptionParser( __doc__.strip() )
    
    parser.add_option( "-d", "--db"       , dest="db", default="gtklookup.db" )
    parser.add_option( "-b", "--debug"    , action="store_true", dest="debug", default=False )
    parser.add_option( "-l", "--lookup"   , dest="key" )
    parser.add_option( "-u", "--update"   , action="store_true", dest="update", default=False )
    parser.add_option( "-a", "--all"      , action="store_true", default=False, dest="all")
    parser.add_option( "-c", "--cache"    , action="store_true", default=False, dest="cache")

    ( opts, args ) = parser.parse_args()

    debug = opts.debug
    
    # create db
    try:
        if exists( opts.db ) :
            db = pickle.load( open( opts.db ) )
        else :
            db = []
    except :
        db = []

    # update
    if opts.update :
        update_db( opts.db )
        exit
        
    # cache
    if opts.cache :
        print "\n".join( [ item[0] for item in db ] )
        exit
        
    # complete
    if opts.all :
        print "\n".join( [ "\t".join( item ) for item in db ] )
        exit
        
    # lookup
    if opts.key :
        
        results = []
        
        for item in db :
            if any( [ subitem.find( opts.key ) != -1 for subitem in item ] ) :
                results.append( item )
        
        results.sort()

        print "\n".join( [ "\t".join( item ) for item in results ] )
        exit

                    
