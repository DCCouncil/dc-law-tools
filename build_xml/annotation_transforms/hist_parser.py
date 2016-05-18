"""
DCLaw - remove Optional; manually fix;
remove dc73Edition; manually fix;
"""

from arpeggio import ParserPython, Optional, ZeroOrMore, OneOrMore, EOF
from arpeggio import RegExMatch as _

###########
##
## PRIMITIVES
##
###########

def ident():	return _(r'\w+(?:[\w.–-]*\w)?')
def numId():	return _(r'\d\w*(?:[\w.–-]*\w)?')
def num():		return _(r'\d+')
def oDot():		return Optional('.')
def oComma():	return Optional(',')
def cot():		return ['.', ','] # comma or dot... geddit?
def oCot():		return ZeroOrMore(cot)
def dash():		return ['-', '–']
def oDash():	return Optional(dash)
def SS():		return ['§§', '§']
def EOL():		return _(r'$')

###########
##
## DATE
##
###########

def month():	return _(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*')	# Month abreviations: Jan. Feb. Mar. Apr. May June July Aug. Sep. Oct. Nov. Dec.
def day():		return _(r'[123]?\d')												# Date format: MMMM DD, YYYY,
def year():		return _(r'(?:12|13|14|15|16|17|18|19|20)\d\d')
def date():		return (month, oCot, day, oCot, year, oCot)

###########
##
## section
##
###########

def subSec():		return ('(', ident, ZeroOrMore((',', ident)), ')')
def subSecErr():	return ('[', subSec, ']')
def subSecRng():	return ([dash, 'to'], subSec)
def subSecs():		return (ZeroOrMore(subSec), Optional(subSecRng), Optional(subSecErr))
def secErr():		return ('[', ident, ']')
def rawSec():		return (ident, Optional(secErr), subSecs)
def singleSec():	return (SS, rawSec)
def section():		return (SS, rawSec, Optional([',', 'and', 'to', dash]), ZeroOrMore(([rawSec, subSecs], ',',)))

###########
##
## intraCite - a generalized citation into a document 
##
###########

def inChapter():		return (['chap', 'ch', 'c.'], oDot, ident)
def inSubChapter():		return ('subch', oCot, ident)
def inTitle():			return ('title', oDot, ident)
def inArt():			return ('art', oDot, ident)
def inPara():			return ('par', Optional('a'), oDot, ident, Optional(subSec))
def inPage():			return ('p', oCot, numId)
def inDiv():			return ('div', oDot, ident)
def inAppendix():		return ('appendix', ident)
def supraSection():		return ZeroOrMore(([inChapter, inSubChapter, inTitle, inArt, inDiv, inPage, inAppendix], oCot, oCot))

def singleIntraCite():	return (supraSection, Optional(singleSec), oComma, Optional(inPara))
def intraCite():		return OneOrMore((supraSection, Optional(section), oComma, Optional(inPara)))

###########
##
## FEDERAL
##
###########

def stat():			return (numId, _(r'Stat'), oDot, numId, oCot, ZeroOrMore(numId, ','), Optional(('[', num, ']')), intraCite)

def pubLawToken():	return _(r'pub[\w.]* l[\w.]* (no\.?)?')
def privLawToken():	return _(r'priv[\w.]* l[\w.]* (no\.?)?')
def law():			return ([pubLawToken, privLawToken], num, oDash, num, oComma, intraCite)

def hr():			return ('h', oDot, 'r', oDot, numId, intraCite)

def ex_ord():		return (['exec', 'ex'], oDot, ['order', 'ord'], oDot, 'no', oDot, numId, oComma, intraCite, oCot, Optional(date))

def resolution():	return (Optional('Joint'), 'Res', oCot, 'No', oCot, numId, intraCite)

def register():		return (num, 'F', oCot, 'R', oCot, num, oCot, Optional(intraCite))
def fedCite():		return [stat, law, hr, ex_ord, resolution, register]

###########
##
## DC
##
###########
def formerly():			return ('formerly', singleSec)
def dcToken():			return ('d', oCot, 'c', oCot)		# D.C.
def usToken():			return ('u', oCot, 's', oCot)		# U.S.
def dcLawToken():		return (dcToken, ['laws', 'law'], oCot, Optional(SS)) # D.C. Law 
def dcLaw():			return (dcLawToken, num, dash, numId, oComma, intraCite, Optional(formerly))	# D.C. Law XX-XXX, §[§] SS, [SS], S(P), (P)
# D.C. Law XX-XXX, § 5(a) - (c),
# D.C. Law XX-XXX, § 5(a)(1), (2),


def dcRegister():		return (num, ['dcr', 'drc'], oCot, numId)
# XX DCR XXXXX

def dcRevStat():		return ('r', oCot, 's', oCot, oComma, Optional([usToken, dcToken]), oComma, section)

def dcReorgToken():		return 'reorg. plan no.'
# Reorg. Plan No. X of YYYY,
def dcReorgYearFirst():	return (year, dcReorgToken, ident)
def dcReorgYearLast():	return (dcReorgToken, ident, oComma, Optional('of'), Optional('('), year, Optional(')'))

def dcReorg():			return ([dcReorgYearFirst, dcReorgYearLast], oComma, intraCite)
def corpLaws():			return (intraCite, 'Corp. Laws of Wash.', oCot, num, 'th council', intraCite)
def dcLegAssem():		return (Optional(numId), 'leg', oCot, 'assem', oCot, oCot, Optional(date), Optional(('p.', ident)), oCot, intraCite)

def dcCite():			return [dcLaw, dcRegister, dcRevStat, dcReorg, dcLegAssem, corpLaws]

###########
##
## ancient
##
###########
def kilty():		return (['Kilty’s', 'kilty'], ['rept', 'rep'], oCot, oCot, Optional(('p', oCot)), ident)
# Kilty's Rept. p. XXX
def alex():			return ('Alex.', ['brit', 'Br'], oCot, 'Stat', oCot, oCot, Optional(('p', oCot)), ident, Optional((oCot, 'ident')))
# Alex. Brit. Stat. p. XXX
def geo():			return (numId, 'Geo', oCot, ident, oCot, singleIntraCite, oCot, year)
# XX Geo. XXX § 5, YYYY
def compStat():		return ('Comp.', 'Stat.', oCot, dcToken, oCot, Optional('p'), oCot, ident, intraCite)
def ann():			return (numId, ['anne', 'ann'], oCot, singleIntraCite, oCot, year)
def edward():		return (numId, 'Edw', oCot, numId, oCot, singleIntraCite, year)
def hen():			return (numId, 'Hen.', numId, oCot, singleIntraCite, year)
def ancientCite():	return [kilty, alex, geo, compStat, ann, edward, hen]

###########
##
## leading keywords - keywords that appear before the date
##
###########

# as added
def added():		return ('as added', Optional('by'))
# manually fix and replace
def repealed():		return ('repealed', Optional(['pursuant to', 'by'], intraCite, 'of'))
# enacted
def enacted():		return 'enacted'

def renumbered():	return ('renumbered', Optional('as'), Optional(intraCite), Optional('and amended'))
def restored():		return ('restored', Optional('as'), section)
def designated():	return ('designated', Optional('as'), intraCite)
def redesignated():	return ('re', designated)
def ruleAmend():	return ('amended by rule', oCot)
def amended():		return (Optional('and'), 'amended')

def keywords():		return ZeroOrMore(([added, repealed, enacted, renumbered,restored, designated, redesignated, ruleAmend, amended], oComma))

###########
##
## ROOT
##
###########


def cite():			return ([fedCite, dcCite, ancientCite], Optional(')'), oComma)
def partialCite():	return (date, intraCite)
def citeString():	return (keywords, [(Optional(date), OneOrMore(cite)), partialCite], oComma, EOF)

parser = ParserPython(citeString, ignore_case=True)




