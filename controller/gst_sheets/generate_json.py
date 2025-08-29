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
            "iamt": round(row['net_iamt'], 2),
            "csamt": 0  # Assuming no cess
        })

    # Now prepare doc_issue part
    # Group invoices and credit notes by 'Type', 'Invoice No.'
    # We'll count documents and list their invoice numbers
    doc_groups = tax_invoice_details_df.groupby(['Type', 'Invoice No.'])

    # We'll aggregate documents per type
    doc_issue_list = []

    # Grouping invoices (INVOICE) and credit notes (CREDIT NOTE)
    for doc_type, group_df in tax_invoice_details_df.groupby('Type'):
        doc_type_upper = doc_type.upper()
        invoice_nos = group_df['Invoice No.'].unique()
        
        docs_detail = []
        for inv_no in invoice_nos:
            docs_detail.append({
                "num": 1,
                "from": inv_no,
                "to": inv_no,
                "totnum": 1,
                "cancel": 0,
                "net_issue": 1
            })
        
        doc_issue_list.append({
            "doc_num": len(invoice_nos),
            "doc_typ": "Invoices for outward supply" if doc_type_upper == "INVOICE" else "Credit Note",
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