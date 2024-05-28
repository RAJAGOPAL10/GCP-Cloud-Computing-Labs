
|       Method 	    |   Local   | Same-Zone |  Different Region  |  
|-------------------|-----------|-----------|--------------------|  
|   REST add	    |   3.15	|   3.18    |  	   297.54        |  
|   gRPC add	    |   0.69	|   0.82	|      145.98        |  
|   REST rawimg	    |   6.31	|   8.42	|      1211.81       |  
|   gRPC rawimg	    |   6.44    |   6.92	|      202.248       |  
|   REST dotproduct	|   4.23	|   3.92	|  	   298.62        |  
|   gRPC dotproduct	|   0.79	|   0.93	|      146.23        |  
|   REST jsonimg	|   34.21	|   39.23	|      1345.78       |  
|   gRPC jsonimg	|   21.13   |   21.48	|      225.96        |  
|   PING            |   0.06    |   0.41    |      140.91        |


Based on the results presented in the table, it is evident that there are substantial performance difference between REST and gRPC in terms of latency in performing the operations, especially in the context of where the server and clients are located. When the server and client are in the same system the operation times are similar. When the server and client are in different systems in different zones the operation time gRPC is much lower than that of REST. gRPC methods are faster by almost 5-6 times when the systems are far apart. The main cause is network latency. This can be explanied because of the following:  

* REST API's use a new TCP connection for each request whereas gRPC usess the same connection for multiple requests.  
* gRPC is able to handel multiple requests at the same time as defined by ThreadPoolExecutor (in our case =10) whereas each client request in REST is handled one at a time.  
* gRPC uses HTTP/2 compared to REST which uses HTTP/1.  
* gRPC uses a light weight protobuff for communication whereas REST uses json in our case.


REST mainly suffers from the extra overhead of setting up new TCP connections for each request. This isn't the case with gRPC. Thus the network latency suffered by REST went the server and client are far apart introduces poor performance when compared to gRPC which requires a single connection. Overall, gRPC is the prefered mode to carry out operations in a distributed environment. 