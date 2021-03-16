# Recycle-able Image Classification

Recycle-able Image Classification is an image classifier that runs a keras Model on an AWS Lambda in a dockerized container. The keras model is hosted on an AWS S3 bucket, to check if an image is recycleable using a pre-built model by the [Portland State University](http://web.cecs.pdx.edu/~singh/rcyc-web/index.html).

## Requirements

- VS Code
- AWS Toolkit for VS Code
- Docker
- AWS S3
- AWS Elastic Container Repository (ECR)
- AWS Lambda

## Installation

### AWS Toolkit for VS Code

In order to deploy the code, AWS Toolkit is required to help with pulling, pushing and invoking the Lambda function.

### AWS S3

AWS S3 will only be accessed via the Lambda instance. Therefore, for security, disable all public access

Steps:

1. Create bucket using Web GUI and block all public access
2. Upload the .h5 models to the S3 bucket

### AWS Elastic Container Repository (ECR)

AWS ECR is required due to the size of the python packages (tensorflow, keras). After you have pulled the code.

#### Creating ECR (First Time)

```bash
# Build the docker image
docker build -t  lambda-tensorflow-example .
```

```bash
# Create a ECR repository
aws ecr create-repository --repository-name lambda-tensorflow-example --image-scanning-configuration scanOnPush=true --region <REGION>
```

```bash
# Tag the image to match the repository name
docker tag lambda-tensorflow-example:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/lambda-tensorflow-example:latest
```

```bash
# Register docker to ECR
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```

```bash
# Push the image to ECR
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/lambda-tensorflow-example:latest
```

#### Updating ECR

```bash
# Build the docker image
docker build -t  lambda-tensorflow-example .
```

```bash
# Tag the image to match the repository name
docker tag lambda-tensorflow-example:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/lambda-tensorflow-example:latest<NEW_NUMBER>
```

```bash
# Push the image to ECR
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/lambda-tensorflow-example:latest<NEW_NUMBER>
```

### AWS Lambda

1. On the Lambda console, choose Functions.
2. Choose Create function.
3. Select Container image.
4. For Function name, enter a name
5. For Container image URI, enter the earlier created lambda-tensorflow-example repository.
6. Configure the instance to have 1024 MB of space and 3 min timeout.
7. Configure the security group of the Lambda Instance to have S3 Read only access.

## Running the Instance

To run the Lambda function, there are 2 different ways of doing it

1. Web GUI, Invoke with a json object
2. Invoke with AWS Toolkit for VS Code

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "recycle-able-image",
        },
        "object": {
          "key": "2.jpg",
        }
      }
    }
  ]
}
```

From whichever way you are starting the Lambda function, parse in the above object to start the Lambda function. The object/key (2.jpg) is a current photo hosted in the S3 instance.

In the future, the telegraf/core will upload the image to the S3 bucket, before calling on this Lambda Function to run independently till a result is given. As per the keras model, the object return will be in the format of 5 arrays, to determine if it is either any of (in order)

1. Boxes
2. Glass Bottles
3. Soda Cans
4. Crushed Soda Cans
5. Plastic Bottles

## Future

In the future, we plan to have a SageMaker instance that will run independently on its own to upload the .h5 models directly to the S3 bucket. Then, we will have a hook for our Lambda Function to our S3 bucket to tell it that there has been a change in the model name. However, due to many factors like cost, we have decided to not do it now.
