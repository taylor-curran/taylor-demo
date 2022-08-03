"""Where we define the depoloyment object."""
from prefect.deployments import Deployment
from prefect.packaging import FilePackager
from prefect.deployments import FlowScript
from pathlib import Path

print(Path(__file__).parent)

my_manifest = FilePackager(
    default_factory=Path(__file__).parent 
)

Deployment(
    flow=FlowScript(
        path="flow.py",
        name="Demo Flow",  
    ),
    packager=my_manifest,
    parameters={
        'desired_outcome': ['Fail', 'Success'][1]
    },
    tags=['Demo', 'Production']

)