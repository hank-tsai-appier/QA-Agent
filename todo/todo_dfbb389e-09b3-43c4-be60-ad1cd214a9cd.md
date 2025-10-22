[1] (api) Send data to Woopra track/ce API using GET method. URL: https://www.woopra.com/track/ce?project=aiquasdk.prd.com&event=update/insert_any_object&cv_user_id=u0091&cv_name=hank&cv_phone=U53297d8d527739ce4e80cbe200a55478&cv_email=hank@email.abc.com
[2] (api) Log the HTTP status code returned from the Woopra track/ce API call using logger.info.
[3] (ui) Navigate to the Airis login page: https://airis.appier.com
[4] (ui) Fill the username field with 'qa.test@appier.com'.
[5] (ui) Fill the password field with 'aaAA1234'.
[6] (ui) Click the login button.
[7] (ui) Navigate to the Airis profile page: https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc
[8] (ui) Click the 'three dots' button on the right side of the screen to open the dropdown menu.
[9] (ui) Click the 'Sync' option in the opened dropdown menu.
[10] (ui) In the filter/search input field within the Sync dialog, type 'Salesforce'.
[11] (ui) Click the 'sync to Salesforce' button/option.
[12] (ui) Click the 'Object type' dropdown menu.
[13] (ui) In the filter/search input field within the 'Object type' dropdown, type 'Contact'.
[14] (ui) Click the 'Contact' option from the filtered list in the dropdown and wait for network to be idle.
[15] (ui) Click the 'Add Salesforce Field' button three times to create three mapping fields.
[16] (ui) For the first mapping field: Click the Salesforce field dropdown, type 'Last Name' in the filter, and then click 'Last Name' from the options.
[17] (ui) For the first mapping field: Click the AIRIS field dropdown (identified by an (X) icon), then click 'Name' from the options.
[18] (ui) For the second mapping field: Click the Salesforce field dropdown, type 'Mobile Phone' in the filter, and then click 'Mobile Phone' from the options.
[19] (ui) For the second mapping field: Click the AIRIS field dropdown (identified by an (X) icon), then click 'phone' from the options.
[20] (ui) For the third mapping field: Click the Salesforce field dropdown, type 'Email' in the filter, and then click 'Email' from the options.
[21] (ui) For the third mapping field: Click the AIRIS field dropdown (identified by an (X) icon), then click 'email' from the options.
[22] (ui) Click the 'export' button to initiate the data sync.
[23] (ui) Wait for the 'import complete' message or indicator to appear on the screen.
[24] (api) Fetch the Woopra profile data using the API: https://www.woopra.com/rest/3.10/profiles?report_id=nxl6ldktnc&project=aiquasdk.prd.com&force=true&update_mapping=true
[25] (api) Retrieve the Salesforce Contact content corresponding to the synced data using the Salesforce API. This will require Salesforce API authentication and querying for the contact with the provided details (e.g., email, name).
[26] (api) Compare the initial data sent via Woopra track/ce API (id 1) with the fetched Woopra profile data (id 24) and the retrieved Salesforce Contact content (id 25) to ensure successful sync and data integrity.
