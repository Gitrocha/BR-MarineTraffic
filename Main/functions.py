import os


def find_folders(xpath):

    result = []
    listdir = os.listdir(xpath)
    print('ListDIR', listdir)

    '''
    for filename in listdir:  # loop through all the files and folders
        if os.path.isdir(
                os.path.join(os.path.abspath("."), filename)):  # check whether the current object is a folder or not
            result.append(filename)
    '''

    for filename in listdir:  # loop through all the files and folders
        if os.path.isdir(xpath / filename):  # check whether the current object is a folder or not
            result.append(filename)
    result.sort()

    return result

#print(find_folders('.'))
#print('done')