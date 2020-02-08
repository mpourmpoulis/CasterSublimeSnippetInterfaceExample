from dragonfly import (MappingRule, Choice, Dictation, Grammar, Function,RunCommand,FocusWindow)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

# import subprocess
import json

def send_sublime(c,data):
    # subprocess.Popen(["subl", "--command",c + " " + json.dumps(data)],creationflags = 0x08000000)
    # subprocess.call("subl", shell = True)
    RunCommand(["subl", "--command",c + " " + json.dumps(data)],synchronous = True).execute()
    FocusWindow("sublime_text").execute()    

def insert_snippet(snippet):
    send_sublime("insert_snippet",{"contents": snippet})

variants = []

def insert_snippet_with_variants(snippet_variants,n = 1):
    global variants
    assert isinstance(snippet_variants,list)
    insert_snippet(snippet_variants[n-1])
    variants = snippet_variants


def insert_variant(n):
    insert_snippet(variants[n-1]) 
    
class SublimeSnippetExample(MappingRule):
    pronunciation = "sublime snippet"
    mapping = {
        "<snippet>":
            R(Function(insert_snippet)),
        "<snippet_variants> [<n>]":
            R(Function(insert_snippet_with_variants)),
        "variant <n>":
            R(Key("c-z") + Function(insert_variant)),

    }
    extras = [
        IntegerRefST("n",1,10),
        Choice("snippet",{
                "function definition":'''def ${1:function}($2):\n\t${0:pass}''',
                "class definition":'class ${1:ClassName}(${2:object}):\n\t${3/.+/"""/}${3:docstring for $1}${3/.+/"""\n/}${3/.+/\t/}def __init__(self${4/([^,])?(.*)/(?1:, )/}${4:arg}):\n\t\t${5:super($1, self).__init__()}\n${4/(\A\s*,\s*\Z)|,?\s*([A-Za-z_][a-zA-Z0-9_]*)\s*(=[^,]*)?(,\s*|$)/(?2:\t\tself.$2 = $2\n)/g}\t$0'               
                
            }
        ),
        Choice("snippet_variants",{
                "truth assignment":[
                    "${1:x} = $1 if $1 else $0",
                    "${1:x} = \"${2:something}\" if $2 else $0",
                ],
                "list comprehension":[
                    "[${3:$1} for ${1:x} in $2 ${5:if $4}]",
                    "[$2 for ${2:x} in $1 if $2]",
                ],

                "sorted":
                    ["sorted($1, key = lambda x:x[{0}])".format(i) for i in range(0,10)],
                "sorted attribute":
                    ["sorted($1, key = lambda x: ({0}))".format(",".join(["x.${0}".format(x + 2) for x in range(0,i)])) for i in range(0,10)],

            }

        )
    ]
    defaults = {}



#---------------------------------------------------------------------------


def get_rule():
    return SublimeSnippetExample, RuleDetails(name="sublime snippet", executable=["sublime_text"])
    
