from openpyxl.styles import PatternFill, Font, Alignment
import openpyxl

def generate_docs_sheet(wb, sales_qty, return_qty):
    ws = wb.active
    ws.title = "docs"

    # Styles
    header_fill = PatternFill(start_color='986801', end_color='986801', fill_type='solid')
    blue_fill = PatternFill(start_color='0000FF', end_color='0000FF', fill_type='solid')
    font_white_bold = Font(color='FFFFFF', bold=True)
    align_center = Alignment(horizontal='center', vertical='center')

    ws['A1'] = "Summary of documents issued during the tax period (13)"
    ws.merge_cells('A1:D1')
    ws['A1'].fill = blue_fill
    ws['A1'].font = font_white_bold
    ws['A1'].alignment = align_center

    ws['D2'] = "Total Number"
    ws['E2'] = "Total Cancelled"
    ws['D3'] = sales_qty
    ws['E3'] = return_qty

    headers = ["Nature of Document", "Sr. No. From", "Sr. No. To", "Total Number", "Cancelled"]
    for i, val in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=i, value=val)
        cell.fill = header_fill
        cell.font = font_white_bold
        cell.alignment = align_center

    ws.append(["Invoices for outward supply", "fleup26712", "fleup26824", sales_qty, 0])
    ws.append(["Credit Note", "fleup26C200", "fleup26C241", return_qty, 0])
