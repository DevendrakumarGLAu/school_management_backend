from openpyxl.styles import PatternFill, Font, Alignment

def generate_b2cs_sheet(wb):
    ws = wb.create_sheet(title="b2cs")

    # === Styles ===
    blue_fill = PatternFill(start_color='0000FF', end_color='0000FF', fill_type='solid')
    peach_fill = PatternFill(start_color='FBE4D5', end_color='FBE4D5', fill_type='solid')
    font_white_bold = Font(color='FFFFFF', bold=True)
    font_bold = Font(bold=True)
    align_center = Alignment(horizontal='center', vertical='center')

    # === Row 1: Title and HELP ===
    ws['A1'] = "Summary For B2CS(7)"
    ws.merge_cells('A1:F1')
    ws['A1'].fill = blue_fill
    ws['A1'].font = font_white_bold
    ws['A1'].alignment = align_center

    ws['G1'] = "HELP"
    ws['G1'].font = font_bold
    ws['G1'].alignment = align_center

    # === Row 2: Summary Headers ===
    ws['D2'] = "Total Taxable  Value"
    ws['F2'] = "Total Cess"
    ws['D2'].fill = blue_fill
    ws['D2'].font = font_white_bold
    ws['D2'].alignment = align_center
    ws['F2'].fill = blue_fill
    ws['F2'].font = font_white_bold
    ws['F2'].alignment = align_center

    # === Row 3: Summary Values (Zeros) ===
    ws['D3'] = 0.00
    ws['F3'] = 0.00

    # === Row 4: Table Headers ===
    headers = [
        "Type", "Place Of Supply", "Applicable % of Tax Rate", "Rate",
        "Taxable Value", "Cess Amount", "E-Commerce GSTIN"
    ]
    for i, val in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=i, value=val)
        cell.fill = peach_fill
        cell.font = font_bold
        cell.alignment = align_center

    # Optional: Adjust column widths for clarity
    widths = [12, 22, 25, 10, 18, 15, 25]
    for i, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = width
