import pandas as pd

def generate_json(tcs_sales_df, tcs_sales_return_df, tax_invoice_details_df, gstin, fp, version="GST3.1.6"):
    gst_state_codes = {
        "jammu & kashmir": "01", "himachal pradesh": "02", "punjab": "03", "chandigarh": "04",
        "uttarakhand": "05", "haryana": "06", "delhi": "07", "rajasthan": "08",
        "uttar pradesh": "09", "bihar": "10", "sikkim": "11", "arunachal pradesh": "12",
        "nagaland": "13", "manipur": "14", "mizoram": "15", "tripura": "16",
        "meghalaya": "17", "assam": "18", "west bengal": "19", "jharkhand": "20",
        "odisha": "21", "chhattisgarh": "22", "madhya pradesh": "23", "gujarat": "24",
        "dadra and nagar haveli and daman and diu": "26", "maharashtra": "27",
        "andhra pradesh (old)": "28", "karnataka": "29", "goa": "30", "lakshadweep": "31",
        "kerala": "32", "tamil nadu": "33", "puducherry": "34", "andaman and nicobar islands": "35",
        "telangana": "36", "andhra pradesh": "37", "ladakh": "38","puducherry": "34",
    }

    def get_state_code(state):
        if not isinstance(state, str):
            return None
        return gst_state_codes.get(state.strip().lower())

    # Aggregate sales
    sales_grouped = tcs_sales_df.groupby(['gst_rate', 'end_customer_state_new'])[['total_taxable_sale_value', 'tax_amount']].sum().reset_index()
    sales_grouped.rename(columns={'total_taxable_sale_value':'sales_txval', 'tax_amount':'sales_iamt'}, inplace=True)

    # Aggregate returns
    returns_grouped = tcs_sales_return_df.groupby(['gst_rate', 'end_customer_state_new'])[['total_taxable_sale_value', 'tax_amount']].sum().reset_index()
    returns_grouped.rename(columns={'total_taxable_sale_value':'returns_txval', 'tax_amount':'returns_iamt'}, inplace=True)

    # Merge and calculate net taxable value and tax amount
    merged = pd.merge(sales_grouped, returns_grouped, how='left', on=['gst_rate', 'end_customer_state_new'])
    merged['returns_txval'] = merged['returns_txval'].fillna(0)
    merged['returns_iamt'] = merged['returns_iamt'].fillna(0)

    merged['net_txval'] = merged['sales_txval'] - merged['returns_txval']
    merged['net_iamt'] = merged['sales_iamt'] - merged['returns_iamt']

    # Filter out near-zero net values
    merged = merged[merged['net_txval'].abs() > 0.01]

    # Build b2cs list
    b2cs_list = []
    for _, row in merged.iterrows():
        state_code = get_state_code(row['end_customer_state_new'])
        if not state_code:
            continue
        b2cs_list.append({
            "sply_ty": "INTER",
            "rt": int(row['gst_rate']),
            "typ": "OE",
            "pos": state_code,
            "txval": round(row['net_txval'], 2),
            "iamt": round(row['net_txval'] * row['gst_rate'] / 100, 2),
            "csamt": 0  # Assuming no cess
        })

    # Now prepare doc_issue part
    doc_groups = tax_invoice_details_df.groupby(['Type', 'Invoice No.'])

    # We'll aggregate documents per type
    doc_issue_list = []
    total_number = len(tax_invoice_details_df)
    
    import pandas as pd

