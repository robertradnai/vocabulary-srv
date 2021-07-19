import os

SHARED_WORKBOOKS_PATH = "testdata/shared_collections"
SHARED_WORKBOOKS_METADATA = "testdata/shared_collections_metadata.yml"

SQLALCHEMY_DATABASE_URI = "postgresql://vocabulary_test:vocabulary_test@localhost/vocabulary_test"

SECRET_KEY="NzdkYTNmZGMxNmY2NjNhNDRjYzc4NTU2NTFkNDBiMGFkZWQzYjcwOTc0OGUxMTMy"


AWS_DEFAULT_REGION = 'eu-central-1'
AWS_COGNITO_DOMAIN = 'https://vocabulary-test-local.auth.eu-central-1.amazoncognito.com'  # TODO what is it?
AWS_COGNITO_USER_POOL_ID = "eu-central-1_1Nc1U9zKv"
AWS_COGNITO_USER_POOL_CLIENT_ID = "3lmlqb5mlp21etl4n20lj37j39"
AWS_COGNITO_USER_POOL_CLIENT_SECRET = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_SECRET")
AWS_COGNITO_REDIRECT_URL = 'http://localhost:5000/auth/aws_cognito_redirect'

# https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html?highlight=http#web-app-example-of-oauth-2-web-application-flow
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
