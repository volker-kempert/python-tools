# -*- UTF-8 -*-

from verbose import Verboser


def format_duplicates(duplicates, outfile):
    for files in duplicates:
        for file in files:
            outfile.write( "# rm " + file + '\n')
        outfile.write("# --\n")


def format_duplicates_with_remove(duplicates, outfile):
    """ let survive only the first file and remove all the others """
    for files in duplicates:
        for file in files[1:]:
            outfile.write( "rm " + file + '\n')
        outfile.write( "# rm " + files[0] + '\n')
        outfile.write("# --\n")


def read_duplicates(infile):
    duplicates = []
    same_files = []
    count_lines = 0
    for line in infile:
        count_lines += 1

        # process line
        if line == '# --\n':
            # a new set starts
            duplicates.append(same_files)
            same_files = []
        else:
            same_files.append(line[5:-1])

    Verboser().verbose_max("Read Lines {0} Read Record {1}".format(
                                            count_lines, len(duplicates)))
    return duplicates 