from controller.gst_controller import GSTController
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

gst_router = APIRouter()

@gst_router.post("/upload-excels")
async def upload_excels(
   tcs_sales_return: UploadFile = File(...),
    tcs_sales: UploadFile = File(...),
    tax_invoice_details: UploadFile = File(...)
):
    return await GSTController.calculate_gst(
        tcs_sales_return,
        tcs_sales,
        tax_invoice_details
    )
