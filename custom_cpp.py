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

variants = []
last_inserted=None

def send_sublime(c,data):
    RunCommand(["subl", "-b","--command",c + " " + json.dumps(data)],synchronous = True).execute()
  

def insert_snippet(snippet):
    global last_inserted
    last_inserted = snippet
    send_sublime("insert_snippet",{"contents": snippet})



def insert_snippet_with_variants(snippet_variants,n = 1, **kwargs):
    global variants
    if isinstance(snippet_variants,list):
        insert_snippet(snippet_variants[n-1])
        variants = snippet_variants
    else:
        insert_snippet(snippet_variants(n))



def insert_variant(n):
    insert_snippet_with_variants(variants,n)

def display_variants():
    items = [{"caption":json.dumps(x),"command":"insert_snippet","args":{"contents":x}} for x in variants]
    send_sublime("quick_panel",{"items":items})




def string_range(lower,upper):
    for i in range(lower,upper):
        yield str(i)

def dollar_range(lower,upper):
    for i in range(lower,upper):
        yield "$" + str(i)

def dollar(x):
    return "$" + str(x)



snippets = {
    "just kidding":[
        "${1:x}=$0;" 
    ],

    "auto assign":[
        "auto $1  = $0;",
        "auto [$1]  = $0;",
        "auto& $1  = $0;",
        "auto& [$1]  = $0;",
        "auto $1  = *$0;",
    ],

    "attribute assign":
        lambda n: "".join(["auto& $"+x+" = $1.$"+x+";\n" for x in string_range(2,n + 2)]),
    "reverse attribute assign":
        lambda n: "".join(["$1.$"+x+" = $"+x+";\n" for x in string_range(2,n + 2)]),
    "assign true":"$1 = true;",
    "assign false":"$1 = false;",

    "get": lambda n:"std::get<{0}>($0)".format(n),


    "output line":lambda n:"std::cout<< " + ' << " " << '.join(["$" + str(x) for x in range(1,n + 1)]) + " << std::endl;",
    "output stream":lambda n:"os << " + ' << " " << '.join(["$" + str(x) for x in range(1,n + 1)]) + " << std::endl;",
    "input line":lambda n:"std::cin >> " + ' >> '.join(["$" + str(x) for x in range(1,n + 1)]) + ';',
    "input stream":lambda n:"is >> " + ' >> '.join(["$" + str(x) for x in range(1,n + 1)]) + ';',
    "error line":lambda n:"std::cerr<< " + ' << " " << '.join(["$" + str(x) for x in range(1,n + 1)]) + " << std::endl;",
    "error named":lambda n:"std::cerr<< " + ' << " " << '.join(['"${0}" << " " << ${0}'.format(x) for x in range(1,n + 1)]) + " << std::endl;",

    "output attributes":lambda n:"${0:std::cout}<< " + ' << " " << '.join(["$1.$" + str(x) for x in range(2,n + 2)]) + " << std::endl;",
    "input attributes":lambda n:"${0:std::cin} >> " + ' >> '.join(["$1.$" + str(x) for x in range(2,n + 2)]) + ";",


    "overload output":[
        'std::ostream& operator << (std::ostream& os,const $1& $2){\n\t$0\n\treturn os;\n}\n'
    ],
    "overload input":[
        'std::istream& operator >> (std::istream& is,const $1& $2){\n\t$0\n\treturn is;\n}\n'
    ],
    
    "output container":[
        'std::copy($1.begin(),$1.end(),std::ostream_iterator<${2:int}>(${4:std::cout}," "));\n',
        'for(auto& ${1:x}:${2:v}){\n'
        '\tstd::copy($1.begin(),$1.end(),std::ostream_iterator<${3:int}>(${4:std::cout}," "));\n'
        '\tstd::cout<< std::endl;\n'
        '}\n',

    ],
    "input container":[
        'std::copy_n(std::istream_iterator<${3:int}>(${4:std::cin}), $2, std::back_inserter(${1:v}));',
    ],
    
    "input old": lambda n:'scanf("' + "%d"*n + '",' + ','.join(["&"+x for x in dollar_range(1,n+1)])+');',
    

    "single lambda":[
        '[](auto a){return $0;}',
        '[=](auto a){return $0;}',
        '[&](auto a){return $0;}',
        '[](auto ${1:a}){\n\t$0\n}',
        '[=](auto ${1:a}){\n\t$0\n}',
        '[&](auto ${1:a}){\n\t$0\n}',
    ],
    "single lambda assign":"auto $1 = [&](auto ${2:a}){\n\t$0\n};",
    "double lambda":[
        '[](auto a,auto b){return $0;}',
        '[=](auto a,auto b){return $0;}',
        '[&](auto a,auto b){return $0;}',
        '[](auto ${1:a},auto ${2:b}){\n\t$0\n}',
        '[=](auto ${1:a},auto ${2:b}){\n\t$0\n}',
        '[&](auto ${1:a},auto ${2:b}){\n\t$0\n}',
        
    ],
    "double lambda assign":"auto $1 = [&](auto ${2:a},auto ${3:b}){\n\t$0\n};",

    "evaluation comparison":[
        "$1(${2:a})<$1(${3:b})",
        "$1(${2:a})>$1(${3:b})",
        "$1(${2:a})==$1(${3:b})",
        "$1(${2:a})!=$1(${3:b})",
    ],
    "attribute comparison":[
        "${2:a}.$1 < ${3:b}.$1",
        "${2:a}.$1 > ${3:b}.$1",
        "${2:a}.$1 == ${3:b}.$1",
        "${2:a}.$1 != ${3:b}.$1",
    ],
    "look up comparison":[
        "$1[${2:a}] < $1[${3:b}]",
        "$1[${2:a}] > $1[${3:b}]",
        "$1[${2:a}] == $1[${3:b}]",
        "$1[${2:a}] != $1[${3:b}]",
    ],
    

    "declare visited":"std::vector<bool> ${2:visited}(${1:n},false);",
    "declare zero":lambda n:"int "+",".join([x+" = 0" for x in dollar_range(1,n+1)]) + ";",
    "declare begin":"auto $1 = $2.begin();",
    "declare end":"auto $1 = $2.end();",
    "declare size":"auto $1 = $2.size();",

    "classic loop":[
        'for(int ${2:i} = 0; $2 < ${1:n}; $2++){\n\t$0\n}\n',
        'for(int ${3:i} = 0; $3 < ${1:n}; $3++){\n\tfor(int ${3:j} = 0; $3 < ${2:m}; $3++){\n\t\t$0\n\t}\n}\n',
    ],
    
    "range loop":[
        "for(auto ${1:x} : ${2:v}){\n\t$0\n}\n",
        "for(auto ${1:x} : ${2:v}){\n\tfor(auto ${3:y}:$1){\n\t\t$0\n\t}\n}\n",
    ],
    "reference loop":[
        "for(auto& ${1:x} : ${2:v}){\n\t$0\n}\n",
        "for(auto& ${1:x} : ${2:v}){\n\tfor(auto& ${3:y}:$1){\n\t\t$0\n\t}\n}\n",
    ],
    "double reference loop":[
        "for(auto&& ${1:x} : ${2:v}){\n\t$0\n}\n",
        "for(auto&& ${1:x} : ${2:v}){\n\tfor(auto& ${3:y}:$1){\n\t\t$0\n\t}\n}\n",
    ],
   
    "zip loop":[
        "for(auto $1 = $2.begin(); $1 < $2.end(); $1++){\n\t$0\n}\n",
        "for(auto $1 = $2.begin(), $3 = $4.begin(); $1 < $2.end() && $3 < $4.end(); $1++,$3++){\n\t$0\n}\n",
    ],

    "loop range":"for(auto&& $1 : range($2)){\n\t$0\n}\n",
    "loop enumerate":"for(auto&& $1 : enumerate($2)){\n\t$0\n}\n",
    "loop zip":"for(auto&& $1 : zip($2)){\n\t$0\n}\n",
    "loop I map":"for(auto&& $1 : imap($2)){\n\t$0\n}\n",
    "loop filter":"for(auto&& $1 : filter($2)){\n\t$0\n}\n",
    "loop filter false":"for(auto&& $1 : filterfalse($2)){\n\t$0\n}\n",
    "loop unique everseen":"for(auto&& $1 : unique_everseen($2)){\n\t$0\n}\n",
    "loop takewhile":"for(auto&& $1 : takewhile($2)){\n\t$0\n}\n",
    "loop dropwhile":"for(auto&& $1 : dropwhile($2)){\n\t$0\n}\n",
    "loop cycle":"for(auto&& $1 : cycle($2)){\n\t$0\n}\n",
    "loop repeat":"for(auto&& $1 : repeat($2)){\n\t$0\n}\n",
    "loop count":"for(auto&& $1 : count($2)){\n\t$0\n}\n",
    "loop groupby":"for(auto&& $1 : groupby($2)){\n\t$0\n}\n",
    "loop starmap":"for(auto&& $1 : starmap($2)){\n\t$0\n}\n",
    "loop accumulate":"for(auto&& $1 : accumulate($2)){\n\t$0\n}\n",
    "loop compress":"for(auto&& $1 : compress($2)){\n\t$0\n}\n",
    "loop sorted":"for(auto&& $1 : sorted($2)){\n\t$0\n}\n",
    "loop sorted":"for(auto&& $1 : sorted($2)){\n\t$0\n}\n",
    "loop chain":"for(auto&& $1 : chain($2)){\n\t$0\n}\n",
    "loop chain from iterable":"for(auto&& $1 : chain.from_iterable($2)){\n\t$0\n}\n",
    "loop reversed":"for(auto&& $1 : reversed($2)){\n\t$0\n}\n",
    "loop slice":"for(auto&& $1 : slice($2)){\n\t$0\n}\n",
    "loop sliding window":"for(auto&& $1 : sliding_window($2)){\n\t$0\n}\n",
    "loop chunked":"for(auto&& $1 : chunked($2)){\n\t$0\n}\n",
    "loop batched":"for(auto&& $1 : batched($2)){\n\t$0\n}\n",
    "loop product":"for(auto&& $1 : product($2)){\n\t$0\n}\n",
    "loop combinations":"for(auto&& $1 : combinations($2)){\n\t$0\n}\n",
    "loop combinations_with_replacement":"for(auto&& $1 : combinations_with_replacement($2)){\n\t$0\n}\n",
    "loop permutations":"for(auto&& $1 : permutations($2)){\n\t$0\n}\n",
    "loop powerset":"for(auto&& $1 : powerset($2)){\n\t$0\n}\n",

    "function template":[
        "template<class T>\nauto $1($3${2:const T& t}){\n\t$0\n}\n",
        "template<class T,class U>\nauto $1($4${2:const T& t},${3:const U& u}){\n\t$0\n}\n",
    ],
    "function main":[
        "int main(){\n\t$0\n}\n",
        "int main(int argc, char** argv){\n\t$0\n}\n",
    ],

    "condition end":"$0 == ${1:v}.end()",
    "condition not end":"$0 != ${1:v}.end()",
    
}








class CppSnippetExample(MappingRule):
    pronunciation = "sublime snippet"
    mapping = {
        "<snippet>":
            R(Function(insert_snippet)),
        "<snippet_variants> [<n>]":
            R(Function(insert_snippet_with_variants)),
        "variant <n>":
            R(Key("c-z") + Function(insert_variant)),
        "display variants":
            R(Key("c-z") + Function(display_variants)),
        "small test":
            R(Function(send_sublime,c = "insert_snippet",data = {"contents":"${1:$PARAK}=2","PARAK":"x"})),
        "small jerry":
            R(Function(send_sublime,c = "prev_field",data = {})),


    }
    extras = [
        IntegerRefST("n",1,10),
        Choice("snippet",{k:v for k,v in snippets.items() if  isinstance(v,str)}),
        Choice("snippet_variants",{k:v for k,v in snippets.items() if  not isinstance(v,str)}),
    ]
    defaults = {}



#---------------------------------------------------------------------------


def get_rule():
    return CppSnippetExample, RuleDetails(name="new snippet", executable=["sublime_text"])
    
