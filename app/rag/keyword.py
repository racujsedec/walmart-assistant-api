import re
def lexical_score(query:str,text:str)->int:
 terms=set(re.findall(r'[a-z]{3,}',query.lower()))
 return len(terms & set(re.findall(r'[a-z]{3,}',text.lower())))
