[1] (api) Make a GET request to the Woopra track/ce API to push data: https://www.woopra.com/track/ce?project=aiquasdk.prd.com&event=update/insert_any_object&cv_user_id=u0091&cv_name=hank&cv_phone=U53297d8d527739ce4e80cbe200a55478&cv_email=hank@email.abc.com
[2] (api) Log the status code of the Woopra track/ce API response using `logger.info`.
[3] (ui) Navigate to https://airis.appier.com and log in with username 'qa.test@appier.com' and password 'aaAA1234'.
[4] (ui) Navigate to the profile page: https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc
[5] (ui) Click the three-dot button on the right side of the screen.
[6] (ui) From the dropdown menu, click 'Sync'.
[7] (ui) In the filter input field, type 'Salesforce'.
[8] (ui) Click the 'sync to Salesforce' option/button.
[9] (ui) Click the 'Object type' dropdown, then in the filter input field, type 'Contact'.
[10] (ui) Click the 'Contact' option in the dropdown and wait for network idle.
[11] (ui) Click the 'Add Salesforce Field' button three times to create three mapping fields.
[12] (ui) For the first mapping field, click the Salesforce dropdown, filter for 'Last Name', and click 'Last Name'.
[13] (ui) For the first mapping field, click the AIRIS field's (X) (which opens a dropdown), and click 'Name'.
[14] (ui) For the second mapping field, click the Salesforce dropdown, filter for 'Mobile Phone', and click 'Mobile Phone'.
[15] (ui) For the second mapping field, click the AIRIS field's (X), and click 'phone'.
[16] (ui) For the third mapping field, click the Salesforce dropdown, filter for 'Email', and click 'Email'.
[17] (ui) For the third mapping field, click the AIRIS field's (X), and click 'email'.
[18] (ui) Click the 'export' button.
[19] (ui) Wait for the 'import complete' message to appear on the screen.
[20] (api) Make an API call to Woopra to fetch profile data: https://www.woopra.com/rest/3.10/profiles?report_id=nxl6ldktnc&project=aiquasdk.prd.com&force=true&update_mapping=true
[21] (api) Make an API call to Salesforce to retrieve the content of the created/updated Contact. (Note: Specific Salesforce API endpoint and authentication details needed for implementation).
[22] (api) Compare the data retrieved from the Woopra profiles API and the Salesforce Contact API to verify consistency.
