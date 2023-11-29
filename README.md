## 🚗 traffic-sign-detection-service 

This service is designed for marking traffic signs on video files. Please check out [demo](karouniform.xyz:7680) for a visual demonstration.

### 🐋 Local launch using Docker
1. Download the repository with `git clone`
2. Enter the folder with `cd`
3. Build image with `sudo docker build . -t demo-itmo` .
Please wait. The project takes about three minutes to create.
4. Start the project using `sudo docker run --name Demo-itmo -p 7860:7860 demo-itmo` . The first run takes about 60 seconds - depends on how many demo files you put in examples. All of them will be preprocessed and cached.
5. Log in to the service at `http://127.0.0.1:7860/` or at the address of the server where you deploy it.
6. ✨ Enjoy it!

### 🌏 Scaling prospects
This container is a self-contained service, but it can be used as a worker in services such as k8s or docker-compose, provided the appropriate architecture. Please use a load balancer (e.g. nginx) to distribute incoming connections across workers. In this case, the service can scale horizontally almost indefinitely, including to different geo-located servers.

### 🔥 Performance evaluation
All measurements took place on the following configuration: Intel(R) Xeon(R) CPU E5-2698 v3 @ 2.30GHz. Number of available cores: 8. Amount of available memory: 32 GB. Memory frequency: 2133 GHz.

We got the following results: RAM usage: no more than 1 GB (typical consumption is around 200 MB). Performance: 8 frames per second. This result shows good performance - the service, being deployed on a mid-segment mobile device using a built-in GPU, is capable of processing video at 8-16 frames per second.