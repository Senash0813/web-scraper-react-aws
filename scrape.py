from selenium import webdriver 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
from urllib.robotparser import RobotFileParser


#for React content
def fetch_react_content(page_name):
    url = f"https://react.dev/learn/{page_name}"
    
    robots_url = "https://react.dev/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    if not rp.can_fetch("*", url): 
        print(f"Scraping is not allowed for {url} as per robots.txt")
        return None
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")

    service = Service('/Users/senash/Downloads/chromedriver/chromedriver') 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3) 

        html_content = driver.page_source 

    except Exception as e:
        print(f"Error loading the page: {e}")
        driver.quit()
        return None

    finally:
        driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.title.string.strip() if soup.title else "No title found"
    source = "react.dev"

    sections = []
    main_section = {
        "heading": title, 
        "content": []
    }

    for div in soup.find_all('div', class_='ps-0'):
        current_subheading = None
        subheading_content = []

        for element in div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'pre', 'code']):
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if current_subheading:
                    main_section["content"].append({
                        "heading": current_subheading,
                        "content": subheading_content
                    })
                current_subheading = element.get_text(strip=True)
                subheading_content = [] 
            else:
                subheading_content.append(element.get_text(strip=True))

        if current_subheading:
            main_section["content"].append({
                "heading": current_subheading,
                "content": subheading_content
            })

    sections.append(main_section)

    data = [{
        "title": title,
        "source": source,
        "url": url,
        "sections": sections
    }]


    json_output = json.dumps(data ,indent=4)
    print(json_output)

    return data



#for AWS Lambda content
def fetch_aws_lambda_content(page_name):
    url = f"https://docs.aws.amazon.com/lambda/latest/dg/{page_name}"
    
    try:
        rp = RobotFileParser()
        rp.set_url("https://aws.amazon.com/robots.txt")
        rp.read()
        
        
        if not rp.can_fetch("*",url):
            print(f"Scraping not allowed for {url}")
            return None
    except Exception as e:
        print(f"Could not fetch robots.txt: {e}")
        print("Proceeding cautiously as no specific rules were found.")


    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")

    service = Service('/Users/senash/Downloads/chromedriver/chromedriver') 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2) 

        html_content = driver.page_source 

    except Exception as e:
        print(f"Error loading the page: {e}")
        driver.quit()
        return None

    finally:
        driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.title.string.strip() if soup.title else "No title found"
    source = "docs.aws.amazon.com"

    sections = []
    current_section = None
    current_subheading = None
    subheading_content = []


    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'pre', 'code']):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if current_subheading: 
                if current_section:
                    current_section["content"].append({
                        "heading": current_subheading,
                        "content": subheading_content
                    })
            current_subheading = element.get_text(strip=True)
            subheading_content = []
            
            if element.name == 'h1':
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "heading": current_subheading,
                    "content": []
                }
        else:
            subheading_content.append(element.get_text(strip=True))

    if current_subheading:
        if current_section:
            current_section["content"].append({
                "heading": current_subheading,
                "content": subheading_content
            })
    if current_section:
        sections.append(current_section)


    data = {
        "title": title,
        "source": source,
        "url": url,
        "sections": sections
    }

    json_output = json.dumps(data, indent=4)
    print(json_output)

    return data


