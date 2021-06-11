# ----------------------------------
# Linter for C89 subset.
# ----------------------------------

# ----------------------------------
# Test Case
# ----------------------------------
# input = ["      if(   ", "i -- 0)", "{   ", "a ", " =1;", "   }     "]


# ----------------------------------
# 1) Remove unnecessary line changes.
# Line changes without ; or { except for line only with }.
# Example)
# if(
# i == 0                if (i==0) {
# ){        into        a = 0;
# a = 0                 }
# ;
# }
# ----------------------------------
def lineCleaner(lines_of_code):

    end = {";", "{"}
    result = []
    token = ""

    for line in lines_of_code:
        line = line.strip()
        line = line.replace(",", " ")
        token += line
        if line == "}":
            result.append(token)
            token = ""
        elif line[-1] not in end:
            pass
        else:
            result.append(token)
            token = ""

    return result


# ----------------------------------
# 2) Whitespace front of '(' and '{', whitespace at front and behind of '+, -, =, <, >, >=, <='.
# Example)
# if(i == 0){} into if (i == 0) {}
# ----------------------------------
def splitSpecial(code_line):
    output = code_line[0]
    for i in range(1, len(code_line)):
        frontSpaced = {"(", "{", ";", "["}
        bothSpaced = {
            "+",
            "-",
            "=",
            "<",
            ">",
        }
        char = code_line[i]
        if char in frontSpaced:
            char = " " + char
        if char in bothSpaced and code_line[i + 1] in bothSpaced:
            char = " " + char
        elif char in bothSpaced and code_line[i - 1] in bothSpaced:
            char = char + " "
        elif char in bothSpaced:
            char = " " + char + " "
        output += char

    return output


# ----------------------------------
# TODO
# 3) Need to change line after ';' and '{'.
#    Need to change line before and after '}'.
#    Consider arrays and for loop?
#
# 4) Determine post/pre of ++, --.
# ----------------------------------

# ----------------------------------
# Linter
#
# input: list of strings.
# output: list of strings.
# ----------------------------------
def lint(source):
    compressed = lineCleaner(source)
    result = []
    for line in compressed:
        result.append(splitSpecial(line))

    return result
