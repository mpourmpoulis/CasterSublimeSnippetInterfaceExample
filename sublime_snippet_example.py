from dragonfly import (MappingRule, Choice, Dictation, Grammar, Function)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

import subprocess


def insert_snippet(snippet):
    command = r'subl --command "insert_snippet {\"contents\":\"' + snippet + r'\"}'
    subprocess.call(command, shell = True)
    subprocess.call("subl", shell = True)
    
class SublimeSnippetExample(MappingRule):
    pronunciation = "sublime snippet"
    mapping = {
        "<snippet>":
            R(Function(insert_snippet)),
    }
    extras = [
        Choice("snippet",{
                "list comprehension":"[${3:$1} for ${1:x} in $2 ${5:if $4}]",
                "truth assignment":"${1:x} = $1 if $1 else $0",
                
            }
        ),
    ]
    defaults = {}


#---------------------------------------------------------------------------


def get_rule():
    return SublimeSnippetExample, RuleDetails(name="sublime snippet", executable=["sublime_text"])
    
