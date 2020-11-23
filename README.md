# audpl2dir

audpl2dir is a Python script which converts Audacious playlists to a
directory containing the tracks in the playlist.

The tracks in the destination directory can by symlinked (-s) or hard linked
from their original locations to the destination directory.

audpl2dir can also optionally (-r) generate new CLI-friendly filenames for
the files in the destination directory based on metadata in the source file. 
For example, if the playlist contains an MP3 with artist tag "Juno Reactor"
and title tag "Rotorblade (Perfect Stranger Remix)", the filename in the
destination directory will be
"juno_reactor-rotorblade-perfect_stranger_remix.mp3" if this option is
enabled.

# Usage

audpl2dir [-r] [-s] <playlist name> <destination directory>

<playlist name> is the name of the playlist as it appears in the playlist
tab in Audacious.  This script will search for the playlist in
~/.config/audacious/playlists/.

<destination directory> is where the linked files from the playlist should
appear. This directory need not already exist. Any existing files will be
overwritten.

-r renames files as described above.

-s creates symlinks instead of hard links.

# Copyright and License

Copyright (C) 2020 Steve Benson

audpl2dir was written by Steve Benson.

audpl2dir is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3, or (at your option) any later
version.

audpl2dir is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program; see the file LICENSE.  If not, see <http://www.gnu.org/licenses/>.


