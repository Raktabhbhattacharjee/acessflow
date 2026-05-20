$BUCKET_NAME = "accessflow-uploads-raktabh-2026"
$REGION = "ap-south-1"

Write-Host "Creating S3 bucket: $BUCKET_NAME in region $REGION"

aws s3 mb "s3://$BUCKET_NAME" --region $REGION

Write-Host "Bucket list:"
aws s3 ls