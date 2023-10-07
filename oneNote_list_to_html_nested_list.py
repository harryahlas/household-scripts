# paste your onenote or tabular data into the input_text object below and run

def process_line(line):
    tabs = line.count('\t')
    text = line.strip()
    return tabs, text

def convert_to_html(input_text):
    lines = input_text.strip().split('\n')
    stack = []
    html = []
    for line in lines:
        tabs, text = process_line(line)
        while len(stack) > tabs:
            html.append('</ul>')
            stack.pop()
        if len(stack) < tabs:
            html.append('<ul>')
            stack.append(tabs)
        html.append(f'<li>{text}</li>')
    while stack:
        html.append('</ul>')
        stack.pop()

    return '\n'.join(html)

# Usage:
input_text = '''
		§ These two are before the compressor:
			§ Usually adds multiband compression. But it is not an important tool for mastering.
				□ See jens_master_4_linmb.png
				□ Very slow attacks
Just to level things, not to make quieter
'''

html_output = convert_to_html(input_text)
print(html_output)
