from common_services import *

file = open(comment_for_classification_file, mode='r')

# read all lines at once
all_comment = file.read()

# close the file
file.close()

file = open(question_for_classification_file, mode='r')

# read all lines at once
all_question = file.read()

# close the file
file.close()
