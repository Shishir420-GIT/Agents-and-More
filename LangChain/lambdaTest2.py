# import json
# import boto3
# import logging

# # Configure logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# # Initialize Bedrock client
# client_bedrock = boto3.client('bedrock-agent-runtime')  # Adjust this client name if incorrect

# def lambda_handler(event, context):
#     try:
#         query_params = event.get('queryStringParameters')
#         # Ensure 'prompt' key exists in the event
#         user_prompt = query_params.get('prompt', None)
#         if not user_prompt:
#             return {
#                 'statusCode': 400,
#                 'body': json.dumps({'error': 'Missing "prompt" in the request payload.'})
#             }

#         # Log the received prompt
#         logger.info(f"Received prompt: {user_prompt}")

#         # Call AWS Bedrock's retrieve-and-generate API
#         response = client_bedrock.retrieve_and_generate(
#             input={
#                 'text': user_prompt
#             },
#             retrieveAndGenerateConfiguration={
#                 'type': 'KNOWLEDGE_BASE',
#                 'knowledgeBaseConfiguration': {
#                     'knowledgeBaseId': '8FVIIXDAW1',
#                     'modelArn': 'arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3.5-haiku'
#                 }
#             }
#         )

#         # Extract the response text from Bedrock's output
#         generated_text = response.get('output', {}).get('text', None)
#         if not generated_text:
#             logger.error("Failed to retrieve text output from Bedrock response.")
#             return {
#                 'statusCode': 500,
#                 'body': json.dumps({'error': 'Failed to generate response.'})
#             }

#         # Return the generated response
#         return {
#             'statusCode': 200,
#             'body': json.dumps({'response': generated_text})
#         }

#     except Exception as e:
#         logger.error(f"Error in Lambda function: {e}")
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)})
#         }

import json
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Bedrock client
client_bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")  # Adjust this client name if incorrect

def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters')
        # Ensure 'prompt' key exists in the event
        user_prompt = query_params.get('prompt', None)
        if not user_prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "prompt" in the request payload.'})
            }

        # Log the received prompt
        logger.info(f"Received prompt: {user_prompt}")

        # Call AWS Bedrock's retrieve-and-generate API
        response = client_bedrock.retrieve_and_generate(
            input={
                'text': user_prompt
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': '8FVIIXDAW1',
                    'modelArn': 'arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3.5-haiku'
                }
            }
        )

        # Extract the response text from Bedrock's output
        generated_text = response.get('output', {}).get('text', None)
        if not generated_text:
            logger.error("Failed to retrieve text output from Bedrock response.")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to generate response.'})
            }

        # Return the generated response
        return {
            'statusCode': 200,
            'body': json.dumps({'response': generated_text})
        }

    except Exception as e:
        logger.error(f"Error in Lambda function: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# Use the native inference API to send a text message to Anthropic Claude.

import boto3
import json

from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters')
        # Ensure 'prompt' key exists in the event
        user_prompt = query_params.get('prompt', None)
        if not user_prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "prompt" in the request payload.'})
            }
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Set the model ID, e.g., Claude 3 Haiku.
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        # Define the prompt for the model.
        prompt = "Describe the purpose of a 'hello world' program in one line."

        # Format the request payload using the model's native structure.
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)
        response = client.invoke_model(modelId=model_id, body=request)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        generated_text = model_response["content"][0]["text"]

        if not generated_text:
            logger.error("Failed to retrieve text output from Bedrock response.")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to generate response.'})
            }

        # Return the generated response
        return {
            'statusCode': 200,
            'body': json.dumps({'response': generated_text})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
