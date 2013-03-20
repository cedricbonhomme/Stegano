"""
This module offers one class, MinimalExifReader.  Pass jpg filename
to the constructor.  Will read minimal exif info from the file.  Three
"public" functions available:
imageDescription()--returns Exif ImageDescription tag (0x010e) contents,
                    or '' if not found.
copyright()--returns Exif copyright tag (0x8298) contents, or '' if not
             found.
dateTimeOriginal()--returns Exif DateTimeOriginal tag (0x9003) contents,
                    or '' if not found.  If found, the trailing nul char
                    is stripped.  This function also takes an optional
                    format string to apply time.strftime-style formatting
                    to the date time.

Brought to you by Megabyte Rodeo Software.
"""

# Written by Chris Stromberger, 10/2004.  Public Domain.
# Much is owed to Thierry Bousch's exifdump.py:
# http://topo.math.u-psud.fr/~bousch/exifdump.py

#---------------------------------------------------------------------
class ExifFormatException(Exception):
  pass

#---------------------------------------------------------------------
class MinimalExifReader:
  IMAGE_DESCRIPTION_TAG = 0x010e
  COPYRIGHT_TAG = 0x8298
  EXIF_SUBIFD_TAG = 0x8769
  DATE_TIME_ORIGINAL_TAG = 0x9003

  #---------------------------------------
  def __init__(self, filename):
    """Pass in jpg exif file name to process.  Will attempt to find tags
    of interest."""

    self.tagsToFind = {self.IMAGE_DESCRIPTION_TAG:'',
                       self.COPYRIGHT_TAG:'',
                       self.DATE_TIME_ORIGINAL_TAG:''}

    # Read first bit of file to see if exif file.
    f = open(filename, 'rb')
    firstTwoBytes = f.read(2)
    if firstTwoBytes != '\xff\xd8':
      f.close()
      raise ExifFormatException("Missing SOI marker")

    appMarker = f.read(2)
    # See if there's an APP0 section, which sometimes appears.
    if appMarker == '\xff\xe0':
      #print "Skipping app0"
      # Yes, we have app0.  Skip over it.
      app0DataLength = ord(f.read(1)) * 256 + ord(f.read(1))
      app0 = f.read(app0DataLength - 2)
      appMarker = f.read(2)

    if appMarker != '\xff\xe1':
      raise ExifFormatException("Can't find APP1 marker")

    exifHeader = f.read(8)
    #import binascii
    #print binascii.hexlify(exifHeader)
    if (exifHeader[2:6] != 'Exif' or
        exifHeader[6:8] != '\x00\x00'):
      f.close()
      raise ExifFormatException("Malformed APP1")

    app1DataLength = ord(exifHeader[0]) * 256 + ord(exifHeader[1])
    #print app1DataLength

    # Read exif info starting at the beginning of the self.tiff section.
    # This is 8 bytes into the app1 section, so subtract 8 from
    # app1 length.
    self.tiff = f.read(app1DataLength - 8)
    f.close()

    self.endian = self.tiff[0]
    if self.endian not in ('I', 'M'):
      raise ExifFormatException("Invalid endianess found: %s" % self.endian)

    # Now navigate to the items of interest and get them.
    ifdStart = self.getValueAtLocation(4, 4)
    self.ifdSearch(ifdStart)

  #---------------------------------------
  def imageDescription(self):
    """Return image description tag contents or '' if not found."""

    return self.tagsToFind[self.IMAGE_DESCRIPTION_TAG].strip('\x20\x00')

  #---------------------------------------
  def copyright(self):
    """Return copyright tag contents or '' if not found."""

    return self.tagsToFind[self.COPYRIGHT_TAG].strip('\x20\x00')

  #---------------------------------------
  def dateTimeOriginal(self, formatString = None):
    """Pass in optional format string to get time.strftime style formatting,
    else get default exif format for date time string (without trailing nul).
    Returns '' if tag not found."""

    # The datetime should end in nul, get rid of it.
    if formatString is None or not self.tagsToFind[self.DATE_TIME_ORIGINAL_TAG]:
      return self.tagsToFind[self.DATE_TIME_ORIGINAL_TAG].strip('\x20\x00')
    else:
      # This will only work if the datetime string is in the standard exif format (i.e., hasn't been altered).
      try:
        import time
        return time.strftime(formatString, time.strptime(self.tagsToFind[self.DATE_TIME_ORIGINAL_TAG].strip('\x20\x00'), '%Y:%m:%d %H:%M:%S'))
      except:
        return self.tagsToFind[self.DATE_TIME_ORIGINAL_TAG].strip('\x20\x00')


  #---------------------------------------
  def ifdSearch(self, ifdStart):
    numIfdEntries = self.getValueAtLocation(ifdStart, 2)
    tagsStart = ifdStart + 2
    for entryNum in range(numIfdEntries):
      # For my purposes, all files will have either no tags, or
      # only our tags of interest, so no need to waste time trying to
      # break out of the loop early.
      thisTagStart = tagsStart + 12 * entryNum
      tagId = self.getValueAtLocation(thisTagStart, 2)
      if tagId == self.EXIF_SUBIFD_TAG:
        # This is a special tag that points to another ifd.  Our
        # date time original tag is in the sub ifd.
        self.ifdSearch(self.getTagValue(thisTagStart))
      elif tagId in self.tagsToFind:
        assert(not self.tagsToFind[tagId])
        self.tagsToFind[tagId] = self.getTagValue(thisTagStart)

  #---------------------------------------
  def getValueAtLocation(self, offset, length):
    slice = self.tiff[offset:offset + length]
    if self.endian == 'I':
      val = self.s2n_intel(slice)
    else:
      val = self.s2n_motorola(slice)
    return val

  #---------------------------------------
  def s2n_motorola(self, str):
    x = 0
    for c in str:
      x = (x << 8) | ord(c)
    return x

  #---------------------------------------
  def s2n_intel(self, str):
    x = 0
    y = 0
    for c in str:
      x = x | (ord(c) << y)
      y = y + 8
    return x

  #---------------------------------------
  def getTagValue(self, thisTagStart):
    datatype = self.getValueAtLocation(thisTagStart + 2, 2)
    numBytes = [ 1, 1, 2, 4, 8, 1, 1, 2, 4, 8 ] [datatype-1] * self.getValueAtLocation(thisTagStart + 4, 4)
    if numBytes > 4:
      offsetToValue = self.getValueAtLocation(thisTagStart + 8, 4)
      return self.tiff[offsetToValue:offsetToValue + numBytes]
    else:
      if datatype == 2 or datatype == 1 or datatype == 7:
        return self.tiff[thisTagStart + 8:thisTagStart + 8 + numBytes]
      else:
        return self.getValueAtLocation(thisTagStart + 8, numBytes)

  #---------------------------------------
  def __str__(self):
    return str(self.tagsToFind)

#---------------------------------------------------------------------
if __name__ == '__main__':
  import sys
  if len(sys.argv) == 1:
    print("Pass jpgs to process.")
    sys.exit(1)


  for filename in sys.argv[1:]:
    try:
      f = MinimalExifReader(filename)
      print(filename)
      print("description: '%s'" % f.imageDescription())
      print("copyright: '%s'" % f.copyright())
      print("dateTimeOriginal: '%s'" % f.dateTimeOriginal())
      print("dateTimeOriginal: '%s'" % f.dateTimeOriginal('%B %d, %Y %I:%M:%S %p'))
      print()
    except ExifFormatException as ex:
      sys.stderr.write("Exif format error: %s\n" % ex)
    except:
      sys.stderr.write("Unable to process %s\n" % filename)

