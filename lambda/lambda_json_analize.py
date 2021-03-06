event = {"Records": [{"eventVersion": "2.1",
                            "eventSource": "aws:s3",
                            "awsRegion": "eu-central-1",
                            "eventTime": "2021-12-02T20:33:24.815Z",
                            "eventName": "ObjectRemoved:Delete",
                            "userIdentity": {"principalId": "AWS:AIDAQ72ZB364ZKLAZCXDJ"},
                            "requestParameters": {"sourceIPAddress": "89.64.85.125"},
                            "responseElements": {"x-amz-request-id": "QX2V9YPG8NA2R5XM",
                                                 "x-amz-id-2": "cCG54J9lrxiiFKiBB+W3UFxDyxALKZWCJ+JrfLlzTqT5GEiAlzB/kNc4KQq0q9OsxER1wj5D84ZY1SlYhQ6ZTfp19kg7CoG/"},
                            "s3": {"s3SchemaVersion": "1.0", "configurationId": "lambda_ses",
                                   "bucket": {"name": "big-mac-index",
                                              "ownerIdentity": {"principalId": "A25JQAR6OF05L5"},
                                              "arn": "arn:aws:s3:::big-mac-index"},
                                   "object": {"key": "bic-mac-index-RUS.json", "sequencer": "0061A92D94CA934975"}}}]}


action = event["Records"][0].get("eventName", None)
ip = event["Records"][0].get("requestParameters", {}).get("sourceIPAddress", None)
bucket_name = event["Records"][0].get("s3", {}).get("bucket", {}).get("name", None)
object = event["Records"][0].get("s3", {}).get("object", {}).get("key", None)


print(f"action = {action}, ip = {ip} bucket_name = {bucket_name}, object = {object}")