# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph,Image
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import cm,inch
# from functools import partial
# header_text = "Your Header Text Here"
# def header(canvas, doc, content):
#     canvas.saveState()
#     w, h = content.wrap(doc.width, doc.topMargin)
#     content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
#     canvas.restoreState()

# styles = getSampleStyleSheet()
# filename = "output_with_header.pdf"
# PAGESIZE = letter

# pdf = SimpleDocTemplate(filename, pagesize=PAGESIZE, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=1.5 * cm, bottomMargin=2.5 * cm)

# frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 2 * cm, id='normal')
# header_content = Paragraph(header_text, styles['Normal'])

# template = PageTemplate(id='test', frames=frame, onPage=partial(header, content=header_content))
# pdf.addPageTemplates([template])

# image_path = "Pics/rci as logo.jpg"
# image_width = 2.5  # Adjust width in inches
# image_height = 0.7  # Adjust height in inches
# elements = []



#         # elements.append(Image(image_path, left=inch * image_width, top=inch * image_height, width=inch * image_width, height=inch * image_height))
# elements.append(Image(image_path, width=inch * image_width, height=inch * image_height))


# pdf.build(elements)


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Image,Spacer,PageBreak
from reportlab.lib import colors
from reportlab.graphics.shapes import Line

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm,inch
import datetime

def findSampleIndex(ref_id, table):
    for i in range(len(table)):
        if table[i][0] == ref_id:
            return i
        
    return -1


filename = "output_with_header.pdf"

doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=20,  # Adjust as needed
                        rightMargin=2.2, topMargin=1.5, bottomMargin=2.5)

elements = []

# Define your header content
header_font_size = 10

# Define styles
styles = getSampleStyleSheet()
header_style = styles['Heading1']
header_style.fontSize = header_font_size
header_style.alignment =1

# Create content elements
image_path = "Pics/rci as logo.png"
image_width = 2.5  # Adjust width in inches
image_height = 0.5  # Adjust height in inches
elements.append(Image(image_path, width=inch * image_width, height=inch * image_height))
header_text = "FINAL CERTIFICATE OF ANALYSIS"
elements.append(Paragraph(header_text, header_style))
header_text = "REVISION 0"
elements.append(Paragraph(header_text, header_style))
# elements.append(Spacer(1, 0.5 * cm))  # Adjust spacing


# Define styles (optional)
styles = getSampleStyleSheet()
contact_style = styles['Normal']  # Adjust style as needed

# Create paragraphs for contact information
from_text = Paragraph("FROM:         RCI Analytical Services", contact_style)
tel_text = Paragraph("TEL:", contact_style)
fax_text = Paragraph("FAX:", contact_style)
date_text = Paragraph(f"Date:       {datetime.date.today()}", contact_style)
current_time = datetime.datetime.now().time()
time_text = Paragraph(f"Time:       {current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}", contact_style)

# elements.append(Spacer(1, 0.5 * cm))  # Adjust spacing

# Add paragraphs to elements list
elements.append(from_text)
elements.append(tel_text)
elements.append(fax_text)
elements.append(date_text)
elements.append(time_text)

elements.append(Spacer(1, 0.5 * cm))  # Adjust spacing


sample_data = [[["Ref ID", "Grams", "Ml", "Cal % CR","% Calc Cr2O3"]],
            [["Ref ID", "Grams", "Ml", "Cal % CR"]],
            [["Ref ID", "Grams", "Ml", "%Fe", "%FeO"]]]

chrome_sample=[
               ['Rcr1', '2.0', '30.0', '4.55', '6.64'], 
               ['Ricr1', '5.0', '60.0', '3.64', '5.31'], 
               ['Rcr2', '2.0', '40.0', '6.06', '8.86'], 
               ['Ricr2', '4', '60.0', '4.55', '6.64'], 
               ['Rcr3', '8.0', '8.0', '0.3', '0.44']]

fe_sample=[
           ['Rfe1', '8.0', '90.0', '3.32'], 
           ['Rife1', '3.0', '50.0', '4.92'], 
           ['Rfe2', '5.0', '70.0', '4.14'], 
           ['Rife2', '15.0', '55.0', '1.08'], 
           ['Rfe3', '12.0', '34.0', '0.84']]

