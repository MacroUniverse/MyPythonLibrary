#! /usr/bin/python3

import os

# Define the code you want to add
code_to_add = """
	<!--百度统计-->
	<script>
		var _hmt = _hmt || [];
		(function() {
			var hm = document.createElement("script");
			hm.src = "https://hm.baidu.com/hm.js?3c7614be3026469d5a60f41ab30b5082";
			var s = document.getElementsByTagName("script")[0]; 
			s.parentNode.insertBefore(hm, s);
			})();
	</script>
"""
# Get a list of all HTML files in the current directory
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# Loop through each file
for file_name in html_files:
    print(file_name, '...')
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Find the first </head> tag and add the code before it
    for i, line in enumerate(content):
        if '</head>' in line:
            content.insert(i, code_to_add)
            break

    # Write the content back to the file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(content)

print("Done!")
