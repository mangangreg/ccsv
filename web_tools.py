import csv
from pathlib import Path

def compile_css(style_obj, indent=2):
    # Assume simple structure
    css_string = ''
    for selector, rules in style_obj.items():
        css_string += f"{selector} {{\n"
        for key,val in rules.items():
            css_string += f"{indent*' '} {key}: {val};\n"
        css_string += '}\n'
            
    return css_string

def build_table(csv_path):
    table_string = ''
    table_string += '<table>\n<tbody>\n'
    table_string += '<tbody>'
    with open(csv_path, 'r') as rfile:
        for i, row in enumerate(csv.reader(rfile)):
            table_string += '<tr>\n'
            tag = 'td' if i!=0 else 'th'
            for cell in row:
                table_string += f"<{tag}> {cell} </{tag}>"
            table_string += '</tr>\n'
            
        table_string += '</tbody>\n</table>'
    return table_string

def build_html(csv_path, config, outdir='examples'):
    csv_path = Path(csv_path)
    css_string = compile_css(config['style'])
    table_string = build_table(csv_path) 
    html_string = f'''
    <html>
      <head>
        <style>
        {css_string}
        </style>
      </head>
      <body>
        {table_string}
        </body>
    </html>
    '''
    
    if outdir:
        hpath = f"{outdir}/{csv_path.stem}.html"
        with open(hpath, 'w') as wfile:
            wfile.write(html_string)
            
    return html_string, hpath
    
    
    
            
    