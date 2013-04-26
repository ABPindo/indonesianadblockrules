#!C:\Python33 python.exe
""" FOP
    Filter Orderer and Preener
    Copyright (C) 2011 Michael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>."""
# FOP version number
VERSION = 3.4

# Import the key modules
import collections, filecmp, os, re, subprocess, sys

# Check the version of Python for language compatibility and subprocess.check_output()
MAJORREQUIRED = 3
MINORREQUIRED = 1
if sys.version_info < (MAJORREQUIRED, MINORREQUIRED):
    raise RuntimeError("FOP requires Python {reqmajor}.{reqminor} or greater, but Python {ismajor}.{isminor} is being used to run this program.".format(reqmajor = MAJORREQUIRED, reqminor = MINORREQUIRED, ismajor = sys.version_info.major, isminor = sys.version_info.minor))

# Import a module only available in Python 3
from urllib.parse import urlparse

# Compile regular expressions to match important filter parts (derived from Wladimir Palant's Adblock Plus source code)
DOMAINPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)#\@?#")
ELEMENTPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)(#\@?#)([^{}]+)$")
OPTIONPATTERN = re.compile(r"^(.*)\$(~?[\w\-]+(?:=[^,\s]+)?(?:,~?[\w\-]+(?:=[^,\s]+)?)*)$")

# Compile regular expressions that match element tags and pseudo classes; "@" indicates either the beginning or the end of a selector
SELECTORPATTERN = re.compile(r"(?<=[\s\[@])([a-zA-Z]*[A-Z][a-zA-Z]*)((?=([\[\]\^\*\$=:@]))|(?=(\s([+>]|[a-zA-Z]+[\[:@]))))")
PSEUDOPATTERN = re.compile(r"(\:[a-zA-Z\-]*[A-Z][a-zA-Z\-]*)(?=([\(\:\@\s]))")
REMOVALPATTERN = re.compile(r"((?<=(@))|(?<=([>+]\s)))([a-zA-Z]+)(?=([#\.]))")

# Compile a regular expression that describes a completely blank line
BLANKPATTERN = re.compile(r"^\s*$")

# Compile a regular expression that validates commit comments
COMMITPATTERN = re.compile(r"^(A|M|P)\:\s(\((.+)\)\s)?(.*)$")

# List the files that should not be sorted, either because they have a special sorting system or because they are not filter files
IGNORE = ("CC-BY-SA.txt", "easytest.txt", "GPL.txt", "MPL.txt")

# List all Adblock Plus options (excepting domain, which is handled separately), as of version 1.3.9
KNOWNOPTIONS =  ("collapse", "document", "donottrack", "elemhide",
                "font", "image", "match-case", "object",
                "object-subrequest", "other", "popup", "script",
                "stylesheet", "subdocument", "third-party", "xmlhttprequest")

# List the supported revision control system commands
REPODEF = collections.namedtuple("repodef", "name, directory, locationoption, repodirectoryoption, checkchanges, difference, commit, pull, push")
GIT = REPODEF(["git"], "./.git/", "--work-tree=", "--git-dir=", ["status", "-s", "--untracked-files=no"], ["diff"], ["commit", "-m"], ["pull"], ["push"])
HG = REPODEF(["hg"], "./.hg/", "-R", None, ["stat", "-q"], ["diff"], ["commit", "-m"], ["pull"], ["push"])
REPOTYPES = (GIT, HG)

def start ():
    """ Print a greeting message and run FOP in the directories
    specified via the command line, or the current working directory if
    no arguments have been passed."""
    greeting = "FOP (Filter Orderer and Preener) version {version}".format(version = VERSION)
    characters = len(str(greeting))
    print("=" * characters)
    print(greeting)
    print("=" * characters)

    # Convert the directory names to absolute references and visit each unique location
    places = sys.argv[1:]
    if places:
        places = [os.path.abspath(place) for place in places]
        for place in sorted(set(places)):
            main(place)
            print()
    else:
        main(os.getcwd())

def main (location):
    """ Find and sort all the files in a given directory, committing
    changes to a repository if one exists."""
    # Check that the directory exists, otherwise return
    if not os.path.isdir(location):
        print("{location} does not exist or is not a folder.".format(location = location))
        return

    # Set the repository type based on hidden directories
    repository = None
    for repotype in REPOTYPES:
        if os.path.isdir(os.path.join(location, repotype.directory)):
            repository = repotype
            break
    # If this is a repository, record the initial changes; if this fails, give up trying to use the repository
    if repository:
        try:
            basecommand = repository.name
            if repository.locationoption.endswith("="):
                basecommand.append("{locationoption}{location}".format(locationoption = repository.locationoption, location = location))
            else:
                basecommand.extend([repository.locationoption, location])
            if repository.repodirectoryoption:
                if repository.repodirectoryoption.endswith("="):
                    basecommand.append("{repodirectoryoption}{location}".format(repodirectoryoption = repository.repodirectoryoption, location = os.path.normpath(os.path.join(location, repository.directory))))
                else:
                    basecommand.extend([repository.repodirectoryoption, location])
            command = basecommand + repository.checkchanges
            originaldifference = True if subprocess.check_output(command) else False
        except(subprocess.CalledProcessError, OSError):
            print("The command \"{command}\" was unable to run; FOP will therefore not attempt to use the repository tools. On Windows, this may be an indication that you do not have sufficient privileges to run FOP - the exact reason why is unknown. Please also ensure that your revision control system is installed correctly and understood by FOP.".format(command = " ".join(command)))
            repository = None

    # Work through the directory and any subdirectories, ignoring hidden directories
    print("\nPrimary location: {folder}".format(folder = os.path.join(os.path.abspath(location), "")))
    for path, directories, files in os.walk(location):
        print("Current directory: {folder}".format(folder = os.path.join(os.path.abspath(path), "")))
        for direct in directories:
            if direct.startswith("."):
                directories.remove(direct)
        directories.sort()
        for filename in sorted(files):
            address = os.path.join(path, filename)
            extension = os.path.splitext(filename)[1]
            # Sort all text files that are not blacklisted
            if extension == ".txt" and filename not in IGNORE:
                fopsort(address)
            # Delete unnecessary backups and temporary files
            if extension == ".orig" or extension == ".temp":
                try:
                    os.remove(address)
                except(IOError, OSError):
                    # Ignore errors resulting from deleting files, as they likely indicate that the file has already been deleted
                    pass

    # If in a repository, offer to commit any changes
    if repository:
        commit(repository, basecommand, originaldifference)

def fopsort (filename):
    """ Sort the sections of the file and save any modifications."""
    temporaryfile = "{filename}.temp".format(filename = filename)
    CHECKLINES = 10
    section = []
    lineschecked = 1
    filterlines = globalelementlines = nonglobalelementlines = 0

    # Read in the input and output files concurrently to allow filters to be saved as soon as they are finished with
    with open(filename, "r", encoding = "utf-8", newline = "\n") as inputfile, open(temporaryfile, "w", encoding = "utf-8", newline = "\n") as outputfile:

        # Writes the filter lines to the file
        def writefilters():
            if globalelementlines > (filterlines + nonglobalelementlines):
                outputfile.write("{filters}\n".format(filters = "\n".join(sorted(set(section), key = lambda rule: re.sub(DOMAINPATTERN, "", rule)))))
            elif filterlines > nonglobalelementlines:
                outputfile.write("{filters}\n".format(filters = "\n".join(sorted(set(section), key = str.lower))))
            else:
                outputfile.write("{filters}\n".format(filters = "\n".join(sorted(set(section)))))

        for line in inputfile:
            line = line.strip()
            if not re.match(BLANKPATTERN, line):
                # Include comments verbatim and, if applicable, sort the preceding section of filters and save them in the new version of the file
                if line[0] == "!" or line[:8] == "%include" or line[0] == "[" and line[-1] == "]":
                    if section:
                        writefilters()
                        section = []
                        lineschecked = 1
                        filterlines = globalelementlines = nonglobalelementlines = 0
                    outputfile.write("{line}\n".format(line = line))
                else:
                    # Neaten up filters and, if necessary, check their type for the sorting algorithm
                    elementparts = re.match(ELEMENTPATTERN, line)
                    if elementparts:
                        domains = elementparts.group(1).lower()
                        if lineschecked <= CHECKLINES:
                            if isglobalelement(domains) or elementparts.group(2) == "#@#":
                                globalelementlines += 1
                            else:
                                nonglobalelementlines += 1
                            lineschecked += 1
                        line = elementtidy(domains, elementparts.group(2), elementparts.group(3))
                    else:
                        if lineschecked <= CHECKLINES:
                            filterlines += 1
                            lineschecked += 1
                        line = filtertidy(line)
                    # Add the filter to the section
                    section.append(line)
        # At the end of the file, sort and save any remaining filters
        if section:
            writefilters()

    # Replace the existing file with the new one only if alterations have been made
    if not filecmp.cmp(temporaryfile, filename):
        # Check the operating system and, if it is Windows, delete the old file to avoid an exception (it is not possible to rename files to names already in use on this operating system)
        if os.name == "nt":
            os.remove(filename)
        os.rename(temporaryfile, filename)
        print("Sorted: {filename}".format(filename = os.path.abspath(filename)))
    else:
        os.remove(temporaryfile)

def filtertidy (filterin):
    """ Sort the options of blocking filters and make the filter text
    lower case if applicable."""
    optionsplit = re.match(OPTIONPATTERN, filterin)

    if not optionsplit:
        # Remove unnecessary asterisks from filters without any options and return them
        return removeunnecessarywildcards(filterin)
    else:
        # If applicable, separate and sort the filter options in addition to the filter text
        filtertext = removeunnecessarywildcards(optionsplit.group(1))
        optionlist = optionsplit.group(2).lower().replace("_", "-").split(",")

        domainlist = []
        removeentries = []
        for option in optionlist:
            # Detect and separate domain options
            if option[0:7] == "domain=":
                domainlist.extend(option[7:].split("|"))
                removeentries.append(option)
            elif option.strip("~") not in KNOWNOPTIONS:
                print("Warning: The option \"{option}\" used on the filter \"{problemfilter}\" is not recognised by FOP".format(option = option, problemfilter = filterin))
        # Sort all options other than domain alphabetically
        # For identical options, the inverse always follows the non-inverse option ($image,~image instead of $~image,image)
        optionlist = sorted(set(filter(lambda option: option not in removeentries, optionlist)), key = lambda option: (option[1:] + "~") if option[0] == "~" else option)
        # If applicable, sort domain restrictions and append them to the list of options
        if domainlist:
            optionlist.append("domain={domainlist}".format(domainlist = "|".join(sorted(set(domainlist), key = lambda domain: domain.strip("~")))))

        # Return the full filter
        return "{filtertext}${options}".format(filtertext = filtertext, options = ",".join(optionlist))

def elementtidy (domains, separator, selector):
    """ Sort the domains of element hiding rules, remove unnecessary
    tags and make the relevant sections of the rule lower case."""
    # Order domain names alphabetically, ignoring exceptions
    if "," in domains:
        domains = ",".join(sorted(set(domains.split(",")), key = lambda domain: domain.strip("~")))
    # Mark the beginning and end of the selector with "@"
    selector = "@{selector}@".format(selector = selector)
    each = re.finditer
    # Remove unnecessary tags
    for untag in each(REMOVALPATTERN, selector):
        bc = untag.group(2)
        if bc == None:
            bc = untag.group(3)
        untagname = untag.group(4)
        ac = untag.group(5)
        selector = selector.replace("{before}{untag}{after}".format(before = bc, untag = untagname, after = ac), "{before}{after}".format(before = bc, after = ac), 1)
    # Make the remaining tags lower case wherever possible
    for tag in each(SELECTORPATTERN, selector):
        tagname = tag.group(1)
        ac = tag.group(3)
        if ac == None:
            ac = tag.group(4)
        selector = selector.replace("{tag}{after}".format(tag = tagname, after = ac), "{tag}{after}".format(tag = tagname.lower(), after = ac), 1)
    # Make pseudo classes lower case where possible
    for pseudo in each(PSEUDOPATTERN, selector):
        pseudoclass = pseudo.group(1)
        ac = pseudo.group(3)
        selector = selector.replace("{pclass}{after}".format(pclass = pseudoclass, after = ac), "{pclass}{after}".format(pclass = pseudoclass.lower(), after = ac), 1)
    # Remove the markers from the beginning and end of the selector and return the complete rule
    return "{domain}{separator}{selector}".format(domain = domains, separator = separator, selector = selector[1:-1])

def commit (repository, basecommand, userchanges):
    """ Commit changes to a repository using the commands provided."""
    difference = subprocess.check_output(basecommand + repository.difference)
    if not difference:
        print("\nNo changes have been recorded by the repository.")
        return
    print("\nThe following changes have been recorded by the repository:")
    print(difference.decode("utf-8"))
    try:
        # Persistently request a suitable comment
        while True:
            comment = input("Please enter a valid commit comment or quit:\n")
            if checkcomment(comment, userchanges):
                break
    # Allow users to abort the commit process if they do not approve of the changes
    except (KeyboardInterrupt, SystemExit):
        print("\nCommit aborted.")
        return

    print("Comment \"{comment}\" accepted.".format(comment = comment))
    try:
        # Commit the changes
        command = basecommand + repository.commit + [comment]
        subprocess.Popen(command).communicate()
        print("\nConnecting to server. Please enter your password if required.")
        # Update the server repository as required by the revision control system
        for command in repository[7:]:
            command = basecommand + command
            subprocess.Popen(command).communicate()
            print()
    except(subprocess.CalledProcessError):
        print("Unexpected error with the command \"{command}\".".format(command = command))
        raise subprocess.CalledProcessError("Aborting FOP.")
    except(OSError):
        print("Unexpected error with the command \"{command}\".".format(command = command))
        raise OSError("Aborting FOP.")
    print("Completed commit process successfully.")

def isglobalelement (domains):
    """ Check whether all domains are negations."""
    for domain in domains.split(","):
        if domain and not domain.startswith("~"):
            return False
    return True

def removeunnecessarywildcards (filtertext):
    """ Where possible, remove unnecessary wildcards from the beginnings
    and ends of blocking filters."""
    whitelist = False
    if filtertext[0:1] == "@@":
        whitelist = True
        filtertext = filtertext[2:]
    while True:
        if filtertext[0] != "*":
            break
        else:
            proposed = filtertext[1:]
            if not proposed or proposed[0] == "|":
                break
            else:
                filtertext = proposed
    while True:
        if filtertext[-1] != "*":
            break
        else:
            proposed = filtertext[:-1]
            if not proposed or proposed[-1] == "|" or proposed[0] == "/" and proposed[-1] == "/":
                break
            else:
                filtertext = proposed
    if whitelist:
        filtertext = "@@{filtertext}".format(filtertext = filtertext)
    return filtertext

def checkcomment(comment, changed):
    """ Check the commit comment and return True if the comment is
    acceptable and False if it is not."""
    sections = re.match(COMMITPATTERN, comment)
    if sections == None:
        print("The comment \"{comment}\" is not in the recognised format.".format(comment = comment))
    else:
        indicator = sections.group(1)
        if indicator == "M":
            # Allow modification comments to have practically any format
            return True
        elif indicator == "A" or indicator == "P":
            if not changed:
                print("You have indicated that you have added or removed a rule, but no changes were initially noted by the repository.")
            else:
                address = sections.group(4)
                if not validurl(address):
                    print("Unrecognised address \"{address}\".".format(address = address))
                else:
                    # The user has changed the subscription and has written a suitable comment message with a valid address
                    return True
    print()
    return False

def validurl (url):
    """ Check that an address has a scheme (e.g. http), a domain name
    (e.g. example.com) and a path (e.g. /), or relates to the internal
    about system."""
    addresspart = urlparse(url)
    if addresspart.scheme and addresspart.netloc and addresspart.path:
        return True
    elif addresspart.scheme == "about":
        return True
    else:
        return False

if __name__ == '__main__':
    start()
