import os
import re


a = "sr"
suggest = list(filter(lambda x: x.startswith(a), os.listdir(".")))

command = "cd F:\\sadoo\\as"

res = re.search(r"^cd\s+(.*)$", command).group(1)
print(res)
