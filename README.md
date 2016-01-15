# TwitterSnake
Repository for those interested in a python-based twitter stream collector hosted on your personal AWS account.

####Blogs on Twitter API
* [Collecting real-time Twitter data with the Streaming API](http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/)

* [An Introduction to Text Mining using Twitter Streaming API and Python](http://adilmoujahid.com/posts/2014/07/twitter-analytics/)
* [Consuming Twitter’s Streaming API using Python and cURL](http://www.arngarden.com/2012/11/07/consuming-twitters-streaming-api-using-python-and-curl/)

####Official Guides on AWS CLI
* [Getting Set Up with the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html)

####Official Guides on Twitter Streaming API
* [Streaming API request parameters](https://dev.twitter.com/streaming/overview/request-parameters)
* [Streaming message types](https://dev.twitter.com/streaming/overview/messages-types#public_stream_messages)
* [Tweets Field Guide](https://dev.twitter.com/overview/api/tweets)

  

##What you'll need to get started:
  1. AWS Account
  2. Twitter Account
  3. Twitter API Keys
  4. Putty (or any SSH client, but this guide uses Putty)
  
##Instructions
### :boom: :exclamation: WARNING: Unless you are on AWS "Free-Tier", continuing with this guide **WILL** cause AWS to bill you for the services you use :exclamation: :boom: 

####Set up your AWS Environment through the AWS Management Console
First things first, we need to set up the environment that will be used to host this application. 

To get started, we need to spin up an EC2 (Elastic Cloud Compute) instance. We will be using an Ubuntu image pre-loaded with Anaconda, which you can read about [here](http://docs.continuum.io/anaconda/images#id4). You can follow these steps or, for a more detailed explanation, follow [this guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html?console_help=true)...
  1. Access your AWS Management Console [here](https://console.aws.amazon.com/console/home?region=us-east-1)
      * Make sure you log in!
  2. Select **EC2** from the **Compute** section
  3. Select **Launch Instance**
  4. From the left-hand navigation pane, select **Community AMIs**
  5. Using the search bar, search for *anaconda* and select Anaconda on Ubuntu from continuum analytics.
      * It should be named similarly to *anaconda3-2.4.1-on-ubuntu-14.04-lts - ami-1cd89176* 
  6. Select the **t1.micro** instance type
  7. [OPTIONAL] From the top navigation bar, select **"6.Configure Security Group"**
  8. [OPTIONAL] In the security specifications, locate the *Source* column and change the selection to **My IP**
  9. Launch your new instance!
  10. - [ ] :exclamation: TODO://Create security group and open necesarry ports, then attach to EC2 instance :exclamation: 
  
Now, we will create the S3 (Simple Storage Solution) bucket to store our collected tweets. You'll need to navigate back to your Management Console [here](https://console.aws.amazon.com/console/home?region=us-east-1).
  1. Select **S3** from the **Storage & Content Deliver** section
  2. Select **Create Bucket**
  3. Name your bucket something fun (and useful)
  4. Select your region (to optimize for latency)
  5. [OPTIONAL] Set up logging. You won't really need this for the purpose of this guide.
  6. Create your bucket!
  
Finally, we need to create an IAM (Identity & Access Management) User so your python program can access your AWS resources. As usual, you'll need to navigate back to your Management Console [here](https://console.aws.amazon.com/console/home?region=us-east-1).
  1. Select **Identity & Access Management** from the **Security and Identity** section
  2. Select **Users** from the left-hand navigation pane
  3. Select **Create New Users**
  4. Name your user something useful (and fun)
  5. Make sure to check the box for the option to **Generate an Access Key for each user**
  6. Select **Create**
  7. Make sure to **download your credentials** from this page and save them somewhere you'll remember... you'll need these later
  8. Now select **close** to close the page (you have to press the button twice)
  9. Now that your back to your **Users** window, select the user you just created by clicking on the name
  10. Select the **Permissions** tab
  11. Select **Attach Policy**
  12. The only resource we will need to access is your S3 bucket, so search for the **AmazonS3FullAccess** policy and **attach it**
  13. You're done!

- [ ]  :exclamation: TODO:// Set up putty to SSH into EC2 instance :exclamation: 
- [ ]  :exclamation: TODO:// Set up your anaconda envinronment :exclamation: 
- [ ]  :exclamation: TODO:// Set up AWS CLI on EC2 instance :exclamation: 
- [ ]  :exclamation: TODO:// Create python files :exclamation: 
- [ ]  :exclamation: TODO:// Explain running with nohup and how to kill if necesarry :exclamation: 
