# AWS Greengrass ML Inference Playground

This codifies [AWS ML inference tutorial](https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-console.html). The intend is a consisten repeatable development environment for experimenting and enjoying Greengrass ML Inference.

* Instead of using AWS Console, resource defined in with [Greengo](http://greengo.io) and created with Python/Boto3.
* Instead of Raspberry PI, a Ubuntu VM.
* Instead of a camera, images are dropped to an `/images` folder in a VM. The ML inference Lambda function
  uses access to local volume to read the images.

### Pre-requisits

* A computer with Linux/MacOS, Python, git (dah!)
* [Vagrant](https://www.vagrantup.com/docs/installation/) with [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* AWS CLI [installed](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) and credentials
  [configured](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).
  Consider using [named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html).

### How to run
The instructions below is a rough draft that gives direction and can work with the right amount of extra hacking.

> Read to the end before attempting to run.
> If it fails, don't get upset: this is work in progress and a trail, not a highway.
> Roll your sleeves, hack alone, PRs welcome.


1. Install [`greengo`](http://greengo.io). Use the head of `master` - I am moving this and `greengo` together.

    ```
    pip install git+git://github.com/dzimine/greengo.git#egg=greengo
    ```

2. Create a Greengrass Core definition in AWS. See [./greengo.yaml](./greengo.yaml) for what will be created.

    ```
    greengo create
    ```

3. Provision Greengrass Core VM. Vagrant will do the magic of installing Greengrass, placing certificates and configuration,
    and adding the necessary ML stuff on the GG Core VM.

    ```
    vagrant up
    ```
    Ah, and before you run it, you should place `greengrass-ubuntu-x86-64-VERSION.tar.gz` into `./downloads`.
    What? You already run it? You should have read the instruction to the end!

4. Deploy Greengrass Core

    ```
    greengo deploy
    ```

5. ***Profit!***
   
   Login to the Vagrant VM. Drop image files to `/images`. There are few already in `./images`, and a script you can run in VM to randomly drop the files:
   
   ```
   vagrant ssh
   sudo su
   cd /vagrant/scripts
   ./feed.sh
   ```
   Watch the GGC log files to see the results:
   
   ```
   tail -f /greengrass/ggc/var/log/user/$AWS_REGION/$AWS_ACCOUNT/GreengrassImageClassification.log
   ```

   I'll eventually get to posting them to MQTT - or you can take it as an exercise.
   
   If you don't like the prediction, it has nothing to do with Greengrass - blame the pretrained [squeezenet1_1 model](http://data.dmlc.ml/mxnet/models/imagenet/squeezenet/) offered in the AWS Tutorial, and bring a better one.

6. The best part: once you've done playing, clean up your AWS resources:

    ```
    greengo remove
    ```
