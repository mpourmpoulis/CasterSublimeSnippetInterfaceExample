# CasterSublimeSnippetInterfaceExample
repository for experimenting with sublime snippets and Caster voice commands 

This a's proof of concept that I hope will make it easier for you to combine code snippets with voice commands. it uses the sublime command line interface `subl` to insert custom snippets!


None of the following requires any additional code running on the sublime side and in fact not even .sublime-snippet files also can directly edit/create snippets from within the grammar. See the [example](./sublime_snippet_example.py)

As they say, a gif is worth a thousand words

![example](./example.gif)

Maybe not the best example but what ever:)
please also note you need to be careful with escaping special characters such as `\n` like using `\\n` or raw strings `r"\n"` and there are technicalities with `"` but I hope you get the point!