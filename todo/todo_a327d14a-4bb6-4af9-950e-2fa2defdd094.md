[1] (api) Send GET request to Woopra track/ce API to insert initial data for profile 'nxl6ldktnc'.
[2] (api) Log the HTTP status code returned from the Woopra track/ce API call.
[3] (ui) Navigate to https://airis.appier.com and log in using username 'qa.test@appier.com' and password 'aaAA1234'.
[4] (ui) Navigate to the specific profile URL: https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc.
[5] (ui) Click the three-dots (kebab menu) button located on the right side of the screen to reveal a dropdown menu.
[6] (ui) From the dropdown menu, click the 'Sync' option.
[7] (ui) In the filter input field within the sync dialog, type 'Salesforce'.
[8] (ui) Click the 'Sync to Salesforce' button/option.
[9] (ui) Click the 'Object type' dropdown menu, then type 'Contact' into the filter field that appears.
[10] (ui) Click the 'Contact' option from the filtered list and wait for the network to become idle.
[11] (ui) Click the 'Add Salesforce Field' button three times to create three mapping rows.
[12] (ui) For the first mapping row, click the Salesforce field dropdown, type 'Last Name' into the filter, and select 'Last Name'.
[13] (ui) For the first mapping row, click the AIRIS field dropdown (identified by an icon like '(X)', distinct from a delete button) and select 'Name'.
[14] (ui) For the second mapping row, click the Salesforce field dropdown, type 'Mobile Phone' into the filter, and select 'Mobile Phone'.
[15] (ui) For the second mapping row, click the AIRIS field dropdown and select 'phone'.
[16] (ui) For the third mapping row, click the Salesforce field dropdown, type 'Email' into the filter, and select 'Email'.
[17] (ui) For the third mapping row, click the AIRIS field dropdown and select 'email'.
[18] (ui) Click the 'Export' button to initiate the data synchronization.
[19] (ui) Wait for the 'Import complete' or similar success message to appear on the screen, indicating the sync has finished.
[20] (api) Send GET request to Woopra profiles API to retrieve the updated profile data for 'nxl6ldktnc'.
[21] (api) Use Salesforce API to retrieve the content of the newly created or updated Contact record.
[22] (api) Compare the data retrieved from the Woopra profiles API (step 20) with the data retrieved from the Salesforce Contact API (step 21) to verify successful synchronization.
