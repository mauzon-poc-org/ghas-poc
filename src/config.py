import boto3

# Configuração AWS - NÃO COMMITAR EM PRODUÇÃO
AWS_ACCESS_KEY_ID = "AKIAI44QH8DHBEXAMPLE"  
AWS_SECRET_ACCESS_KEY = "je7MtGbClwBF/2Wf/2EXAMPLE/bPxRfiCY"
AWS_REGION = "us-east-1"

# Stripe
STRIPE_SECRET_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"

# GitHub token
GITHUB_TOKEN = "ghp_R2D2C3P0xK8mZ4nQ7vL1wJ9bF5tY6uE0sA"

def get_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
