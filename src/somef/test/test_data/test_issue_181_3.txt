# MultiDepth

Source code for MultiDepth, our single-image depth estimation method based on joint regression and classification in a multi-task setup.
This work was presented at the IEEE Intelligent Transportation Systems Conference (ITSC) 2019.

If you make use of our code or approach, please consider citing [our paper](https://arxiv.org/abs/1907.11111) as:

    @InProceedings{,
      author    = {Lukas Liebel and Marco K\"orner},
      title     = {{MultiDepth}: Single-Image Depth Estimation via Multi-Task Regression and Classification},
      booktitle = {IEEE Intelligent Transportation Systems Conference (ITSC)},
      year      = {2019}
    }

Check out the [KITTI leaderboard](http://www.cvlibs.net/datasets/kitti/eval_depth.php?benchmark=depth_prediction) for exemplary results I got using this concept.

> I'm confident that you should be able to achieve better results with more training and some minor tweaks.

This implementation is heavily based on [pytorch-semseg](https://github.com/meetshah1995/pytorch-semseg), a brilliant project maintained by Meet Pragnesh Shah (released under [MIT license](https://github.com/meetshah1995/pytorch-semseg/blob/master/LICENSE)).
Please check out and contribute to their project and feel free to ignore certain parts in my code that are just unused parts of the *ptsemseg* codebase.


## Step-by-step Instructions

### A Word of Warning

I originally wrote this code for a different project.
While most of the unnecessary (and some of the confusing) pieces have already been removed, it might still contain some cryptic lines.
Just ignore them and you should be fine ;)

> *Sorry for the mess :D If you are/were/know a PhD student you know the drill...*

### Docker Container

This repository comes with a Dockerfile allowing you to build an image that can be used to optionally run training inside a container.
Just skip the respective steps in the following instructions if you do not wish to use docker.

> Please note that I highly recommend using docker and never tried to run the provided code outside of a container.

0. *(optional)* Adjust the [Dockerfile](docker/Dockerfile) if needed (e.g., add helpful utils, such as tmux, htop, etc.).
> To change this later just stop running containers, re-build the image and restart the container.

1. Go to the [docker dir](docker).
Build the MultiDepth docker image by running the respective [script](docker/build_image.sh): `./build_image.sh`

2. Adjust the mount parameters of your container in the provided [script](docker/start_container.sh), such that the directories containing your training data are mounted to `/root/data/kitti/rgb` and `/root/data/kitti/depth`.
>Feel free to change this if you want to use a different dir tree.
Keep in mind that it will be necessary to adjust the paths in other places accordingly.

  You can also mount an external directory to `/root/logs` in order to save tensorboard logs and checkpoints outside of the container.

3. Start your container by running the [script](docker/start_container.sh): `./start_container.sh`

4. Connect to the running container, e.g., by running `docker exec -it multidepth bash` or by simply calling the provided minimal [script](docker/connect_to_container.sh): `./connect_to_container.sh`

5. To stop the container simply disconnect from the container (e.g., by pressing [Ctrl] + [D]) and kill it: `docker kill multidepth`.

> If you are familiar with docker, you probably know better ways of starting and stopping containers as well as running scripts within them :)


### Set Training Parameters

You can adjust training behavior and numerous other options using a [YAML configuration file](configs/example_config.yml).
Most of the parameters in the example script should be self-explanatory and they are already set to useful values.

> I might add a more detailed explanation in the future.
Until then, feel free to message me if you have trouble with understanding their effect and I will update this section accordingly.


### Run Training

Run the [main training script](train.py) which expects a single parameter `--config` specifying the path to a configuration file, e.g.: `python train.py --config configs/example_config`.

> Note that it might take a while for the actual training process to start depending on the size of your dataset.


### Visualize Training Progress

The training script will write Tensorboard logs to the directory specified in the [config file](configs/example_config.yml).
Display the results by starting Tensorboard and directing it to the respective log dir.

You could do this by starting another docker container with TensorFlow: `docker run --rm -it -p 6006:6006 -v ~/path/to/my/logs:/root/logs tensorflow/tensorflow`

Make sure to mount the correct data dir and map a different port if necessary (6006 is Tensorboard's standard port).
This will allow you to access the web interface of Tensorboard running on a server from your local machine.

> This works for me in certain settings but your mileage will vary depending on your network configuration!

Start tensorboard: `tensorboard --logdir /root/logs` and navigate to [your server's ip/localhost]:6006 to access the web-interface in your favorite web browser.


### Evaluate Results

Mid-training validation will be carried out from time to time according to your [config file](configs/example_config.yml).


## Hardware Requirements

Even though a CUDA-capable GPU is not strictly required to run this training script, it is highly recommended for obvious reasons.
Adjust the batch size if you run out of memory.
Successfully tested on 1080 and 1080Ti GPUs.
**Multi-GPU training with batch-splitting will be used if you provide multiple GPUs!**


## Contribute

If you encounter any errors or unexpected behavior feel free to message me.
You are also welcome to file pull requests if you want to help to improve or fix any part of this.

**Thank you!**
