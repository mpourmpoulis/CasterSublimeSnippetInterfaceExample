from dragonfly import (MappingRule, Choice, Dictation, Grammar, Repeat, StartApp, Function, BringApp)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

from castervoice.lib import settings, utilities, context, contexts
import shlex
from subprocess import Popen

import json
import os
import re
import subprocess

output_location = "C:\\Users\\Admin\\Desktop\\voice_cpp"
with open(os.path.join(output_location,"documentation.json")) as fp:
    summaries = json.load(fp)

with open(os.path.join(output_location,"snippets.json")) as fp:
    s = json.load(fp)

spoken_mapping = {x[0]:x[1]  for x in summaries}
file_mapping = {x[1]:x[3]  for x in summaries}
modern = re.compile("<content>.</content>",re.DOTALL)
def extract_content(x):
    i = x.find("<![CDATA[") + len("<![CDATA[")
    j = x.find("]]></content>") 
    return x[i:j]


snippets = {k:extract_content(v) for k,v in s}


def show_documentation(item):

    # to make it work with the offline version place in comments
    item=file_mapping[item]
    item = item[item.find("en\\cpp\\")  + len("en\\cpp\\"):]
    website = "https://en.cppreference.com/w/cpp/" + item.replace("\\", "/").replace(".html","")

    # to make it work with the offline version remove comment 
    # and make sure path to the local HTML book is correct
    # website = "file:///" + file_mapping[item]

    browser = utilities.default_browser_command()
    Popen(shlex.split(browser.replace('%1', website)))

def insert_snippet(item):
    print("Item",item)
    use_keys = False
    if use_keys:
        Key("cs-p").execute()
        Text("Snippet: voice_cpp_" + item).execute()
        Key("enter").execute()   
    else:
        y = r'subl --command "insert_snippet {\"contents\":\"' + snippets[item] + r'\"}'
        subprocess.call(y, shell = True)
        subprocess.call("subl", shell = True)

    






class VoiceCpp(MappingRule):
    mapping = {
        "include <library>":
            R(Text("#include <%(library)s>")),
        "document <item>":
            R(Function(show_documentation)),
        "nice <item>":
            R(Function(insert_snippet)),
    }
    extras = [  
        Dictation("description"),   
        IntegerRefST("nn",1,10),
        Choice("item",spoken_mapping),
        Choice("library",{
            'algorithm': 'algorithm', 
            'any': 'any', 
            'array': 'array', 
            'atomic': 'atomic', 
            'bit': 'bit', 
            'bit set': 'bitset', 
            'char convert': 'charconv', 
            'chrono': 'chrono', 
            'code convert': 'codecvt', 
            'compare': 'compare', 
            'complex': 'complex', 
            'concepts': 'concepts', 
            'condition variable': 'condition_variable', 
            'contract': 'contract', 
            'deque': 'deque', 
            'exception': 'exception', 
            'execution': 'execution', 
            'file SYSTEM': 'filesystem', 
            'forward list': 'forward_list', 
            'F stream': 'fstream', 
            'functional': 'functional', 
            'future': 'future', 
            'initializer list': 'initializer_list', 
            'io manipulation': 'iomanip', 
            'ios': 'ios', 
            'io SFWD': 'iosfwd', 
            'io STREAM': 'iostream', 
            'I stream': 'istream', 
            'iterator': 'iterator', 
            'limits': 'limits', 
            'list': 'list', 
            'locale': 'locale', 
            'map': 'map', 
            'memory': 'memory', 
            'memory resource': 'memory_resource', 
            'mu TEX': 'mutex', 
            'new': 'new', 
            'numeric': 'numeric', 
            'optional': 'optional', 
            'O stream': 'ostream', 
            'queue': 'queue', 
            'random': 'random', 
            'ranges': 'ranges', 
            'ratio': 'ratio', 
            'regular expression': 'regex', 
            'scoped allocator': 'scoped_allocator', 
            'set': 'set', 
            'shared mutex': 'shared_mutex', 
            'span': 'span', 
            'S stream': 'sstream', 
            'stack': 'stack', 
            'STD except': 'stdexcept', 
            'stream BUF': 'streambuf', 
            'string': 'string', 
            'string view': 'string_view', 
            'string stream': 'strstream', 
            'SYNC stream': 'syncstream', 
            'system error': 'system_error', 
            'thread': 'thread', 
            'tuple': 'tuple', 
            'type INDEX': 'typeindex', 
            'type INFO': 'typeinfo', 
            'type traits': 'type_traits', 
            'unordered map': 'unordered_map', 
            'unordered set': 'unordered_set', 
            'utility': 'utility', 
            'val ARRAY': 'valarray', 
            'variant': 'variant', 
            'vector': 'vector', 
            'version': 'version'
        }
        )
    ]
    defaults = {
        "nn":1,
    }


#---------------------------------------------------------------------------


def get_rule():
    return VoiceCpp, RuleDetails(name="nothing", executable=["sublime_text","VirtualBox","chrome"])
    #, title="Sublime Text")enable voice C++ enable voice C++
