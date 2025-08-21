import io
import pandas as pd
from controller.gst_sheets.sheet_docs import generate_docs_sheet
from controller.gst_sheets.sheet_eco import generate_eco_sheet
from fastapi import UploadFile, HTTPException, Response
from typing import Dict
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment

class GSTController:

    @staticmethod
    async def calculate_gst(
        tcs_sales_return: UploadFile,
        tcs_sales: UploadFile,
        tax_invoice_details: UploadFile
    ) -> Dict:

        try:
            # Read files into DataFrames using BytesIO
            tcs_sales_return_bytes = await tcs_sales_return.read()
            tcs_sales_bytes = await tcs_sales.read()
            tax_invoice_details_bytes = await tax_invoice_details.read()

            tcs_sales_return_df = pd.read_excel(io.BytesIO(tcs_sales_return_bytes))
            tcs_sales_df = pd.read_excel(io.BytesIO(tcs_sales_bytes))
            tax_invoice_details_df = pd.read_excel(io.BytesIO(tax_invoice_details_bytes))

            if 'quantity' in tcs_sales_df.columns:
                tcs_sales_df['quantity'] = pd.to_numeric(
                    tcs_sales_df['quantity'].astype(str).str.replace("'", "", regex=False),
                    errors='coerce'  # Converts invalid values to NaN
                ).fillna(0).astype(int)  # Replace NaN with 0 and convert to integer
                # total_quantity_tcs_sales = tcs_sales_df['quantity'].sum()
                total_quantity_tcs_sales = tcs_sales_df['quantity'].sum()
                
                
            else:
                raise HTTPException(status_code=400, detail="'quantity' column not found in tcs_sales.xlsx")
            
            if 'quantity' in tcs_sales_return_df.columns:
                tcs_sales_return_df['quantity'] = pd.to_numeric(
                    tcs_sales_return_df['quantity'].astype(str).str.replace("'", "", regex=False),
                    errors='coerce'  # Converts invalid values to NaN
                ).fillna(0).astype(int)  # Replace NaN with 0 and convert to integer
                total_quantity_tcs_sales_return = tcs_sales_return_df['quantity'].sum()
            else:
                raise HTTPException(status_code=400, detail="'quantity' column not found in tcs_sales_return.xlsx")
            
            total_qty = total_quantity_tcs_sales - total_quantity_tcs_sales_return
            total_qty = int(total_qty)
            
            required_columns = ['total_taxable_sale_value', 'tax_amount', 'taxable_shipping']
            for col in required_columns:
                if col not in tcs_sales_df.columns:
                    raise HTTPException(status_code=400, detail=f"'{col}' column not found in tcs_sales.xlsx")
                tcs_sales_df[col] = pd.to_numeric(
                    tcs_sales_df[col].astype(str).str.replace("'", "", regex=False),
                    errors='coerce'
                ).fillna(0)
                
            if 'total_taxable_sale_value' in tcs_sales_return_df.columns:
                tcs_sales_return_df['total_taxable_sale_value'] = pd.to_numeric(
                    tcs_sales_return_df['total_taxable_sale_value'],
                    errors='coerce'
                ).fillna(0)
                total_taxable_sale_value_return = round(tcs_sales_return_df['total_taxable_sale_value'].sum(),2)
                
            total_taxable_sale_value = round(tcs_sales_df['total_taxable_sale_value'].sum(),2)
            total_tax_amount =  round(tcs_sales_df['tax_amount'].sum(), 2)
            total_taxable_shipping = round(tcs_sales_df['taxable_shipping'].sum(), 2)
            print("1",total_taxable_sale_value)
            print("2",total_tax_amount)
            print("3",total_taxable_shipping)
            print("4",total_taxable_sale_value_return)
            
            wb = openpyxl.Workbook()
            meesho_gst = '09AARCM9332R1CM'
            supplier_name = 'meesho'
            Net_value_of_supplies = round(total_taxable_sale_value - total_taxable_sale_value_return, 2)
            Net_value_of_supplies = int(Net_value_of_supplies)
            generate_eco_sheet(wb, meesho_gst,supplier_name,Net_value_of_supplies)
            generate_docs_sheet(wb, total_quantity_tcs_sales, total_quantity_tcs_sales_return)
            

            # Save the workbook to a BytesIO object
            file_stream = io.BytesIO()
            wb.save(file_stream)
            file_stream.seek(0)

            # Return the Excel file as a response
            return Response(
                content=file_stream.read(),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=tax_document_summary.xlsx"}
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

