'''
    Contstant messages to be used with HttpResponse.
    @author Dean Whitbread
    @version 02/12/2022
'''
htmlFile404 = open('lessons/templates/404.html','r')
source_code404 = htmlFile404.read()
DOES_NOT_EXIST_MSG = source_code404

htmlFile403 = open('lessons/templates/403.html','r')
source_code403 = htmlFile403.read()
OTHER_USER_RECORD_MSG = source_code403
#"Cannot change a record created by another user."





MULTIPLE_RECORDS_FOUND_MSG = "Multiple records found. Please contact the system administrator."
CANNOT_BOOK_TWICE_MSG = "Class cannot be booked twice."
