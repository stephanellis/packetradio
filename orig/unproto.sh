    #!/bin/bash
    #
    #   This is a quickie wrapper around 'beacon' to
    #   send UI/unproto mode packets in linux for use
    #   in unproto mode 'nets' or just general CQ type
    #   chatting on packet radio.
    #
    #   If you run this with another window (maybe in a
    #   split 'screen' session) with axlisten, it's a 
    #   reasonably graceful solution.
    #
    #   I hope someone finds this useful
    #
    #  73 de KC2RGW  29 Oct 2011
    
    clear
    echo
    echo "Unproto mode beaconing"
    echo
    echo "   Fill in the information as requested"
    echo
    echo -n "What port should I use? > "
    read PORT
    echo -n "What digi? (blank for none) > "
    read DIGI
    echo -n "What destination callsign? > "
    read DEST

    if [ "$DIGI"a = "a" ] ; then
            DESTINATION="$DEST"
    else
            DESTINATION="$DEST $DIGI"
    fi

    clear

    while [ 0 ] ; do
         if [ "$DIGI"a = "a" ] ; then
                 echo -n "text to "$DEST"> "
         else
                 echo -n "text to "$DEST" via "$DIGI"> "
         fi
         read TEXT
    
         beacon -d "$DESTINATION" -s "$PORT" "$TEXT"
    done
