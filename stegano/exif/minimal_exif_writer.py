"""
Offers one class, MinimalExifWriter, which takes a jpg filename
in the constructor.  Allows you to: remove exif section, add
image description, add copyright.  Typical usage:

f = MinimalExifWriter('xyz.jpg')
f.newImageDescription('This is a photo of something very interesting!')
f.newCopyright('Jose Blow, All Rights Reserved', addCopyrightYear = 1)
f.process()

Class methods:
newImageDescription(description)--will add Exif ImageDescription to file.

newCopyright(copyright, addSymbol = 0, addYear = 0)--will add Exif Copyright to file.
  Will optionally prepend copyright symbol, or copyright symbol and current year.

removeExif()--will obliterate existing exif section.

process()--call after calling one or more of the above.  Will remove existing exif
  section, optionally saving some existing tags (see below), and insert a new exif
  section with only three tags at most: description, copyright and date time original.
  If removeExif() not called, existing description (or new description if newDescription()
  called), existing copyright (or new copyright if newCopyright() called) and existing
  "DateTimeOriginal" (date/time picture taken) tags will be rewritten to the new
  minimal exif section.

Run at comand line with no args to see command line usage.

Does not work on unix due to differences in mmap.  Not sure what's up there--
don't need it on unix!

Brought to you by Megabyte Rodeo Software.
http://www.fetidcascade.com/pyexif.html
"""

# Written by Chris Stromberger, 10/2004.  Public Domain.
# Last updated: 12/3/2004.

DUMP_TIFF = 0
VERBOSE = 0
if VERBOSE:
  import binascii

import mmap
import sys
from . import minimal_exif_reader

#---------------------------------------------------------------------
class ExifFormatException(Exception):
  pass

