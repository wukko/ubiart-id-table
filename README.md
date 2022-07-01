# ubiart-id-table
UbiArt idtable.idt file generator that lets you add new bundles to UbiArt games that use IDTable as way to verify file download completion. More often used for modding Just Dance 2017 on PC.

## Why?
`idtable.idt` file contains a list of bundle path hashes. UbiArt games that let you play before download is complete use this file to check file download status. If IDTable file is missing and/or corrupted, there's no way for game to verify consistency of downloaded files and the game will see bundles as "not yet finished downloading". This script lets you overwrite official IDTable to let the game load unofficial bundles.

## Supported games
- Just Dance 2017 PC
- Probably Just Dance 2015 - 2022 on PS4 and Xbox One
- ...maybe some other UbiArt games that let you play before download is done

## How to use it
This script doesn't depend on any external modules. All you need is Python 3+.

1. Download `generateIDTable.py`
2. Copy downloaded file to desired game directory
3. Run it by opening command prompt or terminal in directory and running `py generateIDTable.py`
4. Good job, you have successfully bypassed the annoying bundle limitation!

You can also use this script as a module (like I usually do).

## Customization
You can change default values in the `generateIDTable.py` file to match your modded game.

## Credits
UbiArt CRC32 Python implementation by [InvoxiPlayGames](https://gist.github.com/InvoxiPlayGames/4320e6781fa8d17baedd22f6e6ff779c).
