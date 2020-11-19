### Delete AMI Backups with related snapshots older than specified days
#### AWS Lambda function

Delete AMI backups woth related snapshots older than specified days.  
Run at desired schedule through CloudWatch rules. 

### Requirements
Lambda function will need IAM role with following policies  
	- arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole  
	- EC2 policy for AMI removal  
Please set your environment variable for desired days.  
 [Env Vars](/img.png)

### Output
```shell
Sample output:  
Deleting ami-023f8b3d457ec7c0f 
Deleting snap-0e489caca1ae6eeb9 
Deleting ami-02da60454a7716f38 
Deleting snap-0c59f5f35523ddc88 
Deleting snap-0ab7deb52f49dfcb0 
Deleting ami-032f04c94e709382c 
Deleting snap-0efd023e6000e4a03 
Deleting ami-0cbfe2d5463302b5f 
Deleting snap-07d1570378373de96 
Deleting snap-0188236075c3c792f 
Deleting snap-07492204fe316466d 
Deleting ami-0cd2355e997952c9c 
Deleting snap-011ef714fe72a2059 
```
