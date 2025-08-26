from openpyxl.styles import PatternFill, Font, Alignment
import pandas as pd

def generate_hsn_sheet(wb, tcs_sales_return_df, tcs_sales_df, tax_invoice_details_df):
    ws = wb.create_sheet(title="hsn(b2c)")

    # ========== STYLING ==========
    blue_fill = PatternFill(start_color='0000FF', end_color='0000FF', fill_type='solid')
    peach_fill = PatternFill(start_color='FBE4D5', end_color='FBE4D5', fill_type='solid')
    font_white_bold = Font(color='FFFFFF', bold=True)
    font_bold = Font(bold=True)
    align_center = Alignment(horizontal='center', vertical='center')

    # ========== CLEAN AND PREPARE DATA ==========
    cols_to_clean = ['quantity', 'total_taxable_sale_value', 'total_invoice_value', 'gst_rate']
    for col in cols_to_clean:
        if col in tcs_sales_df.columns:
            tcs_sales_df[col] = pd.to_numeric(
                tcs_sales_df[col].astype(str).str.replace("'", "", regex=False),
                errors='coerce'
            ).fillna(0)
        
        if col in tcs_sales_return_df.columns:
            tcs_sales_return_df[col] = pd.to_numeric(
                tcs_sales_return_df[col].astype(str).str.replace("'", "", regex=False),
                errors='coerce'
            ).fillna(0)
            
    # ========== GROUP SALES AND RETURNS SEPARATELY ==========
    sales_grouped = tcs_sales_df.groupby('hsn_code').agg({
        'quantity': 'sum',
        'total_taxable_sale_value': 'sum',
        'total_invoice_value': 'sum',
        'gst_rate': 'first'
    }).reset_index()

    returns_grouped = tcs_sales_return_df.groupby('hsn_code').agg({
        'quantity': 'sum',
        'total_taxable_sale_value': 'sum',
        'total_invoice_value': 'sum'
    }).reset_index()

    # ========== MERGE SALES AND RETURNS TO COMPUTE NETS ==========
    hsn_grouped = pd.merge(
        sales_grouped,
        returns_grouped,
        on='hsn_code',
        how='left',
        suffixes=('', '_return')
    ).fillna(0)

    # Compute net values
    hsn_grouped['net_quantity'] = hsn_grouped['quantity'] - hsn_grouped['quantity_return']
    hsn_grouped['net_taxable'] = hsn_grouped['total_taxable_sale_value'] - hsn_grouped['total_taxable_sale_value_return']
    hsn_grouped['net_invoice'] = hsn_grouped['total_invoice_value'] - hsn_grouped['total_invoice_value_return']
    
    # Round
    hsn_grouped['net_taxable'] = hsn_grouped['net_taxable'].round(2)
    hsn_grouped['net_invoice'] = hsn_grouped['net_invoice'].round(2)

    # ========== EXCEL SHEET SETUP ==========

    # Row 1 - Title and Help
    ws['A1'] = "Summary For HSN(12)"
    ws['A1'].fill = blue_fill
    ws['A1'].font = font_white_bold
    ws['A1'].alignment = align_center
    # ws.merge_cells('A1:G1')

    ws['H1'] = "HELP"
    ws['H1'].font = font_bold
    ws['H1'].alignment = align_center

    # Row 2 - Headers for summary
    headers_row2 = ["No. of HSN", "","","", "Total Value", "Total Taxable Value",
                    "Total Integrated Tax", "Total Central Tax", "Total State/UT Tax", "Total Cess"]

    for i, val in enumerate(headers_row2, start=1):
        cell = ws.cell(row=2, column=i, value=val)
        cell.fill = blue_fill
        cell.font = font_white_bold
        cell.alignment = align_center

    # Row 3 - Summary values
    total_value = hsn_grouped['net_invoice'].sum()
    taxable_value = hsn_grouped['net_taxable'].sum()

    ws.append([hsn_grouped.shape[0], "","","", total_value, taxable_value, 0.00, 0.00, 0.00, 0.00])

    # Row 4 - HSN Detail Headers
    headers_row4 = [
        "HSN", "Description", "UQC", "Total Quantity", "Total Value", "Rate",
        "Taxable Value", "Integrated Tax Amount", "Central Tax Amount", "State/UT Tax Amount", "Cess Amount"
    ]

    for i, val in enumerate(headers_row4, start=1):
        cell = ws.cell(row=4, column=i, value=val)
        cell.fill = peach_fill
        cell.font = font_bold
        cell.alignment = align_center

    # Row 5 onwards - HSN Detail Data
    for index, row in hsn_grouped.iterrows():
        ws.append([
            int(row['hsn_code']), "", "PCS-PIECES",
            int(row['net_quantity']),
            row['net_invoice'],
            row['gst_rate'],
            row['net_taxable'],
            0.00, 0.00, 0.00, 0.00
        ])