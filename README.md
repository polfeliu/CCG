# CCG. 

CCG is a C/C++ code generation framework for python. It encapsulates the language syntax and grammar with python objects to be able to manipulate them more easily and generate code automatically, with a configurable style.

This library will be the developer's friend for code generation applications. It can be the language abstraction layer for any code generation project for C/C++. It won't do anything that couldn't be done manipulating strings but the code written with it will be easier to write and understand and the style of the generated code won't be embedded in the application, leaving the option to the developer to pass all the style choices to the end user without any effort.

## Documentation
https://ccg.readthedocs.io/

## Quick Demonstration
Declare an C/C++ object, for instance, a function:

```python
f = CFunction(
        name="examplefun",
        return_type=Cuint32,
        static=True,
        arguments=[
            CFunction.Argument(name="first", c_type=Cuint32, doc=Doc("First argument")),
            CFunction.Argument(name="second", c_type=Cdouble, default=CLiteral(2), doc=Doc("Second Argument"))
        ],
        doc=Doc("Awesome function", "This function is awesome because it does marvellous things",
                ret="returns a lucky number"),
        content=CStatements([
            CVariable("local_var", Cint8).declare()
        ])
)
```

Modify the default style and add your own choices:
```python
my_style = Style()
my_style.function_bracket.new_line_open_before = False
```

Print the declaration:
```python
print(f.declare().render(my_style))
```

```C
/**
* @brief Awesome function
*
* This function is awesome because it does marvellous things
* @param first First argument
* @param second Second Argument
* @return returns a lucky number
*/
static uint32_t 
examplefun(uint32_t first, double second = 2);
```

And print the definition:
```python
print(f.define().render(my_style))
```

```C
uint32_t examplefun(uint32_t first, double second){
	int8_t local_var;
};
```
