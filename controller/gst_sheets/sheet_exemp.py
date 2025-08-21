from openpyxl.styles import PatternFill, Font, Alignment

def generate_exemp_sheet(wb, ):
    ws = wb.create_sheet(title="exemp")
    

    # Define styles
    bold_font = Font(bold=True)
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    header_fill = PatternFill(start_color="FFD966", end_color="FFD966", fill_type="solid")  # light yellow

    # Row 1: Title
    ws.merge_cells("A1:D1")
    ws["A1"] = "Summary For Nil rated, exempted and non GST outward supplies (8)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A1"].alignment = center_align

    # Row 2: Headers
    ws["A2"] = ""
    ws["B2"] = "Total Nil Rated Supplies"
    ws["C2"] = "Total Exempted Supplies"
    ws["D2"] = "Total Non-GST Supplies"

    for col in ['B2', 'C2', 'D2']:
        ws[col].font = bold_font
        ws[col].alignment = center_align
        ws[col].fill = header_fill

    # Row 3: Zero values
    ws["A3"] = ""
    ws["B3"] = 0.00
    ws["C3"] = 0.00
    ws["D3"] = 0.00

    for col in ['B3', 'C3', 'D3']:
        ws[col].alignment = center_align

    # Row 4: Description header
    ws["A5"] = "Description"
    ws["B5"] = "Nil Rated Supplies"
    ws["C5"] = "Exempted(other than nil rated/non GST supply)"
    ws["D5"] = "Non-GST Supplies"

    for cell in ['A5', 'B5', 'C5', 'D5']:
        ws[cell].font = bold_font
        ws[cell].alignment = center_align
        ws[cell].fill = header_fill

    # Row 5-8: Data Rows
    data = [
        ("Inter-State supplies to registered persons", 0.00, "", ""),
        ("Intra-State supplies to registered persons", 0.00, "", ""),
        ("Inter-State supplies to unregistered persons", 7080.00, "", ""),
        ("Intra-State supplies to unregistered persons", 4269.00, "", "")
    ]

    start_row = 6
    for idx, (desc, nil_rate, exempted, non_gst) in enumerate(data):
        ws[f"A{start_row + idx}"] = desc
        ws[f"B{start_row + idx}"] = nil_rate
        ws[f"C{start_row + idx}"] = exempted
        ws[f"D{start_row + idx}"] = non_gst

        for col in ['A', 'B', 'C', 'D']:
            ws[f"{col}{start_row + idx}"].alignment = center_align

    return wb