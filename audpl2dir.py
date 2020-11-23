#!/usr/bin/env python

import posix
import sys
import os
import urllib


def strToFilename(s):
    #print s
    rv = ''
    s=s.lower()
    for c in s:
        #print repr(c),c.isalpha()
        if ord(c) in range(128):
            if c.isalpha():
                rv += c
            elif c.isdigit():
                rv += c
            elif c==' ':
                if len(rv)==0 or rv[-1]!='_':
                    rv += '_'
            elif c=='&':
                rv += 'and'
            elif c=='(':
                if len(rv)>0 and rv[-1]=='_':
                    rv = rv[:-1]
                if s.find(c) != 0:
                    rv += '-' 
        elif ord(c)==239:
            rv += 'i'
        else:
            # drop the character
            pass
    return rv

def tagToFilename(path):
    try:
        import eyeD3
        tag = eyeD3.Tag()
        tag.link(path)
        artist = strToFilename(tag.getArtist())
        title = strToFilename(tag.getTitle())
        if artist=='' or title=='':
            return None
        newfn = '%s-%s.mp3' % (artist,title)    
        return newfn
    except Exception, e:
        print 'error reading tag for %s: %s' % (path, e)

def getTagArtist(path):
    import eyeD3
    tag = eyeD3.Tag()
    tag.link(path)
    return tag.getArtist()

def getTagTitle(path):
    import eyeD3
    tag = eyeD3.Tag()
    tag.link(path)
    return tag.getTitle()

def getPlaylistTitle(path):
    for line in open(path):
        if line.startswith('title='):
            line=line.strip('\n')
            line = line[len('title='):]
            return urllib.unquote(line)

def findPlaylist(pldir,title):
    for fn in os.listdir(pldir):
        if not fn.endswith('.audpl'):
            continue
        thisTitle = getPlaylistTitle(os.path.join(pldir,fn))
        if thisTitle==title:
            return fn

def getFilesInPlaylistFile(path):
    files = []
    for line in open(path):
        line = line.strip('\n')
        if line.startswith('uri='):
            line = line[len('uri='):]
            if line.startswith('file://'):
                line = line[len('file://'):]
            files.append(urllib.unquote(line))
    return files

def main():
    if len(sys.argv)<3:
        print 'usage: %s <playlist name> <output directory>' % sys.argv[0]
        return
        
    plName = sys.argv[1]
    destDir = sys.argv[2]
    destRename = '-r' in sys.argv
    sym = '-s' in sys.argv

    plDir = os.path.join(os.getenv('HOME'),'.config/audacious/playlists')

    if not os.path.exists(destDir):
        print 'creating destination directory %s' % repr(destDir)
        os.makedirs(destDir)
    else:
        print 'destination directory %s already exists' % repr(destDir)
    
    plPath = findPlaylist(plDir,plName)
    if plPath:
        print 'found playlist named %s at %s' % (repr(plName),repr(plPath))
        for srcPath in getFilesInPlaylistFile(os.path.join(plDir,plPath)):
            srcFilename = os.path.split(srcPath)[-1]
            
            if destRename:
                destFilename = tagToFilename(srcPath)
                if not destFilename:
                    destFilename=srcFilename
            else:
                destFilename = srcFilename
            
            destPath = os.path.join(destDir,destFilename)
            
            print ' < %s' % repr(srcPath)
            print ' > %s' % repr(destPath)
            if os.path.exists(destPath):
                os.unlink(destPath)

            if sym:
                posix.symlink(srcPath,destPath)
            else:
                posix.link(srcPath,destPath)

            print ''
    else:
        print 'unable to find any playlist with name %s in %s' % (repr(plName),repr(plDir))

if __name__ == '__main__':
    main()

    