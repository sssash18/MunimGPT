import streamlit as st
import munim
import time
import base64
import ocr
import json
import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
'''
# MunimGPT
*Your AI friend for seemless **Perks+** approvals*
'''

account_url = "https://hackboxocrstorage.blob.core.windows.net"
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)


if 'first_load' not in st.session_state:
    
    with st.spinner('Initializing...'):
        time.sleep(2)

    # Set the session state to indicate that the app has been loaded
    st.session_state.first_load = False


with st.container():
  '''
  ### Invoice File 
  '''
  invoice = st.file_uploader("Please upload your copy of invoice for item to be reimbursed", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

with st.container():
  '''
  ### Product Images
  '''
  product_images = st.file_uploader("Please upload product images with serial number clearly visible in at least one of them", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

if st.button("Submit", type="primary",use_container_width=True):
  if (invoice is None or product_images is None) : 
    st.error("At least one file is required for both the inputs. Try again.")
    st.stop()
  base64_encoded_data = base64.b64encode(invoice.getvalue()).decode("utf-8")
 
    
  with st.status("Performing checks on the submitted claim", expanded=True) as status:
    st.write("Analyzing the invoice...")
    file_data = invoice.getvalue()
    # Create a blob client using the filename as the blob name
    blob_client = blob_service_client.get_blob_client(container="images", blob=invoice.name)
    # Upload the file to Azure Blob Storage
    try:
      blob_client.upload_blob(file_data)
    except:
      print("image already uploaded.")
    blob_url = f"https://hackboxocrstorage.blob.core.windows.net/images/{invoice.name}"
    print(blob_url)
    imageText = ocr.performOCR(blob_url)
    st.write("Verifying the vendor details...")
    details = munim.analyze(imageText)
    print(details)
    detailsMap = json.loads(details)
    if detailsMap["confidence"] < 0.5 :
      status.update(
        label="Verification of vendor details failed", state="error", expanded=False
      )
      st.stop()
    st.write("Validating the claim with account balance...")
    time.sleep(2)
    with open("artifacts/db.json") as f:
      dbMap = json.load(f)
    if (detailsMap["invoiceAmount"] > dbMap["customers"][0]["balance"] or detailsMap["vendorGST"] != dbMap["vendor"]["GST"] or detailsMap["customerName"] != dbMap["customers"][0]["name"]) :
      print("Invoice is not genuine")
      status.update(
        label="Validation of claim failed", state="error", expanded=False
      )
      st.stop()
    status.update(
        label="Checks complete! Your claim is approved", state="complete", expanded=False
    )
  
  print("Invoice is genuine")
  st.balloons()

  