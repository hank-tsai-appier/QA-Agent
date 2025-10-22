[1] (api) Make a GET request to the Woopra track/ce API endpoint to insert or update user data. The API call is: `https://www.woopra.com/track/ce?project=aiquasdk.prd.com&event=update/insert_any_object&cv_user_id=u0091&cv_name=hank&cv_phone=U53297d8d527739ce4e80cbe200a55478&cv_email=hank@email.abc.com`
[2] (api) Log the HTTP status code returned from the Woopra track/ce API call using `logger.info`.
[3] (ui) Navigate to the AIRIS login page: `https://airis.appier.com`.
[4] (ui) Fill the username field with `qa.test@appier.com` and the password field with `aaAA1234`, then click the login button.
[5] (ui) Navigate directly to the AIRIS profile page: `https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc`.
[6] (ui) Click the three-dot (ellipsis) button located on the right side of the screen to open a dropdown menu.
[7] (ui) From the dropdown menu that appears, click the 'Sync' option.
[8] (ui) In the filter input field, type `Salesforce`.
[9] (ui) Click the 'Sync to Salesforce' button or option that appears after filtering.
[10] (ui) Click the 'Object type' dropdown menu.
[11] (ui) In the filter input field within the 'Object type' dropdown, type `Contact`.
[12] (ui) Click the 'Contact' option from the filtered results in the 'Object type' dropdown and wait for network activity to become idle.
[13] (ui) Click the 'Add Salesforce Field' button three times to create three distinct mapping rows.
[14] (ui) For the first mapping row, open the Salesforce field dropdown, type `Last Name` in the filter, and select `Last Name` from the results.
[15] (ui) For the first mapping row, click the AIRIS field dropdown trigger (identified by an icon like '(X)' or similar, ensuring it's not a delete button) and select `Name` from the options.
[16] (ui) For the second mapping row, open the Salesforce field dropdown, type `Mobile Phone` in the filter, and select `Mobile Phone` from the results.
[17] (ui) For the second mapping row, click the AIRIS field dropdown trigger (identified by an icon like '(X)') and select `phone` from the options.
[18] (ui) For the third mapping row, open the Salesforce field dropdown, type `Email` in the filter, and select `Email` from the results.
[19] (ui) For the third mapping row, click the AIRIS field dropdown trigger (identified by an icon like '(X)') and select `email` from the options.
[20] (ui) Click the 'Export' button to initiate the data synchronization to Salesforce.
[21] (ui) Wait for the 'Import complete' message or a similar success notification to appear on the screen, confirming the synchronization has finished.
[22] (api) Make a GET request to the Woopra profiles API endpoint to retrieve the updated profile data. The API call is: `https://www.woopra.com/rest/3.10/profiles?report_id=nxl6ldktnc&project=aiquasdk.prd.com&force=true&update_mapping=true`
[23] (api) Use the Salesforce API (e.g., REST API) to query and retrieve the Contact record that was just synced. Use the email `hank@email.abc.com` or mobile phone `U53297d8d527739ce4e80cbe200a55478` as a lookup key.
[24] (api) Compare the 'name', 'phone', and 'email' data retrieved from the Woopra profile API (Task 22) with the 'Last Name', 'Mobile Phone', and 'Email' fields from the Salesforce Contact API (Task 23) to verify successful synchronization.
