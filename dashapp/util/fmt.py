import re
from parse_config import get_config
# TODO Split into formatting functions and actually utility functions
# Tex based functions to add highlighting to tabular data.
def add_url(url_str='http://google.com'):
    min_point = min(int(len(url_str) / 2), 20)
    middle_txt = url_str[8:min_point]
    return r'\href{{{}}}{{{}}}'.format(url_str, middle_txt)

def format_date(date='2019-02-08'):
    # Slices the YYYY-MM-DD part from the inputted string
    return date[:10] 
def add_url_complex(url_str='http://google.com'):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url_str) is not None:
        url_str = r'\url{{{}}}'.format(url_str)
    else:
        return url_str
# Add latex formatting and colour keywords of interest.
def highlight_keywords(data_str='Bitcoin By Agence France-Presse US job creation came back to life in March, possibly assuaging recession fears and allowing Donald Trump a sigh of relief. New construction at a building site in New York City in March 2019  US job creation came back to life in March'):
    
    if type(data_str) in [int, float]:
        return data_str

    cfg = get_config()
    # keyword categories
    keyword_data = cfg['categories']
    for idx, category in enumerate(keyword_data.keys()):
        color = keyword_data[category]['color']
        keywords = keyword_data[category]['keywords']
        for keyword in keywords:
            # perhaps add word boundary for keyword
            # This is the simple implementation, regex allows for case insenstive searches
            # colored_keyword = '\\textcolor{{{}}}{{{}}}'.format(color, keyword)
            # data_str = data_str.replace(keyword,colored_keyword)
            colored_keyword = r'\\textcolor{{{}}}{{{}}}'.format(color, keyword)
            insen_keyword = re.compile(re.escape(keyword), re.IGNORECASE)
            data_str = insen_keyword.sub(colored_keyword,data_str)

    # Since I am using latex without escaping special characters, replace $ and %
    data_str = fmt_proper_tex(data_str)
    return data_str

def fmt_proper_tex(data_str=''):
    data_str = data_str.replace('$','\$')
    data_str = data_str.replace('%','\%')
    data_str = data_str.replace('&','\&')
    # strip html tags 
    data_str = re.sub('<[^<]+?>', '', data_str)
    return data_str

def color_negative_red(data_item):
    color = 'red' if data_item < 1 else 'black'
    return 'color: %s' % color

def color_loss_red(x):
    # Try to make number float
    try:
        x = float(x)
    except ValueError:
        pass
    if type(x) in [int, float]:
        if float(x) < 1.00:
            return '\\textcolor{red}{%1.5f}' % x
        else:
            return '%1.5f' % x
    else:
        # With attempts to convert to float, this condition 
        # is no longer called
        if str(x) == 'nan':
            return 'N/A'
        else:
            return '%s' % fmt_proper_tex(x)

# Example color loss function for latex formatting
def color_loss_red(x):
    print(x)
    print(type(x))
    if type(x) in [int, float]:
        return '%1.4f' % x
    else:
        return '%s %s' % (x, 'fake news')