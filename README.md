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
  7. Select the **Review and Launch** button
  8. On this screen, you'll see a warning about improving your instance's security; ignore this for now. 
  9. Select the **Launch** button. You've created your instance!
  10. From the main EC2 management page, find the **Network & Security** section, and select **Security Groups**
  11. Select **Create new security group**
  12. Name your security group something meaningful, add a description (if you want), and leave the VPC as it defaults
  13. In the **Inbound** tab, select **Add Rule**
  14. For the type, select **HTTP**
  15. Select **Add a rule** again, and select **SSH** as the type
  16. For the source, select **My IP** if you only want to allow connection from your current IP address, or enter a custom IP address (that you have access too, obviously)
  17. Select the **Outbound** tab
  18. You'll notice **All traffic** already added; this is okay, leave it.
  19. Select **Add a rule**, then select **HTTPS** as the type. 
      * This is required so that your EC2 instance can communicate using AWS CLI
  20. Select **Create**
  21. Now your done! Your EC2 instance is spun up and ready to go!
  
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

####FOR WINDOWS: Set up putty in order to SSH into EC2 instance
  In order to connect to your EC2 instance from a windows system, please follow [this guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html)
  
  * Mac or Linux users have a native SSH client.  Get to your command line and enter:
  
 ```python
  ssh
  ```
  If your computer does NOT recognize the command, you need to download Putty or some SSH client.  If your computer recognized the command, you should see something like this (from Mac):
  ```python
  usage: ssh [-1246AaCfGgKkMNnqsTtVvXxYy] [-b bind_address] [-c cipher_spec]
           [-D [bind_address:]port] [-E log_file] [-e escape_char]
           [-F configfile] [-I pkcs11] [-i identity_file]
           [-L [bind_address:]port:host:hostport] [-l login_name] [-m mac_spec]
           [-O ctl_cmd] [-o option] [-p port]
           [-Q cipher | cipher-auth | mac | kex | key]
           [-R [bind_address:]port:host:hostport] [-S ctl_path] [-W host:port]
           [-w local_tun[:remote_tun]] [user@]hostname [command]
    ```
    
####FOR UNIX (MAC or LINUX): SSH into your EC2 instance from the Terminal command line
  In order to connect to your EC2 instance from a UNIX system, please follow [this guide](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)
	
####Set up your Conda envinronment
   Once you're inside of your EC2 instance, you'll be in control of a simple Ubuntu machine with Anaconda pre-installed. Through these instructions, you'll be able to develop a simple python program to connect to the twitter streaming api. You can read about using Conda [here](http://conda.pydata.org/docs/using/index.html)
   1. Run the command **conda create --name `<name of your environment>`**
   2. Run the command __source activate `<name of your environment>`__
   3. Now that you're in your environment, you can install some packages that Anaconda does not include
   4. Run the command **pip install boto3**
   5. Run the command **pip install awscli**
   6. Run the command **pip install botocore**
   7. Run the command **pip install tweepy**
   8. Now, you should have all of the packages that you need in your conda environment

####Configure up AWS CLI on EC2 instance
  You should configure AWS CLI in this environment in case you want to manage your AWS resources from here; you also need to in order to use the boto3 from a python script. You can read about configuring AWS CLI [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), but I'll provide a simple guide as well to get you up and running.
  1. From the command line, execute **aws configure**
  2. Remember those credentials you downloaded in step 7 of setting up your IAM user? You need those now! Find the file and open it
  3. Enter the access key and secret key which are provided in your IAM user credential file, and then type in your default region name (us-east-1, for example)
  4. You don't need to enter anything for Default Output Format, juts hit **Enter**
  5. Your AWS CLI is now configured!

#### Install git on your EC2 Insance
  With AWS CLI configured, and EC2 ready to go, you need to clone this repository to your instance. But first, we need *git* on our instance. We follow the [steps from this page](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-14-04):  
  ```python
  sudo apt-get update
  # Wait for this process to finish
  
  sudo apt-get install git
  # Wait for process to finish
  
  git clone https://github.com/Knowa42/TwitterSnake.git
  
  # Switch to the correct directory
  cd TwitterSnake
  ```  
  
  We're almost ready to pull Twitter data.  We cover more administrative tasks below:  
  
