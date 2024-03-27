from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer


def save_results_to_pdf(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []

        # Assuming self.factor_results is updated to include all required details
        factor_header = ["Sample", "Grams", "ML", "Factor", "%Cr", "Known Value", "Bias"]
        self.know_sample_results.append(["Average", "N/A", "N/A", round(self.factor_average, 6), "N/A", "N/A", "N/A"])
        print(f"Factor information :{self.know_sample_results}")
        factor_table = Table([factor_header] + self.know_sample_results, colWidths=[50, 40, 40, 50, 50, 60, 50])
       

        factor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(factor_table)

        elements.append(Spacer(1, 12))
    
        # Define the tested samples table as before, including the spacer
        tested_samples_header = ["Ref ID", "Grams", "ML", "Cal % Cr", "Cal % CR2O3"]
        tested_samples_table = Table([tested_samples_header] + self.tested_samples)
        tested_samples_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('TOPPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(tested_samples_table)

        doc.build(elements)
        print("PDF Saved")