#---------------------------------------------------------------------------
class MinimalExifWriter:
  SOI_MARKER = '\xff\xd8'
  APP0_MARKER = '\xff\xe0'
  APP1_MARKER = '\xff\xe1'

  # Standard app0 segment that will work for all files.  We hope.
  # Based on http://www.funducode.com/freec/Fileformats/format3/format3b.htm.
  APP0 = '\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'

  def __init__(self, filename):
    self.filename = filename
    self.removeExifSection = 0
    self.description = None
    self.copyright = None
    self.dateTimeOriginal = None

  #---------------------------------------------
  def newImageDescription(self, description):
    self.description = description

  #---------------------------------------------
  def newCopyright(self, copyright, addSymbol = 0, addYear = 0):
    if addYear:
      import time
      year = time.localtime()[0]
      self.copyright = "\xa9 %s %s" % (year, copyright)
    elif addSymbol:
      self.copyright = "\xa9 %s" % copyright
    else:
      self.copyright = copyright

  #---------------------------------------------
  def removeExif(self):
    self.removeExifSection = 1

  #---------------------------------------------
  def process(self):
    if not self.removeExifSection:
      self.getExistingExifInfo()

    if VERBOSE:
      print(self)

    import os
    try:
      fd = os.open(self.filename, os.O_RDWR)
    except:
      sys.stderr.write('Unable to open "%s"\n' % filename)
      return

    self.m = mmap.mmap(fd, 0)
    os.close(fd)

    # We only add app0 if all we're doing is removing the exif section.
    justRemovingExif = self.description is None and self.copyright is None and self.removeExifSection
    if VERBOSE: print('justRemovingExif=%s' % justRemovingExif)
    self.removeExifInfo(addApp0 = justRemovingExif)
    if justRemovingExif:
      self.m.close()
      return

    # Get here means we are adding new description and/or copyright.
    self.removeApp0()

    totalTagsToBeAdded = len([_f for _f in (self.description, self.copyright, self.dateTimeOriginal) if _f])
    assert(totalTagsToBeAdded > 0)

    # Layout will be: firstifd|description|copyright|exififd|datetime.
    # First ifd will have tags: desc|copyright|subifd tag.
    ifd = [self.twoBytesHexIntel(totalTagsToBeAdded)]
    ifdEnd = ['\x00\x00\x00\x00']
    NUM_TAGS_LEN = 2
    TAG_LEN = 12
    NEXT_IFD_OFFSET_LEN = 4
    TIFF_HEADER_LENGTH = 8
    ifdLength = NUM_TAGS_LEN + TAG_LEN * totalTagsToBeAdded + NEXT_IFD_OFFSET_LEN

    # Subifd only has one tag.
    SUBIFD_LENGTH = NUM_TAGS_LEN + TAG_LEN + NEXT_IFD_OFFSET_LEN

    offsetToEndOfData = ifdLength + TIFF_HEADER_LENGTH

    if self.description:
      ifd.append(self.descriptionTag(len(self.description), offsetToEndOfData))
      ifdEnd.append(self.description)
      offsetToEndOfData += len(self.description)

    if self.copyright:
      ifd.append(self.copyrightTag(len(self.copyright), offsetToEndOfData))
      ifdEnd.append(self.copyright)
      offsetToEndOfData += len(self.copyright)

    if self.dateTimeOriginal:
      ifd.append(self.subIfdTag(offsetToEndOfData))
      offsetToEndOfData += SUBIFD_LENGTH
      ifdEnd.append(self.buildSubIfd(len(self.dateTimeOriginal), offsetToEndOfData))
      ifdEnd.append(self.dateTimeOriginal)

    app1 = self.buildApp1Section(ifd, ifdEnd)

    self.addApp1(app1)

    self.m.close()

  #---------------------------------------------
  # Build exif subifd with one tag for datetime (0x9003).
  # Type is ascii (0x0002).
  def buildSubIfd(self, lenDateTime, offsetToEndOfData):
    return '\x01\x00\x03\x90\x02\x00%s%s\x00\x00\x00\x00' % (self.fourBytesHexIntel(lenDateTime), self.fourBytesHexIntel(offsetToEndOfData))

  #---------------------------------------------
  def getExistingExifInfo(self):
    # Save off the old stuff.
    try:
      f = minimal_exif_reader.MinimalExifReader(self.filename)
    except:
      # Assume no existing exif info in the file.  We
      # don't care.
      return

    if not self.description:
      self.description = f.imageDescription()

    if not self.copyright:
      self.copyright = f.copyright()

    self.dateTimeOriginal = f.dateTimeOriginal()
    if self.dateTimeOriginal:
      # Restore ending nul.
      if self.dateTimeOriginal[-1] != '\x00':
        self.dateTimeOriginal += '\x00'

  #---------------------------------------------------------------------------
  def removeExifInfo(self, addApp0 = 1):
    """Remove the app1 section of the jpg.  This removes all exif info and the exif
    thumbnail.  addApp0 should be 1 to add a minimal app0 section right after soi
    to make it a legitimate jpg, I think (various image programs can read the file
    without app0, but I think the standard requires one).
    """
    # Read first bit of file to see if exif file.
    self.m.seek(0)
    if self.m.read(2) != self.SOI_MARKER:
      self.m.close()
      raise ExifFormatException("Missing SOI marker")

    app0DataLength = 0
    appMarker = self.m.read(2)
    # See if there's an APP0 section, which sometimes appears.
    if appMarker == self.APP0_MARKER:
      if VERBOSE: print('app0 found')
      app0DataLength = ord(self.m.read(1)) * 256 + ord(self.m.read(1))
      if VERBOSE: print('app0DataLength: %s' % app0DataLength)
      # Back up 2 bytes to get the length bytes.
      self.m.seek(-2, 1)
      existingApp0 = self.m.read(app0DataLength)
      appMarker = self.m.read(2)

    if appMarker != self.APP1_MARKER:
      # We don't care, we'll add our minimal app1 later.
      return

    exifHeader = self.m.read(8)
    if VERBOSE: print('exif header: %s' % binascii.hexlify(exifHeader))
    if (exifHeader[2:6] != 'Exif' or
        exifHeader[6:8] != '\x00\x00'):
      self.m.close()
      raise ExifFormatException("Malformed APP1")

    app1Length = ord(exifHeader[0]) * 256 + ord(exifHeader[1])
    if VERBOSE: print('app1Length: %s' % app1Length)

    originalFileSize = self.m.size()

    # Shift stuff just past app1 to overwrite app1.
    # Start at app1 length bytes in + other bytes not incl in app1 length.
    src = app1Length + len(self.SOI_MARKER) + len(self.APP1_MARKER)
    if app0DataLength:
      src += app0DataLength + len(self.APP0_MARKER)
    dest = len(self.SOI_MARKER)
    if addApp0:
      if app0DataLength != 0:
        # We'll re-add the existing app0.
        dest += app0DataLength + len(self.APP0_MARKER)
      else:
        # Add our generic app0.
        dest += len(self.APP0)
    count = originalFileSize - app1Length - len(self.SOI_MARKER) - len(self.APP1_MARKER)
    if app0DataLength:
      count -= app0DataLength + len(self.APP0_MARKER)

    if VERBOSE: print('self.m.move(%s, %s, %s)' % (dest, src, count))
    self.m.move(dest, src, count)

    if addApp0:
      if app0DataLength != 0:
        self.m.resize(originalFileSize - app1Length - len(self.APP1_MARKER))
      else:
        self.m.seek(len(self.SOI_MARKER))
        self.m.write(self.APP0)
        self.m.resize(originalFileSize - app1Length - len(self.APP1_MARKER) + len(self.APP0))
    else:
      self.m.resize(originalFileSize - app1Length - len(self.APP1_MARKER))

  #---------------------------------------------------------------------------
  def removeApp0(self):
    self.m.seek(0)
    header = self.m.read(6)
    if (header[0:2] != self.SOI_MARKER or
        header[2:4] != self.APP0_MARKER):
      if VERBOSE: print('no app0 found: %s' % binascii.hexlify(header))
      return

    originalFileSize = self.m.size()

    app0Length = ord(header[4]) * 256 + ord(header[5])
    if VERBOSE: print('app0Length:', app0Length)

    # Shift stuff to overwrite app0.
    # Start at app0 length bytes in + other bytes not incl in app0 length.
    src = app0Length + len(self.SOI_MARKER) + len(self.APP0_MARKER)
    dest = len(self.SOI_MARKER)
    count = originalFileSize - app0Length - len(self.SOI_MARKER) - len(self.APP0_MARKER)
    self.m.move(dest, src, count)
    if VERBOSE: print('m.move(%s, %s, %s)' % (dest, src, count))
    self.m.resize(originalFileSize - app0Length - len(self.APP0_MARKER))

  #---------------------------------------------------------------------------
  def addApp1(self, app1):
    originalFileSize = self.m.size()

    # Insert app1 section.
    self.m.resize(originalFileSize + len(app1))
    src = len(self.SOI_MARKER)
    dest = len(app1) + len(self.SOI_MARKER)
    count = originalFileSize - len(self.SOI_MARKER)
    self.m.move(dest, src, count)
    self.m.seek(len(self.SOI_MARKER))
    self.m.write(app1)

  #---------------------------------------------------------------------------
  def fourBytesHexIntel(self, number):
    return '%s%s%s%s' % (chr(number & 0x000000ff),
                         chr((number >> 8) & 0x000000ff),
                         chr((number >> 16) & 0x000000ff),
                         chr((number >> 24) & 0x000000ff))

  #---------------------------------------------------------------------------
  def twoBytesHexIntel(self, number):
    return '%s%s' % (chr(number & 0x00ff),
                     chr((number >> 8) & 0x00ff))

  #---------------------------------------------------------------------------
  def descriptionTag(self, numChars, loc):
    return self.asciiTag('\x0e\x01', numChars, loc)

  #---------------------------------------------------------------------------
  def copyrightTag(self, numChars, loc):
    return self.asciiTag('\x98\x82', numChars, loc)

  #---------------------------------------------------------------------------
  def subIfdTag(self, loc):
    return '\x69\x87\x04\x00\x01\x00\x00\x00%s' % self.fourBytesHexIntel(loc)

  #---------------------------------------------------------------------------
  def asciiTag(self, tag, numChars, loc):
    """Create ascii tag.  Assumes description > 4 chars long."""

    return '%s\x02\x00%s%s' % (tag, self.fourBytesHexIntel(numChars), self.fourBytesHexIntel(loc))

  #---------------------------------------------------------------------------
  def buildApp1Section(self, ifdPieces, ifdEndPieces):
    """Create the APP1 section of an exif jpg.  Consists of exif header plus
    tiff header + ifd and associated data."""

    # Intel byte order, offset to first ifd will be 8.
    tiff = 'II\x2a\x00\x08\x00\x00\x00%s%s' % (''.join(ifdPieces), ''.join(ifdEndPieces))
    if DUMP_TIFF:
      f = open('tiff.dump', 'wb')
      f.write(tiff)
      f.close()
    app1Length = len(tiff) + 8
    return '\xff\xe1%s%sExif\x00\x00%s' % (chr((app1Length >> 8) & 0x00ff), chr(app1Length & 0x00ff), tiff)

  #---------------------------------------------------------------------------
  def __str__(self):
    return """filename: %(filename)s
removeExifSection: %(removeExifSection)s
description: %(description)s
copyright: %(copyright)s
dateTimeOriginal: %(dateTimeOriginal)s
""" % self.__dict__

