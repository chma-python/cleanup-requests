# cleanup-requests
- Deletes the "Message" and "First Name" fields and the Twilio recording for any message with the status "Request Complete" in the Intake(?) AirTable.
- Runs every hour on the hour via Heroku Scheduler.
- Can be easily expanded to delete more data (in the same tables or others)
- Can also be duplicated for new cleaning purposes
