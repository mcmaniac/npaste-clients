#!/usr/bin/python

import optparse
import sys
import urllib3

version = "%prog 0.1"
usage = "usage: %prog [options]"

def read_data(filename):
  if filename:
    return open(filename, "r").read()
  else:
    return sys.stdin.read()

def main():

  # Get command line arguments

  parser = optparse.OptionParser(usage=usage, version=version)

  parser.add_option("-f", "--file",
                    help="read input from FILE", metavar="FILE",
                    action="store", type="string", dest="filename")

  parser.add_option("-l", "--language",
                    help="language for syntax highlighting", metavar="LANG",
                    action="store", type="string", dest="language")

  parser.add_option("-d", "--desc", "--description",
                    help="description of the paste", metavar="DESC",
                    action="store", type="string", dest="desc")

  parser.add_option("--hide", "--hidden",
                    help="hide paste (only accessible via URL)",
                    action="store_true", dest="hidden", default=False)

  opts, args = parser.parse_args()

  # Define fields to send to npaste.de

  content = read_data(opts.filename)
  lang    = opts.language if opts.language else opts.filename
  hidden  = opts.hidden
  desc    = opts.desc

  fields = {
      "lang": lang,
      "desc": desc,
      "hidden": hidden,
      "content": content,
      }

  # Open connection and upload data

  conn = urllib3.connection_from_url("https://npaste.de")

  r = conn.request("POST", "/", fields=fields, redirect=False)

  print r.data

if __name__ == "__main__":
  main()