iron_sample=[ 
             ['Ricr1', '2.0', '10.0', '2.72', '3.5'], 
             ['Ri1', '4.0', '3.0', '0.41', '0.52'], 
             ['Ri2', '5.0', '8.0', '0.87', '1.12'], 
             ['Rife1', '5.0', '40.0', '4.35', '5.6'], 
             ['Ri3', '3.0', '8.0', '1.45', '1.87'], 
             ['Ricr2', '4.0', '70.0', '9.52', '12.25'], 
             ['Ri4', '5.0', '59.0', '6.42', '8.26'], 
             ['Rife2', '34.0', '45.0', '0.72', '0.93'], 
             ['Ri5', '6.0', '6.0', '0.54', '0.7']]


sampletables = [chrome_sample,fe_sample,iron_sample]


for i in range(3):
    for row in range(len(sampletables[i])):
        row_data = []
        for col in range(len(sampletables[i][0])):
            item = sampletables[i][row][col]
            row_data.append(item if item else "")
        sample_data[i].append(row_data)
    print(sample_data[i])

    # Add the Sample Table to the elements
    sample_table = Table(sample_data[i], hAlign='LEFT')
    sample_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('BACKGROUND', (0,0), (0,-1), colors.blue),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)
    ]))
    elements.append(sample_table)


elements.append(PageBreak())




samples_data = [["Sample Ref ID","CR %","Cr2O3","Fe %", "Fe0 %"]]
for i in range(len(iron_sample)):
    if i < len(iron_sample):
        index_chrome = findSampleIndex(iron_sample[i][0],chrome_sample)
        if index_chrome != -1 :
            item = [iron_sample[i][0],chrome_sample[index_chrome][3],chrome_sample[index_chrome][4],iron_sample[i][3],iron_sample[i][3]]
            samples_data.append(item)
            iron_sample.pop(i)
            chrome_sample.pop(index_chrome)
            i+=1
        
for i in range(len(iron_sample)):
    if i < len(iron_sample):
        index_fe = findSampleIndex(iron_sample[i][0],fe_sample)
        if index_fe != -1 :
            item = [iron_sample[i][0],fe_sample[index_fe][3],"",iron_sample[i][3],iron_sample[i][3]]
            samples_data.append(item)
            iron_sample.pop(i)
            fe_sample.pop(index_fe)
            i+=1

for i in range(len(chrome_sample)):
    item = [chrome_sample[i][0],chrome_sample[i][3],chrome_sample[i][4],"",""]
    samples_data.append(item)

for i in range(len(fe_sample)):
    item = [fe_sample[i][0],fe_sample[i][3],"","",""]
    samples_data.append(item)

for i in range(len(iron_sample)):
    item = [iron_sample[i][0],"","",iron_sample[i][3],iron_sample[i][4]]
    samples_data.append(item)

print(samples_data)
# sample_data = [['Sample Ref ID', 'CR %', 'Cr2O3', 'Fe %', 'Fe0 %'], ['Ricr1', '3.64', '5.31', '2.72', '2.72'], ['Ricr2', '4.55', '6.64', '9.52', '9.52'], ['Rife1', '4.92', '', '4.35', '4.35'], ['Rife2', '1.08', '', '0.72', '0.72'], ['Rcr1', '4.55', '6.64', '', ''], ['Rcr2', '6.06', '8.86', '', ''], ['Rcr3', '0.3', '0.44', '', ''], ['Rfe1', '3.32', '', '', ''], ['Rfe2', '4.14', '', '', ''], ['Rfe3', '0.84', '', '', ''], ['Ri1', '', '', '0.41', '0.52'], ['Ri2', '', '', '0.87', '1.12'], ['Ri3', '', '', '1.45', '1.87'], ['Ri4', '', '', '6.42', '8.26'], ['Ri5', '', '', '0.54', '0.7']]

sample_table = Table(samples_data, hAlign='LEFT')
sample_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.blue),
    ('BACKGROUND', (0,0), (0,-1), colors.blue),

    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
    ('TEXTCOLOR',(0,0),(0,-1),colors.whitesmoke)

]))
elements.append(sample_table)




doc.build(elements)




# Define line properties (adjust start/end points and stroke color as needed)
# line_color = "#000000"  # Black color
# line_start_x = inch * 2.2  # Adjust X-coordinate
# line_start_y = topMargin + 1.8 * cm  # Adjust Y-coordinate
# line_end_x = inch * 7.8  # Adjust X-coordinate
# line_end_y = topMargin + 1.8 * cm  # Adjust Y-coordinate (same as start for a horizontal line)

# horizontal_line = Line(line_start_x, line_start_y, line_end_x, line_end_y,
#                         strokeColor=line_color, strokeWidth=1)


# # # Add the line to the elements list
# elements.append(horizontal_line)


# Build the PDF
