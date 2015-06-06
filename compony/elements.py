from functools import partial
from compony.core import create_element


def generate_element_function(tag_name, self_closing=False, multiline=True):
    """
    (tag_name: str, self_closing: bool, multiline: bool) -> Callable
    """
    return partial(create_element, tag_name, self_closing, multiline)

e = generate_element_function


# basic elements
html = e('html')

# document metadata
base = e('base', True)
head = e('head')
link = e('link', True)
meta = e('meta', True)
style = e('style')
title = e('title', False, False)

# content sectioning
address = e('address')
article = e('article')
body = e('body')
footer = e('footer')
header = e('header')
h1 = e('h1')
h2 = e('h2')
h3 = e('h3')
h4 = e('h4')
h5 = e('h5')
h6 = e('h6')
hgroup = e('hgroup')
nav = e('nav')
section = e('section')

# text content
dd = e('dd')
div = e('div')
dl = e('dl')
dt = e('dt')
figcaption = e('figcaption')
figure = e('figure')
hr = e('hr', True)
li = e('li')
main = e('main')
ol = e('ol')
p = e('p')
pre = e('pre')
ul = e('ul')

# inline text semantics
a = e('a', False, False)
abbr = e('abbr', False, False)
b = e('b', False, False)
bdi = e('bdi', False, False)
bdo = e('bdo', False, False)
br = e('br', False, False)
cite = e('cite', False, False)
code = e('code', False, False)
data = e('data', False, False)
dfn = e('dfn', False, False)
em = e('em', False, False)
i = e('i', False, False)
kbd = e('kbd', False, False)
mark = e('mark', False, False)
q = e('q', False, False)
rp = e('rp', False, False)
rt = e('rt', False, False)
rtc = e('rtc', False, False)
ruby = e('ruby', False, False)
s = e('s', False, False)
samp = e('samp', False, False)
small = e('small', False, False)
span = e('span', False, False)
strong = e('strong', False, False)
sub = e('sub', False, False)
sup = e('sup', False, False)
time = e('time', False, False)
u = e('u', False, False)
var = e('var', False, False)
wbr = e('wbr', False, False)

# image & multimedia
area = e('area')
audio = e('audio', True)
img = e('img', True)
map = e('map')
track = e('track', True)
video = e('video', True)

# embedded content
embed = e('embed', True)
iframe = e('iframe')
object = e('object')
param = e('param', True)
source = e('source', True)

# scripting
canvas = e('canvas')
noscript = e('noscript')
script = e('script')

# edits
e_del = e('del') #del is reserved word :)
ins = e('ins')

# table content
caption = e('caption')
col = e('col')
colgroup = e('colgroup')
table = e('table')
tbody = e('tbody')
td = e('td')
tfoot = e('tfoot')
th = e('th')
thead = e('thead')
tr = e('tr')

# forms
button = e('button', False, False)
datalist = e('datalist')
fieldset = e('fieldset')
form = e('form')
input = e('input', False, False)
keygen = e('keygen', True)
label = e('label')
legend = e('legend')
meter = e('meter')
optgroup = e('optgroup')
option = e('option', False, False)
output = e('output')
progress = e('progress')
select = e('select')
textarea = e('textarea')

# interactive elements
details = e('details')
dialog = e('dialog')
menu = e('menu')
menuitem = e('menuitem')
summary = e('summary')

# web components
content = e('content')
element = e('element')
shadow = e('shadow')
template = e('template')

