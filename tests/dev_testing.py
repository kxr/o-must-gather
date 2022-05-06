from omg.config.logging import setup_logging
from omg.must_gather.load_resources import load_res


setup_logging("info")

paths = [
    '/home/knaeem/Desktop/mgs/must-gather.etism/registry-redhat-io-openshift-service-mesh-istio-must-gather-rhel7-sha256-b73931d591587f34e94fd79de84b557417b817616a04631e6c741268b47d9d05',
    '/home/knaeem/Desktop/mgs/must-gather.etism/quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256-2f3d142d13081954fc73e1d5e6ee96a04ba7c5714e9193f985d0a6962d325841'
]

# config = Config()
# config.paths = paths
# config.project = "openshift-apiserver"

res = load_res(paths, "configmap", ns="openshift-config")

for r in res:
    rs = r["res"]
    print(rs["metadata"]["name"])
