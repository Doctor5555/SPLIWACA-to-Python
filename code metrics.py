import os
import re


class File:
    def __init__(
        this,
        lines,
        includes,
        comments,
        whitespace,
        l_lines,
        l_includes,
        l_comments,
        l_whitespace,
        filename,
    ):
        this.lines = str(lines)
        this.includes = str(includes)
        this.comments = str(comments)
        this.whitespace = str(whitespace)
        this.actual_lines = str(
            int(this.lines) - int(this.whitespace) - int(this.comments)
        )
        this.l_lines = l_lines
        this.l_includes = l_includes
        this.l_comments = l_comments
        this.l_whitespace = l_whitespace
        this.filename = filename


def calculateMetrics(lines, filename):
    includes = []
    comments = []
    whitespace = []
    multi_line_comment = False

    for line in lines:
        if lines.index(line) == 137:
            # print(line)
            pass
        line_no_tabs = re.sub("[\t]", "", line)
        if line_no_tabs.startswith("//") and not multi_line_comment:
            comments.append(line)
        if "/*" in line_no_tabs and not multi_line_comment:
            multi_line_comment = True
            if line_no_tabs.startswith("/*"):
                comments.append(line)
        if "*/" in line_no_tabs and multi_line_comment:
            multi_line_comment = False
            if line_no_tabs.endswith("*/"):
                if line_no_tabs.startswith("/*") or "/*" not in line_no_tabs:
                    comments.append(line)
        if multi_line_comment:
            comments.append(line)

        if line not in comments:
            if line.startswith("#include"):
                includes.append(line)
            if not re.search("[a-zA-Z]", line) or line == "#pragma once":
                whitespace.append(line)
                if lines.index(line) == 137:
                    # print(line)
                    pass

    file = File(
        len(lines),
        len(includes),
        len(comments),
        len(whitespace),
        lines,
        includes,
        comments,
        whitespace,
        filename,
    )

    return file


def Str(Int: int, Len: int):
    Str = str(Int)
    for i in range(Len - len(Str)):
        Str = " " + Str
    return Str


path = "c:\\dev\\EPQ Spliwaca"

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for dir in d:
        if "vendor" in dir:
            d.remove(dir)
    for file in f:
        if ".h" in file:
            files.append(os.path.join(r, file))
        if ".cpp" in file:
            files.append(os.path.join(r, file))

data = []

longest_file_name_length = 0
for f in files:
    open_file = open(f)
    lines = open_file.readlines()
    metrics = calculateMetrics(lines, f)
    data.append(metrics)
    if len(metrics.filename) > longest_file_name_length:
        longest_file_name_length = len(metrics.filename)
    open_file.close()

total_lines = 0
total_includes = 0
total_comments = 0
total_whitespace = 0

for file in data:
    print(
        "File: "
        + file.filename[len(path) + 1 :]
        + " " * (longest_file_name_length - len(file.filename))
        + "   total line count: "
        + Str(int(file.lines), 4)
        + ", comment lines: "
        + Str(int(file.comments), 4)
        + ", include lines: "
        + Str(int(file.includes), 4)
        + ", whitespace: "
        + Str(int(file.whitespace), 4)
        + ", total loc: "
        + Str(int(file.actual_lines), 4)
    )
    total_lines += int(file.lines)
    total_includes += int(file.includes)
    total_comments += int(file.comments)
    total_whitespace += int(file.whitespace)

print("\n")

print("Total line count: " + str(total_lines))
print("Total include lines:" + str(total_includes))
print("Total comment lines:" + str(total_comments))
print("Total whitespace:" + str(total_whitespace))
print(
    "Actual loc:"
    + str((total_lines - total_comments - total_whitespace - total_includes))
)

while not input():
    pass