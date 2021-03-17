#!/bin/bash -xe

echo 'Downloading and installing Cloudwatch Agent'
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb -O /tmp/amazon-cloudwatch-agent.deb
sudo dpkg -i -E /tmp/amazon-cloudwatch-agent.deb
echo 'Installation of CW agent Finished'
echo '============================================'
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c ssm:AmazonCloudWatch-Config-Ubuntu
echo '============================================'
sudo apt-get update -y
sudo apt-get install ruby-full -y
sudo apt-get install wget -y
sudo apt-get install -y python3-pip

sudo apt install -y awscli

echo '================CLOUDWATCH-STATUS========================'
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
echo '========================================================='

EC2_AVAIL_ZONE=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone`
EC2_REGION="`echo \"$EC2_AVAIL_ZONE\" | sed 's/[a-z]$//'`"
wget https://aws-codedeploy-${EC2_REGION}.s3.amazonaws.com/latest/install
sudo chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent start
sleep 2
sudo service codedeploy-agent status
