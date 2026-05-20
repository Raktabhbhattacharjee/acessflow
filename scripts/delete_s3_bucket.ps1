$BUCKET_NAME = "accessflow-uploads-raktabh-2026"

Write-Host "Deleting all objects from bucket: $BUCKET_NAME"

aws s3 rm "s3://$BUCKET_NAME" --recursive

Write-Host "Deleting bucket: $BUCKET_NAME"

aws s3 rb "s3://$BUCKET_NAME"

Write-Host "Remaining buckets:"
aws s3 ls