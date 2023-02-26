import requests
import json

claimbuster_api_key = "ca8b488b9e4a46479a249a99e887f19f"
input_claim = "Dowsing, also known as divining or water witching, is a practice that involves using a tool, such as a Y-shaped rod or a pendulum, to locate underground water, minerals, or other hidden objects. There are several theories on how dowsing works, but there is no scientific evidence to support any of them. Some proponents believe that dowsing relies on the dowser's ability to tap into a subconscious or extrasensory perception, while others suggest that it involves subtle physical cues, such as changes in the dowser's muscle tension or body movements. Despite the lack of scientific evidence, some people continue to use dowsing as a tool for exploration or problem-solving, while others consider it to be a pseudoscience or superstition. It is important to note that relying on dowsing alone to make important decisions, such as the location of a well or the presence of hazardous materials, can be risky and potentially dangerous."

# Define the endpoint (url) with the claim formatted as part of it, api-key (api-key is sent as an extra header)
# api_sing_sent_endpoint = f"https://idir.uta.edu/claimbuster/api/v2/score/text/{input_claim}"
api_sentence_endpoint = f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{input_claim}"
request_headers = {"x-api-key": claimbuster_api_key}

# Send the GET request to the API and store the api response
api_response = requests.get(url=api_sentence_endpoint, headers=request_headers)

# Print out the JSON payload the API sent back
print(api_response.json())

