"""
Traffic Analyzer Project

Command	Explanation	Outcome


docker build -t traffic-analyzer .

Builds a Docker image named 'traffic-analyzer' from the current folder 
(containing the Dockerfile).	Creates a reusable image of your Python
app with all dependencies installed.



docker ps -a	

Lists all containers, including ones that have stopped.	Confirms if your
container ran successfully (Exit 0 means no error).



docker run traffic-analyzer	

Runs the container from the 'traffic-analyzer' image.Executes your Python
script in an isolated container but does not save output to your real folder.



docker run -v %cd%:/app traffic-analyzer	

Mounts your current Windows folder into the container’s /app directory.	Files
created in the container (like flagged_ips.txt) appear in your actual project folder.




docker images	

Lists all Docker images on your system.	Lets you see and manage built
images like 'traffic-analyzer'.




docker container prune

Removes all stopped containers to free space.Cleans up unused
containers safely.




docker rmi traffic-analyzer

Removes the 'traffic-analyzer' image if you no longer need it.
Cleans up space by removing your custom Docker image.

"""