# Torrent Metadata File

- <b>info</b>: a dictionary that describes the file(s) of the torrent. There are two possible forms: one for the case of a 'single-file' torrent with no directory structure, and one for the case of a 'multi-file' torrent (see below for details)

- <b>announce</b>: The announce URL of the tracker (string)

- <b>announce-list</b>: (optional) this is an extention to the official specification, offering backwards-compatibility. (list of lists of strings).
The official request for a specification change is here.

- <b>creation date</b>: (optional) the creation time of the torrent, in standard UNIX epoch format (integer, seconds since 1-Jan-1970 00:00:00 UTC)

- <b>comment</b>: (optional) free-form textual comments of the author (string)

- <b>created by</b>: (optional) name and version of the program used to create the 
.torrent (string)

- <b>encoding</b>: (optional) the string encoding format used to generate the pieces part of the info dictionary in the .torrent metafile (string)