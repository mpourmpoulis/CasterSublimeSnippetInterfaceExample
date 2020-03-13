# CasterSublimeSnippetInterfaceExample

Repository for experimenting with sublime snippets and Caster voice commands 

## Introduction And Motivation

When programming by voice, utilizing code snippets can have an important impact on improving your speed and making your overall experience more enjoyable! Nonetheless, creating such snippets can be time-consuming, because you need to create all the individual .sublime-snippet files containing the actual content of those snippets as well as the voice grammar containing commands to trigger them!

This is a proof of concept that lifts these restriction and which I hope will make your life easier by enabling you to do everything from only the grammar side!

None of the following, and I mean literally NONE (including the quick panel!), requires any additional code running on the sublime side and in fact not even a single .sublime-snippet file! Everything can be directly edited from within the grammar which uses the sublime command line interface `subl` to insert custom (possibly even dynamically generated) snippets!

But enough blah blah let's get going!

## First Example

Let's start with the [original example](./sublime_snippet_example.py)

### Basic Usage

As they say, a gif is worth a thousand words

![example](./example.gif)





## Snippets With Variants

I have also added some support for snippets with variants and you can optionally display those alternatives on the quick panel as you can see below

![example2](./example2.gif)

Hope this helps!

## Snippets With Variants 


