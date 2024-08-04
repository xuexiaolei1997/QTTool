import re

command = "cd F:\\sadoo\\as"

res = re.search(r"^cd\s+(.*)$", command).group(1)
print(res)
