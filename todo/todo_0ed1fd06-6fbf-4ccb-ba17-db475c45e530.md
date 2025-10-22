[1] (api) Make a GET request to Woopra track/ce API to send data for user 'u0091' with specified details. Log the response status code.
[2] (ui) Navigate to https://airis.appier.com and log in with username 'qa.test@appier.com' and password 'aaAA1234'.
[3] (ui) Navigate to the specific profile page: https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc.
[4] (ui) Click the three-dot button on the right side of the screen to open the dropdown menu.
[5] (ui) From the dropdown menu, click the 'Sync' option.
[6] (ui) In the filter input field, type 'Salesforce'.
[7] (ui) Click the 'Sync to Salesforce' button.
[8] (ui) Click the 'Object type' dropdown menu, then type 'Contact' into the filter field.
[9] (ui) Click 'Contact' from the filtered options and wait for network idle to ensure the page is fully loaded.
[10] (ui) Click the 'Add Salesforce Field' button three times to create three mapping rows.
[11] (ui) For the first mapping row: Click the Salesforce field dropdown, type 'Last Name' into the filter, and select 'Last Name'. Then, click the AIRIS field's (X) button, and select 'Name' from the dropdown.
[12] (ui) For the second mapping row: Click the Salesforce field dropdown, type 'Mobile Phone' into the filter, and select 'Mobile Phone'. Then, click the AIRIS field's (X) button, and select 'phone' from the dropdown.
[13] (ui) For the third mapping row: Click the Salesforce field dropdown, type 'Email' into the filter, and select 'Email'. Then, click the AIRIS field's (X) button, and select 'email' from the dropdown.
[14] (ui) Click the 'export' button to start the data export process.
[15] (ui) Wait for the 'Import complete' message to appear on the screen, indicating the export process has finished.
[16] (api) Make a GET request to the Woopra profiles API to retrieve the updated profile data for 'nxl6ldktnc'.
[17] (api) Make an API call to Salesforce to retrieve the content of the relevant Contact record(s) that should have been synced.
[18] (api) Compare the data retrieved from the Woopra profiles API and the Salesforce Contact API to verify successful synchronization.
