# CasterSublimeSnippetInterfaceExample

Repository for experimenting with sublime snippets and Caster voice commands 

## Contents
<!-- MarkdownTOC  autolink="true" -->

- [Introduction And Motivation](#introduction-and-motivation)
- [First Example](#first-example)
	- [Basic Usage](#basic-usage)
	- [Snippets With Variants Initial](#snippets-with-variants-initial)
- [Custom C++ Snippets](#custom-c-snippets)
	- [Snippets With Variants Improved](#snippets-with-variants-improved)
- [More Experimental Features](#more-experimental-features)
	- [Applying Transformations To Snippets](#applying-transformations-to-snippets)
		- [Potential Improvements](#potential-improvements)
	- [Passing Parameters To Snippets](#passing-parameters-to-snippets)
		- [General About Snippet Parameters](#general-about-snippet-parameters)
		- [Fake Auto Complete](#fake-auto-complete)
		- [Collecting Those Parameters](#collecting-those-parameters)
		- [Improvements](#improvements)
- [Snippets Generated From C++ STL](#snippets-generated-from-c-stl)

<!-- /MarkdownTOC -->

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

(please note that the file has been modified ever since these gif was recorded but you still get the point)


### Snippets With Variants Initial


I have also added some support for snippets with variants, so that you can use suffix integer

```python
"<snippet_variants> [<n>]"
```

to select which alternative from an 1-indexed list of variants of the same snippet you want! In case of error, you can use 

```python
"variant <n>"
```

To pick another variant and you can optionally display those alternatives on the quick panel by using

```python
"display variants"
```

To see that all in action

![example2](./example2.gif)



## Custom C++ Snippets

Inside [custom_cpp.py](./custom_cpp.py) you can find a whole bunch of custom snippets that I have created for my personal usage. You probably might want to change them to suit your needs but they could serve as a baseline, I really had a great time with some of them like `error line [<n>]`!


### Snippets With Variants Improved

This script would take those ideas a bit further and has 2 formats for snippets with variants

* the old 1-indexed list of strings

* a callable which will be fed with the choice `n`, if not provided the default value will be 1

```python
{
    "attribute assign":
        lambda n: "".join(["auto& $"+x+" = $1.$"+x+";\n" for x in string_range(2,n + 2)]),

    "error line":lambda n:"std::cerr<< " + ' << " " << '.join(["$" + str(x) for x in range(1,n + 1)]) + " << std::endl;",
    "error named":lambda n:"std::cerr<< " + ' << " " << '.join(['"${0}" << " " << ${0}'.format(x) for x in range(1,n + 1)]) + " << std::endl;",

    "output attributes":lambda n:"${0:std::cout}<< " + ' << " " << '.join(["$1.$" + str(x) for x in range(2,n + 2)]) + " << std::endl;",
}
```

![example4](./example4.gif)

As you can see, the `variant <n>` command also works with them! 


## More Experimental Features

Inside [custom_cpp_experimental.py](./custom_cpp_experimental.py) you will find more or less the same snippets but with a couple of more features. How useful they actually are and what changes should be made is yet to be determined!

### Applying Transformations To Snippets

A feature that might be of interest is the ability to apply some transformation upon the last snippet inserted. 

```python
"apply <transformation>":
	R(Key("c-z") + Function(transform_last_snippet)),
```

this script currently supports

- callable with a single argument

- tuple if you want to use a regular expression

In the latter case, the tuples should contain anything that you would pass into `re.sub` excluding third parameter which would be the string you apply the substitution on. You can find implementation [here](https://github.com/mpourmpoulis/CasterSublimeSnippetInterfaceExample/blob/master/custom_cpp_experimental.py#L70) for more details!


But on top of that you can also pass in a list of transformations and they will be applied one after another!


![example3](./example3.gif)

#### Potential Improvements

One of the examples above shows two successive commands that apply transformation, with the second being fed the result of the first one! it might make sense to keep a stack so that if we do not like some sequence of transformation we could revert as many steps as we want, or even have a command like

```python
"instead apply <transformation>":
	R(Key("c-z") + Function(transform_last_snippet_instead)),
```

To revert to the last transformation and apply another one instead in a single go

### Passing Parameters To Snippets

#### General About Snippet Parameters

Except from the more classical placeholders,

#### Fake Auto Complete

#### Collecting Those Parameters

#### Improvements


## Snippets Generated From C++ STL

