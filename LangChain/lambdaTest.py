# lambda_arn = "arn:aws:lambda:us-east-2:730335549776:function:shishir-lambda-demo"
# url = "https://jsvucuwrs7.execute-api.us-east-2.amazonaws.com/default/shishir-lambda-demo"

# import requests
# import json

# response = requests.get(url)
# print(response.json())

import json
import boto3

client_bedrock_knowledgebase = boto3.client('bedrock-agent-runtime')

def lambda_handler (event, context):
    query_params = event.get('queryStringParameters')
    user_prompt = query_params.get('prompt', '')
    
    client_knowledgebase = client_bedrock_knowledgebase.retrieve_and_generate(
    input={
        'text': user_prompt
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': '8FVIIXDAW1',
            'modelArn': 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-instant-v1'
        }
    })
    response_kbase_final= client_knowledgebase['output']['text']

    return {
        'statusCode': 200,
        'body': response_kbase_final
    }