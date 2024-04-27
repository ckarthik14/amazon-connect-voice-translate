def lambda_handler(event, context):
    client = boto3.client('apigatewaymanagementapi', endpoint_url="https://qv1241nc27.execute-api.us-east-1.amazonaws.com/dev/")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('WebSocketConnections')
    response = table.scan()

    for record in event['Records']:
        # Decode the base64 encoded string
        encoded_data = record['kinesis']['data']
        decoded_data = b64decode(encoded_data)
        # Convert JSON string to Python dictionary
        data = json.loads(decoded_data)

        for item in response['Items']:
            connection_id = item['connectionId']
            try:
                # Send decoded audio data (assume 'audio_data' is a key in the data dictionary)
                client.post_to_connection(ConnectionId=connection_id, Data=json.dumps({'audio_data': data['audio_data']}))
            except client.exceptions.GoneException:
                # Delete item from DynamoDB if connection is gone
                table.delete_item(Key={'connectionId': connection_id})
            except Exception as e:
                # Log other exceptions
                print(f"Error posting to connection {connection_id}: {str(e)}")

    return {'statusCode': 200}