#to write into JSON
#def write_to_json_file(data, output_file="content.json"):
    try:
        with open(output_file, 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open(output_file, 'w') as f:
        json.dump(existing_data, f, indent=4)

    print(f"Data written to {output_file}")


def main():
    page_names_react = [
        "installation",
        "start-a-new-react-project",
        "add-react-to-an-existing-project",
        "editor-setup",
        "typescript",
        "react-developer-tools",
        "react-compiler",
        "describing-the-ui",
        "your-first-component",
        "importing-and-exporting-components",
        "writing-markup-with-jsx",
        "javascript-in-jsx-with-curly-braces",
        "passing-props-to-a-component",
        "conditional-rendering",
        "rendering-lists",
        "keeping-components-pure",
        "understanding-your-ui-as-a-tree",
        "adding-interactivity",
        "responding-to-events",
        "state-a-components-memory",
        "render-and-commit",
        "state-as-a-snapshot",
        "queueing-a-series-of-state-updates",
        "updating-objects-in-state",
        "updating-arrays-in-state",
        "managing-state",
        "reacting-to-input-with-state",
        "choosing-the-state-structure",
        "sharing-state-between-components",
        "preserving-and-resetting-state",
        "extracting-state-logic-into-a-reducer",
        "passing-data-deeply-with-context",
        "scaling-up-with-reducer-and-context",
        "escape-hatches",
        "referencing-values-with-refs",
        "manipulating-the-dom-with-refs",
        "synchronizing-with-effects",
        "you-might-not-need-an-effect",
        "lifecycle-of-reactive-effects",
        "separating-events-from-effects",
        "removing-effect-dependencies",
        "reusing-logic-with-custom-hooks"
    ]

    page_names_aws = [
        "welcome.html",
        "example-apps.html",
        "file-processing-app.html",
        "scheduled-task-app.html",
        "lambda-typescript.html",
        "typescript-handler.html",
        "typescript-package.html",
        "typescript-image.html",
        "typescript-layers.html",
        "typescript-context.html",
        "typescript-logging.html",
        "typescript-tracing.html",
        "lambda-services.html",
        "with-kafka.html",
        "with-kafka-configure.html",
        "with-kafka-process.html",
        "with-kafka-filtering.html",
        "with-kafka-on-failure.html",
        "with-kafka-troubleshoot.html",
        "services-apigateway.html",
        "services-apigateway-tutorial.html",
        "services-apigateway-errors.html",
        "apig-http-invoke-decision.html",
        "services-appcomposer.html",
        "services-cloudformation.html",
        "with-documentdb.html",
        "with-documentdb-tutorial.html",
        "with-ddb.html",
        "services-dynamodb-eventsourcemapping.html",
        "services-ddb-batchfailurereporting.html",
        "services-dynamodb-errors.html",
        "services-ddb-windows.html",
        "services-ddb-params.html",
        "with-ddb-filtering.html",
        "with-ddb-example.html",
        "services-ec2.html",
        "services-alb.html",
        "with-eventbridge-scheduler.html",
        "services-iot.html",
        "with-kinesis.html",
        "services-kinesis-create.html",
        "services-kinesis-batchfailurereporting.html",
        "kinesis-on-failure-destination.html",
        "services-kinesis-windows.html",
        "services-kinesis-parameters.html",
        "with-kinesis-filtering.html",
        "with-kinesis-example.html",
        "with-mq.html",
        "process-mq-messages-with-lambda.html",
        "services-mq-params.html",
        "with-mq-filtering.html",
        "services-mq-errors.html",
        "with-msk.html",
        "with-msk-configure.html",
        "with-msk-process.html",
        "with-msk-filtering.html",
        "with-msk-on-failure.html",
        "services-msk-tutorial.html",
        "services-rds.html",
        "with-s3.html",
        "with-s3-example.html",
        "with-s3-tutorial.html",
        "with-sqs.html",
        "services-sqs-configure.html",
        "services-sqs-scaling.html",
        "services-sqs-errorhandling.html",
        "services-sqs-parameters.html",
        "with-sqs-filtering.html",
        "with-sqs-example.html",
        "with-sqs-cross-account-example.html",
        "services-s3-batch.html",
        "with-sns.html",
        "with-sns-example.html",
        "service_code_examples.html",
        "service_code_examples_basics.html",
        "example_lambda_Hello_section.html",
        "example_lambda_Scenario_GettingStartedFunctions_section.html",
        "service_code_examples_actions.html",
        "example_lambda_CreateAlias_section.html",
        "example_lambda_CreateFunction_section.html",
        "example_lambda_DeleteAlias_section.html",
        "example_lambda_DeleteFunction_section.html",
        "example_lambda_DeleteFunctionConcurrency_section.html",
        "example_lambda_DeleteProvisionedConcurrencyConfig_section.html",
        "example_lambda_GetAccountSettings_section.html",
        "example_lambda_GetAlias_section.html",
        "example_lambda_GetFunctionConcurrency_section.html",
        "service_code_examples_scenarios.html",
        "example_cross_CognitoAutoConfirmUser_section.html",
        "example_cross_CognitoAutoMigrateUser_section.html",
        "example_cross_ApiGatewayDataTracker_section.html",
        "example_cross_AuroraRestLendingLibrary_section.html",
        "example_cross_StepFunctionsMessenger_section.html",
        "example_cross_PAM_section.html",
        "example_cross_ApiGatewayWebsocketChat_section.html",
        "example_cross_FSA_section.html",
        "example_cross_LambdaForBrowser_section.html",
        "example_cross_ServerlessS3DataTransformation_section.html",
        "example_cross_LambdaAPIGateway_section.html",
        "example_cross_ServerlessWorkflows_section.html",
        "example_cross_LambdaScheduledEvents_section.html",
        "example_cross_CognitoCustomActivityLog_section.html",
        "example_serverless_connect_RDS_Lambda_section.html",
        "example_serverless_Kinesis_Lambda_section.html",
        "example_serverless_DynamoDB_Lambda_section.html",
        "example_serverless_DocumentDB_Lambda_section.html",
        "example_serverless_MSK_Lambda_section.html",
        "example_serverless_S3_Lambda_section.html",
        "example_serverless_SNS_Lambda_section.html",
        "example_serverless_SQS_Lambda_section.html",
        "example_serverless_Kinesis_Lambda_batch_item_failures_section.html",
        "example_serverless_DynamoDB_Lambda_batch_item_failures_section.html",
        "example_serverless_SQS_Lambda_batch_item_failures_section.html"
    ]

    output_file = "scraped_content.json"

    with open(output_file, 'w') as f:
        f.write("[\n")

    for i, page_name in enumerate(page_names_react):
        react_data = fetch_react_content(page_name)
        if react_data:
            with open(output_file, 'a') as f:
                json.dump(react_data, f, indent=4)
                if i < len(page_names_react) - 1 or page_names_aws:
                    f.write(",\n")
                else:
                    f.write("\n")

 
    for i, page_name in enumerate(page_names_aws):
        aws_data = fetch_aws_lambda_content(page_name)
        if aws_data:
            with open(output_file, 'a') as f:
                json.dump(aws_data, f, indent=4)
                if i < len(page_names_aws) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")


    with open(output_file, 'a') as f:
        f.write("]\n")


if __name__ == "__main__":
    main()