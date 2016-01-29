import re

# Regex for complete valid reference link with double quote wrapped title
valid_reference_link_pattern_double_quote =r'^ {0,3}\[.+\]:\s+\S*#\S+\s+".+"\s*$'
# Regex for complete valid reference link with single quote wrapped title
valid_reference_link_pattern_single_quote =r"^ {0,3}\[.+\]:\s+\S*#\S+\s+'.+'\s*$"
# Regex for complete valid reference link with parentheses wrapped title
valid_reference_link_pattern_parentheses =r"^ {0,3}\[.+\]:\s+\S*#\S+\s+(.+)\s*$"
# Regex for complete valid reference link with no title
valid_reference_link_pattern_notitle =r"^ {0,3}\[.+\]:\s+\S*#\S+\s*$"

valid_ref_double_regex = re.compile(valid_reference_link_pattern_double_quote, re.UNICODE)
valid_ref_single_regex = re.compile(valid_reference_link_pattern_single_quote, re.UNICODE)
valid_ref_paren_regex = re.compile(valid_reference_link_pattern_parentheses, re.UNICODE)
valid_ref_notitle_regex = re.compile(valid_reference_link_pattern_notitle, re.UNICODE)

def is_valid_reference_link(string):
	return (valid_ref_double_regex.match(string) or valid_ref_single_regex.match(string)
		or valid_ref_paren_regex.match(string) or valid_ref_notitle_regex.match(string) )
