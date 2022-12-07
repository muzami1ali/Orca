'''
    Contstant messages to be used with HttpResponse.
    @author Dean Whitbread
    @version 02/12/2022
'''
htmlFile = open('404.html','r')
source_code = htmlFile.read()
OTHER_USER_RECORD_MSG = "Cannot change a record created by another user."


DOES_NOT_EXIST_MSG = source_code


MULTIPLE_RECORDS_FOUND_MSG = "Multiple records found. Please contact the system administrator."
