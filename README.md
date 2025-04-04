This project follows the book [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom.

It is an interpreter for [Lox](https://craftinginterpreters.com/the-lox-language.html), a simple
scripting language.

# Using the Interpreter

1. Ensure you have `python (3.12)` installed locally
2. Input your script into `input.txt`
3. Run `python3 -m app.main evaluate input.txt` to run the program implemented in `app/main.py`

```
python3 -m app.main evaluate input.txt
```

Other commands include `parse` and `tokenize` which respectively return the parsed and tokenized versions of input.txt.

```
python3 -m app.main parse input.txt
```
```
python3 -m app.main tokenize input.txt
```
