# aws app

#
Image processing application: allow user to add image and store it in s3, store image metadata in rds (sql table)
Adding image code adds an event to sqs that will be read by labmda and sent as a notification to subscribers using sns.

There are additional scripts for use with: cloudformation, ec2 userdata, labmdas and aws ci-cd.
Additional files for deployment needs: gunicorn (linux autoloader) and nginx configurations files.

Application can also return aws region and availability zone

#

ui by default at every page if available

?json request param for json responses

?quantity=,start_position= for /images if needed

/metadata - for each image available - data without picture

s3 name for userdata script 'aliaksandr-bulhak-for-ec2', can be changed in init server script

'deploy' folder - for s3 - scripts/deploy_preparer.py to create if not created

'scripts/init_server.txt' - ec2 user data script on launch

/email/subscription - backend only - post/delete as body param : {"email":"aliaksandr_bulhak@email.com"}