#---------------------------------------------------------------------------
def usage(error = None):
  """Print command line usage and exit"""

  if error:
    print(error)
    print()

  print("""This program will remove exif info from an exif jpg, and can optionally
add the ImageDescription exif tag and/or the Copyright tag.  But it will always remove
some or all existing exif info (depending on options--see below)!
So don't run this on your original images without a backup.

Options:
  -h: shows this message.
  -f <file>: jpg to process (required).
  -x: remove exif info (including thumbnail).
  -d <description or file>: remove exif info (including thumbnail) and then add exif
                            ImageDescription.  Will save the existing copyright tag if present,
                            as well as the date time original tag (date & time photo taken),
                            unless -x also passed (-x always means remove all exif info).
                            It will attempt to open whatever is passed on the
                            command line as a file; if successful, the contents of the file
                            are added as the description, else the literal text on the
                            command line is used as the description.
  -c <copyright or file>: remove exif info (including thumbnail) and then add exif
                          Copyright tag.  Will save the existing image description tag if present,
                          as well as the date time original tag (date & time photo taken),
                          unless -x also passed (-x always means remove all exif info).
                          It will attempt to open whatever is passed on the command line as a file;
                          if successful, the contents of the file are added as the copyright,
                          else the literal text on the command line is used as the copyright.
  -s: prepend copyright symbol to copyright.
  -y: prepend copyright symbol and current year to copyright.

  The image description and copyright must be > 4 characters long.

  This software courtesy of Megabyte Rodeo Software.""")

  sys.exit(1)

