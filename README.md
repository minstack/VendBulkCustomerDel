# VendBulkCustomerDel

To make bulk customer deletes more efficient without the need for the use of (multiple) CSVs, VLOOKUPs and text formatting to manually copy paste to backend.

This will delete the provided customers provided that they are not attached to any open (layby or on-account sales).  If they cannot be deleted because of the previous reason, those customers will be exported into a list (customer_code only) as well as all the open sales (invoice #). These exports will be separate files.

Currently, it has been tested and increased to include 8 threads (just much faster) but have not been tested on large amount of customers to delete. This must be monitored to see if that may be too many threads to run. If that is the case, I will update with possibly 4-6 threads in total.


# Platform
Currently macOS only, however, the Windows binary can be compiled easily if needed.


# Setup
Download the VendBulkCustomerDel.app file and double click to run.


# Steps
    1. Run app
    2. Input the store prefix and copy/paste token (expiry set)
    3. Add as many CSVs provided by the retailer (since customer export will split into 1000 lines per CSV)
    4. Complete (select) checklist items
    5. Press Delete Customers to run
