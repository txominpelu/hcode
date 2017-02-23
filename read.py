#!/usr/bin/env python
import sys
import pprint

#5 2 4 3 100
#50 50 80 30 110
#1000 3
#0 100
#2 200
#1 300
#500 0
#3 0 1500
#0 1 1000
#4 0 500
#1 0 1000

def read_header(line):
    params = line.split(" ")
    return {
        "num_videos" : int(params[0]),
        "num_endpoints" : int(params[1]),
        "num_request_descriptions" : int(params[2]),
        "num_caches" : int(params[3]),
        "caches_size" : int(params[4].strip())
    }

def read_video_sizes(line):
    return [int(x.strip()) for x in line.split(" ")]

def read_endpoint(f):
    [data_center_latency, num_connections] = f.next().split(" ")
    num_connections = int(num_connections.strip())
    data_center_latency = int(data_center_latency)
    connections = []
    for i in range(0, num_connections):
        [endpoint, latency] = f.next().split(" ")
        latency = int(latency.strip())
        endpoint = int(endpoint.strip())
        connections.append({"cache": endpoint, "latency": latency})
    return { "data_center_latency" : data_center_latency,
             "num_connections" : num_connections,
             "connections" : connections}


def read_request(f):
    params = [ int(s.strip()) for s in f.next().split() ]
    return { "video": params[0],
      "endpoint": params[1],
      "requests": params[2]}

def assign(params):
    results = [ { "left": params["caches_size"], "videos_stored": [] } for i in range(0, params["num_caches"]) ]
    for i,v in enumerate(params["videos"]):
        bigger_size = max([ x["left"] for x in results])
        bigger_size_index = [ x["left"] for x in results].index(bigger_size)
        if  bigger_size >= v :
            results[bigger_size_index]["left"] = results[bigger_size_index]["left"] - v
            results[bigger_size_index]["videos_stored"].append(i)
    return results

def print_result(results):
    print len(results)
    for i,v in enumerate(results):
        print "{0} {1}".format(i, " ".join([str(x) for x in results[i]]))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        params = read_header(f.next())
        params["videos"] = read_video_sizes(f.next())
        params["endpoints"] = [read_endpoint(f) for i in range(0,params['num_endpoints'])]
        params["requests"] = [read_request(f) for i in range(0,params['num_request_descriptions'])]
        #pprint.pprint(params)
        print_result([x["videos_stored"] for x in assign(params)])
        #pprint.pprint(assign(params))



