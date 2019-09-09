

from bs4 import BeautifulSoup, Comment, NavigableString

def removeAttrs(soup):
    """Remove all tags from the soup object
    """
    for tag in soup.findAll(True): 
        tag.attrs = {}
    return soup

def stripTags(html, invalid_tags):
    """ Remove specific tags from html
    """
    try:
        soup = BeautifulSoup(html, features="lxml")
    except:
        soup = BeautifulSoup(html, features="lxml")
    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                try:
                    if not isinstance(c, NavigableString):
                        c = stripTags(str(c), invalid_tags)
                    s += str(c)
                except:
                    print("Failed to strip Tags")
            tag.replaceWith(s)
    return soup

def stripCustom(html):
    """ Stripping html str imgs, and/or class styles
    """
    try:
        soup = BeautifulSoup(html, features="lxml")
    except:
        soup = BeautifulSoup(html, features="lxml")
    for script in soup(["img"]): # remove all javascript and stylesheet code
        script.extract()

    for tag in soup:
        try:
            for attribute in ["class", "data-aria"]: # You can also add id,style,etc in the list
                del tag[attribute]
        except:
            print('tags deleting')

    for child in soup:
        try:
            if isinstance(child, Comment):
                child.extract()
        except:
            print("Failed to extract comment")

    return soup


def get_fund_code(td_bank_fund_name):
    """Td bank fund name (leftmost column)

    Example: TD Balanced Growth Fund - I Fund Code Multiple TDB970
    """
    fund_list = str(td_bank_fund_name).split()
    return fund_list[-1]

def get_strip_fund_code(td_bank_fund_name):
    """Td bank fund name (leftmost column)

    Example: TD Balanced Growth Fund - I Fund Code Multiple TDB970
    """
    fund_list = td_bank_fund_name.split()
    return ' '.join(fund_list[:-4])

def strip_rbc_footnote(rbc_bank_fund_desc):
    """Td bank fund name (leftmost column)

    Example: TD Balanced Growth Fund - I Fund Code Multiple TDB970
    """
    result = ''.join(i for i in rbc_bank_fund_desc if not i.isdigit())
    result = result.replace('Footnote','')
    return result

def get_td_rows(td_df):
    """Extracts rows of interest from dataframe 
    """
    clean_df = td_df
    return clean_df