def generate_json(tcs_sales_df, tcs_sales_return_df, tax_invoice_details_df, gstin, fp, version="GST3.1.6"):
    gst_state_codes = {
        "jammu & kashmir": "01", "himachal pradesh": "02", "punjab": "03", "chandigarh": "04",
        "uttarakhand": "05", "haryana": "06", "delhi": "07", "rajasthan": "08",
        "uttar pradesh": "09", "bihar": "10", "sikkim": "11", "arunachal pradesh": "12",
        "nagaland": "13", "manipur": "14", "mizoram": "15", "tripura": "16",
        "meghalaya": "17", "assam": "18", "west bengal": "19", "jharkhand": "20",
        "odisha": "21", "chhattisgarh": "22", "madhya pradesh": "23", "gujarat": "24",
        "dadra and nagar haveli and daman and diu": "26", "maharashtra": "27",
        "andhra pradesh (old)": "28", "karnataka": "29", "goa": "30", "lakshadweep": "31",
        "kerala": "32", "tamil nadu": "33", "puducherry": "34", "andaman and nicobar islands": "35",
        "telangana": "36", "andhra pradesh": "37", "ladakh": "38","puducherry": "34",
    }

    def get_state_code(state):
        if not isinstance(state, str):
            return None
        return gst_state_codes.get(state.strip().lower())

    # ================== B2CS CALCULATION ==================
    # Aggregate sales
    sales_grouped = tcs_sales_df.groupby(['gst_rate', 'end_customer_state_new'])[['total_taxable_sale_value', 'tax_amount']].sum().reset_index()
    sales_grouped.rename(columns={'total_taxable_sale_value':'sales_txval', 'tax_amount':'sales_iamt'}, inplace=True)

    # Aggregate returns
    returns_grouped = tcs_sales_return_df.groupby(['gst_rate', 'end_customer_state_new'])[['total_taxable_sale_value', 'tax_amount']].sum().reset_index()
    returns_grouped.rename(columns={'total_taxable_sale_value':'returns_txval', 'tax_amount':'returns_iamt'}, inplace=True)

    # Merge and calculate net taxable value and tax amount
    merged = pd.merge(sales_grouped, returns_grouped, how='left', on=['gst_rate', 'end_customer_state_new'])
    merged['returns_txval'] = merged['returns_txval'].fillna(0)
    merged['returns_iamt'] = merged['returns_iamt'].fillna(0)

    merged['net_txval'] = merged['sales_txval'] - merged['returns_txval']
    merged['net_iamt'] = merged['sales_iamt'] - merged['returns_iamt']

    # Filter out near-zero net values
    merged = merged[merged['net_txval'].abs() > 0.01]

    # Build b2cs list
    b2cs_list = []
    for _, row in merged.iterrows():
        state_code = get_state_code(row['end_customer_state_new'])
        if not state_code:
            continue
        b2cs_list.append({
            "sply_ty": "INTER",
            "rt": int(row['gst_rate']),
            "typ": "OE",
            "pos": state_code,
            "txval": round(row['net_txval'], 2),
            "iamt": round(row['net_txval'] * row['gst_rate'] / 100, 2),
            "csamt": 0  # Assuming no cess
        })

    # ================== HSN CALCULATION ==================
    # Ensure returns df has required columns even if empty
    if tcs_sales_return_df.empty:
        tcs_sales_return_df = pd.DataFrame(columns=['hsn_code','quantity','total_taxable_sale_value','total_invoice_value'])

    sales_hsn = tcs_sales_df.groupby(['hsn_code','gst_rate']).agg({
        'quantity':'sum',
        'total_taxable_sale_value':'sum',
        'total_invoice_value':'sum'
    }).reset_index()

    returns_hsn = tcs_sales_return_df.groupby(['hsn_code','gst_rate']).agg({
        'quantity':'sum',
        'total_taxable_sale_value':'sum',
        'total_invoice_value':'sum'
    }).reset_index()

    hsn_merged = pd.merge(sales_hsn, returns_hsn, how='left', on=['hsn_code','gst_rate'], suffixes=('','_r')).fillna(0)

    hsn_merged['net_qty'] = hsn_merged['quantity'] - hsn_merged['quantity_r']
    hsn_merged['net_txval'] = hsn_merged['total_taxable_sale_value'] - hsn_merged['total_taxable_sale_value_r']
    hsn_merged['net_val'] = hsn_merged['total_invoice_value'] - hsn_merged['total_invoice_value_r']

    hsn_merged = hsn_merged[hsn_merged['net_txval'].abs() > 0.01]

    hsn_list = []
    for i, row in hsn_merged.iterrows():
        rt = row['gst_rate']
        txval = row['net_txval']
        igst = round(txval * rt / 100, 2)
        # Here I'm splitting equally between CGST and SGST for intra,
        # you can change logic if you want to differentiate based on place of supply
        cgst = round(igst/2,2)
        sgst = round(igst/2,2)

        hsn_list.append({
            "num": i+1,
            "hsn_sc": str(int(row['hsn_code'])),
            "uqc": "PCS",
            "qty": int(row['net_qty']),
            "rt": rt,
            "txval": round(txval,2),
            "iamt": igst,
            "samt": sgst,
            "camt": cgst,
            "csamt": 0
        })
    
    # ===== Helper: Natural sort for alphanumeric invoice numbers =====
    def sort_key(val):
        import re
        match = re.match(r"([a-zA-Z]+)(\d+)", str(val))
        if match:
            prefix, num = match.groups()
            return (prefix, int(num))
        return (val, 0)
    
     # ===== Document Types to Process =====
    document_types = {
        "INVOICE": "Invoices for outward supply",
        "CREDIT NOTE": "Credit Note"
    }
    doc_issue_list = []
    for doc_type, label in document_types.items():
        filtered_df = tax_invoice_details_df[
            tax_invoice_details_df['Type'].str.upper() == doc_type
        ]

        if filtered_df.empty:
            continue

        invoice_numbers = sorted(
            filtered_df['Invoice No.'].dropna().unique(),
            key=sort_key
        )

        if not invoice_numbers:
            continue

        sr_from = invoice_numbers[0]
        sr_to = invoice_numbers[-1]
        total_count = len(invoice_numbers)

        # no cancelled info available → always 0
        cancelled_count = 0  

        docs_detail = [{
            "num": 1,
            "from": sr_from,
            "to": sr_to,
            "totnum": total_count,
            "cancel": int(cancelled_count),
            "net_issue": total_count - int(cancelled_count)
        }]

        doc_issue_list.append({
            "doc_num": len(doc_issue_list) + 1,
            "doc_typ": label,
            "docs": docs_detail
        })

    # Compose final JSON
    result_json = {
        "gstin": gstin,
        "fp": fp,
        "version": version,
        "hash": "hash",  # Replace with actual hash if needed
        "b2cs": b2cs_list,
        "doc_issue": {
            "doc_det": doc_issue_list
        }
    }

    return result_json