####Create python files
  For simplicity's sake, you can simply fetch **TwitFarm.py** from this repository, and it should be able to run in the environment that you have defined (with the changes defined below). Of course, you can always make your own, better program using the resources you've collected and installed on this EC2 instance. You're ready to do whatever you want! (with python, tweepy, and AWS at least). 
  * To run TwitFarm.py, you need to make the following changed before running it.
  * You need to add in your own Twitter API consumer and access keys in the following section. You'll find these in your twitter developer profile.
  * To add your credentials, in your prompt type:
  ```python
  vim TwitFarm.py
  ```
  If you need a refresher or introduction to Vim commands, [visit this page for instructions](https://www.fprintf.net/vimCheatSheet.html).  When you have the file open, make sure to enter your credentials in this section: 
  
  ```python
  #Write the access tokens and consumer tokens from your Twitter Appliation in these fields
  access_token = ""
  access_token_secret = ""
  consumer_key = ""
  consumer_secret = ""
  ```
  * In the following code section, change the second argument of `self.s3.meta.client.upload_file(self.fileName,'',self.fileName)` to your own S3 bucket's name.

  ```python 
  def on_status(self, status):
  self.output.write(status + "\n")
	self.counter += 1
	if (self.counter%200==0):
		print(self.counter)
	if self.counter >= 20000:
		self.output.close()
		self.s3.meta.client.upload_file(self.fileName,'',self.fileName) # CHANGE THIS LINE
		#Once uploaded to S3, delete the file locally
		os.remove(self.filename)
		self.fileName = fprefix+'.'+time.strftime('%Y%m%d-%H%M%S')+'.json'
		self.output = open(self.fileName, 'w') 
		self.counter = 0
	return
	```
  * If you would like to run TwitFarm.py, please read the section below about running using the UNIX command nohup so you're educated about how to run this python script in the background.
  
####Explain running with nohup and how to kill if necesarry
  * If you want to skip the boring explanations, run these commands
      * `nohup python -u TwitFarm.py` to start your python job in the background. You can close your SSH instance now and the job will still be running.
      * `tail -f nohup.out` to monitor any output from the script
      * `kill -9 <pid>` to kill the process
  
  Wouldn't it be nice if you could just run this process without having to keep your SSH instance alive? Well, you can do that pretty simply! We'll make use of the **nohup** command it order to do that. Here's a quick explanation:
  * The nohup command allows you to run a script that ignores the signal sent when you terminate your terminal instance. Most jobs will end when you kill the terminal that started them, but not a job run with nohup!
  * It may become necesarry to kill the job you started with nohup; things do happen. You'll need to use the **kill** command to do this. All you need to kill it is the PID (process identifier). To find that, run this command: `ps aux | grep <username>`
      * If you've followed this guide, your username will simple be **ubuntu**
  * The process you'll be looking for will have this (or a similar) command in the right-most column: `python TwitFarm.py`
    * The PID will be the second column from your `ps` command, right after your username.
  Now, normally you woudln't have to use any special commands to kill a process. A simple `kill <pid>` would do the job... but that is not the case when you start a job with `nohup`. `Kill` normally kills a job using the very signal that `nohup` ignores, so you need to specify `kill -9 <pid>` to properly kill this job. 

  So, we know how to start the job, and we know how to end the job. What about monitoring it, though? That's fairly easy as well. `nohup` by default appends all output to the file **nohup.out**. In order to continuously monitor this, we can run a simple `tail` command using the file flag, i.e. `tail -f nohup.out'. This will give you a continous stream of the script output in your terminal window. 
  
  **HOWEVER** this will not work if, to start the job, you ran `nohup python TwitFarm.py`. Why is that? It's because python uses a buffered output and, without going to far into what that means, it won't write anything to the output file unless you flush stdout periodically. We can get around this, however, by running python in unbuffered mode. You simply need to pass the `-u` flag when running python to do this, which gives us the end result of `nohup python -u TwitFarm.py`. Now, you can successfully view any output from the script with the `tail -f` command. Enjoy!
  * If you run the commands as specified, you can close your SSH instance now and you'll be collecting tweets on the EC2 instance indefinitely (unless the program, or EC2 instance,  crashes). 

#### Analysis of Twitter Data

Next, you can begin to install some tools to analyze the twitter data you just downloaded.  First, you will need a few tools.  These steps will install Jupyter notebook on your instance.  Jupyter is a web application that allows you to create and share documents that contain live code, equations, visualizations and explanatory text. Read more [here](http://jupyter.org/). The first thing we will do is install the dependencies:


```python
  #Type this line exactly; pyzmq causes lots of problems
  sudo pip install --upgrade pyzmq
  pip install qtconsole
  pip install ipython
  pip install notebook

```
