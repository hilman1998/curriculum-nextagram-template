import boto3, botocore
from app import app
import braintree

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config["S3_KEY"],
   aws_secret_access_key=app.config["S3_SECRET"]
)

def upload_file_to_s3(file, username, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            app.config.get('S3_BUCKET'),
            "{}/{}".format(username,file.filename), 
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e    

    return "{}/{}".format(username,file.filename)  

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config["SANDBOX_ID"],
        public_key=app.config["SANDBOX_PUBLIC_KEY"],
        private_key=app.config["SANDBOX_PRIVATE_KEY"]
    )
)
