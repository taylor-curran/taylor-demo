from prefect import flow, task


@task(name="Task 1")
def task_1(runs):
    if runs:
        return 42
    else:
        raise ValueError("I am bad task")
        return 2

@flow(name="Flow 1")
def flow_1(runs):
    result_1 = task_1.submit(runs) # result_1 = task_1(runs) 
    return result_1

@task(name="Task 2")
def task_2(val):
    return 1

@flow(name="Flow 2")
def flow_2(flow_output_1):
    result_2 = task_2.submit(flow_output_1) # result_2 = task_2(flow_output_1) 
    return result_2

@task(name="Task 3")
def task_3():
    return 3

@flow(name="Flow 3")
def flow_3():
    task_3.submit()

@flow(name="My_Parent_Flow")
def my_parent_flow(runs):
    flow_output_1 = flow_1(runs)
    flow_state_1 = flow_1(runs)
    flow_output_2 = flow_2(flow_output_1)
    flow_3()


# """Where we define the depoloyment object."""
# from prefect.deployments import Deployment
# from prefect.infrastructure import Process
# from prefect.deployments import FlowScript

# Deployment(
#     name="Subflow Behavior",
#     flow="My Parent Flow",
#     parameters={
#         'desired_outcome': (['Fail', 'Success'][1])
#     },
#     infrastructure=Process(),
#     tags=['dev_subflow_behavior', 'DEV']
#     )