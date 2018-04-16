# Solar-Weather-Station-API
API for weather.zerogravityantfarm.com


**API Endpoint Resources:**

	/register
		GET - Generate a nodeid for new nodes

	/nodes
		GET - List nodes, locations, and status (online/offline)
		POST - Add new nodes to the system
	
	/nodes/{nodeid}
		GET - Get information on single node
		PUT - Modify information on a single node
		DELETE - Delete node but not node data
		
	/nodes/{nodeid}/strikes
		GET - List all strikes for {nodeid}
		POST - Write single strike distance and date/time
		
	/nodes/{nodeid}/power
		GET - List all power data for {nodeid}
		POST - Write new power data 
		
	/nodes/{nodeid}/multisensor
		GET - List all multisensor data for {nodeid}
		POST - Write new sensor data

Api example followed from here: https://github.com/sagaragarwal94/python_rest_flask


**Build**

sudo docker build -t weatherapi .

**Run**

sudo docker run -v /home/jcox/weatherstation/api:/app -p 8081:8081 weatherapi 
