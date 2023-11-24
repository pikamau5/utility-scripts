the_file = 'W:\\houdini-gpt\\used files\\vex-scraped.txt'
the_file2 = 'W:\\houdini-gpt\\used files\\vex-scraped2.txt'
inputFile = open(the_file, "r", encoding="utf-8")
exportFile = open(the_file2, "w", encoding="utf-8")
for line in inputFile:
   new_line = line.replace('\t', ' ')
   exportFile.write(new_line)

inputFile.close()
exportFile.close()