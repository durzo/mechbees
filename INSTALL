Python dependencies: boto, Tkinter, multimechanize, matplotlib, os, paramiko, time, re, and many many more

cp boto-configs/boto-aws ~/.boto
vim ~/.boto (update access keys)

Setup the Queen Bee AMI:

make a t1.micro ec2 instance and install the python multimechanize tools and make sure they are accessible from the users $PATH
see http://testutils.org/multi-mechanize/#install-setup for more info
upload the contents of the queen_bee/ folder to the users home on the new ec2
on the ec2, create a symlink to fix a bug in multimechanize: user@queenbee:~/$ ln -s . projects
shutdown the instance and create an AMI image, taking note of the AMI-ID that we will use futher down

to fire up 39 bees:

*** only one region can be used at a time, make sure you use the correct boto config for your region! ***

Sydney:
sed -e 's/\(ap\|us\)-\w*-[0-9]/ap-southeast-2/g' -i ~/.boto
./bees up -k catalyst-bees -s 39 -g Bees -z ap-southeast-2b -i ami-3e74e504 -t m1.medium -l ubuntu

Tokyo:
sed -e 's/\(ap\|us\)-\w*-[0-9]/ap-northeast-1/g' -i ~/.boto
./bees up -k catalyst-bees -s 39 -g Bees -z ap-northeast-1b -i ami-af1293ae -t m1.medium -l ubuntu

Singapore:
sed -e 's/\(ap\|us\)-\w*-[0-9]/ap-southeast-1/g' -i ~/.boto
./bees up -k catalyst-bees -s 39 -g Bees -z ap-southeast-1b -i ami-8c064ade -t m1.medium -l ubuntu

California:
sed -e 's/\(ap\|us\)-\w*-[0-9]/us-west-1/g' -i ~/.boto
./bees up -k catalyst-bees -s 39 -g Bees -z us-west-1b -i ami-94507dd1 -t m1.medium -l ubuntu

tell the bees to launch multimechanize in xmlrpc server mode:

./bees attack -p <project>

run gridgui and control the swarm:

./gridgui.py

"List Nodes" - list running bees
"Check Tests" - is test running on bee
"Get Project Names" - did we load the right project?
"Get Config" - retrieve bee project config
"Update Configs" - send new project config to all bees
"Run Tests" - run the test on all bees
"Get Results" - "aggregate results and compile graphs"

shutdown the swarm:

./bees down


Graphs will be in gridresults/project_name/results/results_dir/results.html
