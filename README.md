 # Introduction
 ```
In this project, The focus is on batch-processing data architecture which will be built on the Azure platform. 

The goal of this project is to use Azure services to design and build a reliable batch-processing data architecture that will be used as the backend of a machine learning application that processes enormous amounts of data.
Creating a scalable, dependable, and maintainable system that can effectively process substantial amounts of data, store it, conduct the necessary preprocessing, and aggregate the data for use in machine learning applications is the main goal.
The primary goal of this project is to construct the required data infrastructure by utilizing Azure DevOps, Azure Databricks, Azure Key Vault, Azure Blob Storage, Azure PostgreSQL, and Azure Network security.
At the conceptual stage, we will focus on integrating canonical software components and frameworks and adapting common data engineering principles to create a state-of-the-art architecture for data processing.
The design will prioritize batch scheduling of data processing tasks to coincide with the frontend application's quarterly execution cycle, which oversees producing new iterations of the machine learning model.
```

![Project Architecture](https://github.com/DadaNanjesha/batch-processing/blob/main/Project%20structure.png)

## Tools used for this entire project:
```
• Azure DevOps
• Azure Repos
• Azure Pipelines
• Azure Portal
• Azure Database for PostgreSQL flexible server
• Azure Databricks Service
• Resource Group
• Network Watcher
• Azure Blob Storage account
• Network security group
• Azure Key Vault
```
## Steps to setup:
```
1. Create Azure subscription
2. Create Azure DevOps account
3. Create the resource group and access provided and follow the Azure documentation
4. Create the required resoucres for the project
5. Create the pipeline in Azure Devops for CI
6. Deploy the CSV data into PostgreSQL
7. Create a DataBricks pipeline to load and transform the given data in Batch.
```
