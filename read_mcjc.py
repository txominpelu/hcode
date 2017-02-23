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
    endpoints = [ { "videos": [], "caches": params["endpoints"][i]["connections"], "total_requests": 0 } for i in range(0, params["num_endpoints"])]

    for i, request in enumerate(params["requests"]):
        endpoint_number = request["endpoint"]
        video_number = request["video"]
        video_size = params["videos"][video_number]
        num_requests = request["requests"]
        weight = float(video_size)/num_requests
        endpoints[endpoint_number]["videos"].append({"video": video_number, "num_requests": num_requests, "weight": weight})
        endpoints[endpoint_number]["total_requests"] = endpoints[endpoint_number]["total_requests"] + num_requests
    sorted_endpoints = sorted(endpoints, key=lambda endpoint: endpoint["total_requests"])
    endpoints = sorted_endpoints
    
    for i, endpoint in enumerate(endpoints):
        sorted_videos = sorted(endpoint["videos"], key=lambda video: video["weight"])
        sorted_caches = sorted(endpoint["caches"], key=lambda cache: cache["latency"])
        endpoint["videos"] = sorted_videos
        endpoint["caches"] = sorted_caches

    result = [ {"space_left": params["caches_size"], "videos": []} for i in range(0, params["num_caches"])]

    for i, endpoint in enumerate(endpoints):
        video_it = 0
        num_videos_for_endpoint = len(endpoint["videos"])

        for i, cache in enumerate(result):
            num_videos_in_cache = 0
            while num_videos_in_cache < num_videos_for_endpoint:
                video_number = endpoint["videos"][video_it]["video"]
                video_size = params["videos"][video_number]
                if ((video_number not in cache["videos"]) and (cache["space_left"] - video_size > 0)):
                    cache["videos"].append(video_number)
                    cache["space_left"] = cache["space_left"] - video_size
                else:
                    break
                video_it = (video_it + 1)%num_videos_for_endpoint
                num_videos_in_cache = num_videos_in_cache + 1
    return result

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
        result = assign(params)
        print_result([cache["videos"] for cache in result])
        #pprint.pprint(params)
        #print_result([x["videos_stored"] for x in assign(params)])
        #pprint.pprint(assign(params))



