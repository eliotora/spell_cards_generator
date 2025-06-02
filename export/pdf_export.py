from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def exporter_pdf(data, filename):
    if not data:
        return

    headers = list(data[0].keys())
    rows = [headers] + [[str(item.get(h, '')) for h in headers] for item in data]

    doc = SimpleDocTemplate(filename, pagesize=A4)
    table = Table(rows)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    doc.build([table])
