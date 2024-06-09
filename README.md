# Data Processing Project

## Overview
This project demonstrates how to fetch messages from an AWS SQS queue, process them by masking personally identifiable information (PII), and store the processed data in a PostgreSQL database. The project uses Docker to run both LocalStack (a fully functional local AWS cloud stack) and PostgreSQL.

## Prerequisites
Before you begin, ensure you have the following installed on your machine:

Docker
Docker Compose
Python 3.6+ (with pip)

## Project Structure

docker-compose.yml: Defines the Docker services for LocalStack and PostgreSQL.
main.py: The main script that fetches messages from the SQS queue, processes them, and inserts the data into the PostgreSQL database

Step 1: Set Up Docker Containers
1. Create a docker-compose.yml 
2. Run docker-compose up to start the Docker containers in detached mode.

Step 2: Run the Python Script
1. Install the required Python packages by running pip install -r requirements.txt
2. Run python main.py to execute the script.

Step 3: Verify the Result as Expected

Open a New Terminal and Run the Command:
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue

Result: This command will retrieve and display the original data received from the AWS SQS queue in JSON format.

Open a New Terminal and Run the Command:
docker exec -it etl_application-master-postgres-1 psql -U postgres

Result: This command will open an interactive PostgreSQL session within the Docker container named etl_application-master-postgres-1 (this can be different accordig to your postgres image name). 

Connect to the PostgreSQL Database: 
\c postgres
Result: This command will connect you to the postgres database.

List All Tables: 
\dt
Result: This command will list all the tables in the connected database.

Query the user_logins Table:
SELECT * FROM user_logins;

Note: Verify that the table contains all the AWS SQS values with the transformation of Personally Identifiable Information (PII). Try running the process again to add more data to the table. Comapre original data and masked postgres data. 

## Questions

● How would you deploy this application in production? 

To deploy this application in production:

- Containerization: Use Docker to containerize the application and its dependencies (Postgres and LocalStack).

- Orchestration: Use Docker Compose or Kubernetes to manage and scale the containers.

- Cloud Services: Deploy the containers to a cloud provider like AWS, Azure, or Google Cloud for reliable hosting and scaling.

● What other components would you want to add to make this production ready?

To make this application production-ready, I would add:

- Logging and Monitoring: Implement logging to track application behavior and monitoring tools to watch performance and health.

- Error Handling: Improve error handling to manage exceptions and retry logic.

- Security: Secure database connections and API endpoints using HTTPS and environment variables for sensitive information.

- Testing: Add unit tests and integration tests to ensure code quality and reliability.

- CI/CD Pipeline: Set up Continuous Integration/Continuous Deployment to automate testing and deployment.


● How can this application scale with a growing dataset.

To scale with a growing dataset:

- Database Optimization: Use indexing and optimized queries to handle large amounts of data efficiently.
- Message Batching: Process multiple messages at once to reduce database load.
- Horizontal Scaling: Use load balancers to distribute the workload across multiple instances of the application.
- Cloud Database: Use managed database services that can scale automatically with demand.

● How can PII be recovered later on?

To recover PII (personally identifiable information):

- Reversible Masking: Instead of using SHA-256, use reversible encryption methods that allow decryption with a key.

- Secure Storage: Store the encryption keys securely, ensuring only authorized users can access them.

● What are the assumptions you made? 

Assumptions made include:

- Message Format: The messages in the SQS queue are in a consistent JSON format.

- Database Schema: The Postgres database has a table named user_logins with the specified columns.

- Environment: Docker and Docker Compose are available for container management.

- PII Handling: Using SHA-256 for masking PII is sufficient for anonymization and compliance with privacy standards.

## How I Would Continue Enhancing This Project?

If I had more time to work on this project, I would take the following steps:

1. Database Schema Changes

Change Data Type of app_version:

Reason: Currently, app_version is stored as an integer, which limits the clarity of version numbers (e.g., storing "230" instead of "2.3.0"). Changing it to a string or varchar allows storing version numbers in a more readable format.

Action: Modify the database schema to change app_version from int to varchar.

2. Persistent Data Storage

Include Volume in Docker-Compose:

Reason: Volumes enable persistent data storage, ensuring data is not lost when the container is restarted.

Action: Update the docker-compose.yml file to include volumes for persistent data storage.

3. Deployment and Orchestration

CI/CD Pipeline:

Reason: Automating testing, building, and deployment processes ensures that changes are reliably tested and deployed, reducing manual effort and errors.

Action: Implement a CI/CD pipeline using a tool like GitHub Actions, Jenkins, or GitLab CI.

Kubernetes:

Reason: Kubernetes helps manage container orchestration, including scaling, load balancing, and failover, which is essential for handling increased traffic and ensuring high availability.

Action: Deploy the application to a Kubernetes cluster, defining services, deployments, and other resources.

4. Testing and Quality Assurance

Unit Tests: Write unit tests for individual functions using a testing framework like pytest.

Integration Tests: Develop integration tests to ensure the entire data pipeline works as expected.

Continuous Integration: Set up a CI pipeline to run tests automatically on code commits, ensuring code quality and preventing regressions.
