import json

from dragonfly import (MappingRule, Choice, Dictation, Grammar, Function,RunCommand,FocusWindow)

from castervoice.lib import control,settings,context
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


############################## INTERFACE WITH SUBLIME ##############################
from castervoice.lib.sublime_snippets import Snippet,SnippetVariant,SnippetTransform,DisplaySnippetVariants

############################## ACTUAL SNIPPETS ##############################

snippets = {
    "declare zero":lambda n:"int "+",".join(["$" + str(x) +" = 0" for x in range(1,n+1)]) + ";",
    "function main":[
        "int main(){\n\t$0\n}\n",
        "int main(int argc, char** argv){\n\t$0\n}\n",
    ],
    "classic loop":[
        'for(int ${2:i} = 0; $2 < ${1:n}; $2++){\n\t$0\n}\n',
        'for(int ${3:i} = 0; $3 < ${1:n}; $3++){\n\tfor(int ${3:j} = 0; $3 < ${2:m}; $3++){\n\t\t$0\n\t}\n}\n',
    ],
    

    "lovely":"#"*30 + " $0 " + "#"*30,
}

############################## TRANSFORMATIONS AVAILABLE ##############################

transformations = {
    "raw": lambda s:json.dumps(s).replace("$","\\$"),
    "alternative raw": [lambda s:json.dumps(s),lambda s:s.replace("$","\\$")],
    "almost raw": lambda s:json.dumps(s),
    "weird J":(r"\{(\d):i\}",r"\{\1:j\}",),
}

delimiter = {
    "space":'" "',
    "line":"std::endl",
    "hello":'"hello"',
}
############################## ACTUALLY CLASS ##############################


class CppSnippetMoreExampleExperimental(MappingRule):
    pronunciation = "sublime snippet"
    mapping = {
        "<snippet>":
            R(Snippet("%(snippet)s")),
        "<snippet_variants> [<n>]":
            R(Snippet("%(snippet_variants)s")),
        "<stream> <thing> [<n>] [with <delimiter>]":
            R(Snippet(lambda stream,thing,n,delimiter:
                stream[0] + stream[1].format(delimiter).join([thing(x) for x in range(1,n + 1)]) + stream[2]
                )
            ),
        "variant (<thing>|<stream>)":
            R(Key("c-z") + SnippetVariant(thing="thing",stream="stream")),
        "apply <transformation>":
            R(Key("c-z") + SnippetTransform("%(transformation)s")),
        "instead apply <transformation>":
            R(Key("c-z") + SnippetTransform("%(transformation)s",steps=1)),
        "display delimiter variants":
            R(Key("c-z") + DisplaySnippetVariants("delimiter",delimiter.values())),

    }
    extras = [
        IntegerRefST("n",1,10),
        Choice("stream",{
            "output":("std::cout<< ",' << {0} << '," << std::endl;"),
            "error":("std::cerr<< ",' << {0} << '," << std::endl;"),
            "input":("std::cin>> "," >> ",";"),
        }),
        Choice("thing",{
            "line": lambda x: "$" + str(x),
            "attribute": lambda x: "$1.$" + str(x+1),
            "index": lambda x: "$1[${0}]".format(x+1),
            "named": lambda x: '"${0}" << " " << ${0}'.format(x),
            "common attribute": lambda x: "${0}.$1".format(x+1),
            "common index": lambda x: "${0}[$1]".format(x+1),
        }),
        Choice("delimiter",delimiter),


        Choice("snippet",{k:v for k,v in snippets.items() if  isinstance(v,str)}),
        Choice("snippet_variants",{k:v for k,v in snippets.items() if  not isinstance(v,str)}),
        Choice("transformation",transformations),
    ]
    defaults = {"n":1,"delimiter":'" "'}




#---------------------------------------------------------------------------


def get_rule():
    return CppSnippetMoreExampleExperimental, RuleDetails(name="new snippet more experimental", executable=["sublime_text"])
    