#---------------------------------------------------------------------------
def parseArgs(args_):
  import getopt
  try:
    opts, args = getopt.getopt(args_, "yshxd:f:c:")
  except getopt.GetoptError:
    usage()

  filename           = None
  description        = ''
  copyright          = ''
  addCopyrightSymbol = 0
  addCopyrightYear   = 0
  removeExif         = 0

  for o, a in opts:
    if o == "-h":
      usage()
    if o == "-f":
      filename = a
    if o == "-d":
      try:
        f = open(a)
        description = f.read()
        f.close()
      except:
        description = a
    if o == "-c":
      try:
        f = open(a)
        copyright = f.read()
        f.close()
      except:
        copyright = a
    if o == '-x':
      removeExif = 1
    if o == '-s':
      addCopyrightSymbol = 1
    if o == '-y':
      addCopyrightYear = 1

  if filename is None:
    usage('Missing jpg filename')
  if description and (len(description) <= 4 or len(description) > 60000):
    usage('Description too short or too long')
  if copyright and (len(copyright) <= 4 or len(copyright) > 60000):
    usage('Copyright too short or too long')
  if not description and not copyright and not removeExif:
    usage('Nothing to do!')

  return filename, description, copyright, removeExif, addCopyrightSymbol, addCopyrightYear

#---------------------------------------------------------------------------
if __name__ == '__main__':
  try:
    filename, description, copyright, removeExif, addCopyrightSymbol, addCopyrightYear = parseArgs(sys.argv[1:])
    f = MinimalExifWriter(filename)
    if description:
      f.newImageDescription(description)
    if copyright:
      f.newCopyright(copyright, addCopyrightSymbol, addCopyrightYear)
    if removeExif:
      f.removeExif()

    f.process()
  except ExifFormatException as ex:
    sys.stderr.write("Exif format error: %s\n" % ex)
  except SystemExit:
    pass
  except:
    sys.stderr.write("Unable to process %s\n" % filename)
    raise
