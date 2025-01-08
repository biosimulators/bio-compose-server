import yaml
import sys


service_name: str = sys.argv[1]
# is_dev: int = int(sys.argv[2])

fp = 'docker-compose.yaml'

with open(fp, 'r') as file:
    compose_data = yaml.safe_load(file)

image = compose_data['services'][service_name]['image']
version = image.split(":")[1]

# if is_dev:
#     version += '-dev'

print(version)


