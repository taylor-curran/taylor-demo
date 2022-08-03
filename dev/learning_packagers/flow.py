from prefect import task, flow
from prefect.orion.schemas.states import Completed, Failed
from prefect.tasks import task_input_hash

from datetime import timedelta
from prefect import tags
import os
import random


@task(
    name="Always Succeeds Task",
    version=os.getenv("GIT_COMMIT_SHA")
    )
def always_succeeds_task():
    return "foo"

@task(
    name="Depnds on AST",
)
def depends_on_ast(ast):
    if ast == 'foo':
        return "fa"
    else:
        return "na?"

@task(
    name="Often Fails Task",
    retries=20
)
def often_fails_task():
    """A task that benefits from task retries"""
    outcome = random.choice(['Fail', 'Success', 'Fail', 'Fail', 'Fail'])
    if outcome == 'Fail':
        raise Exception('Random Choice was Failure')
    elif outcome == 'Success':
        return 'Success!!'

@task(
    name="Very Large Computation",
    cache_key_fn=task_input_hash, 
    cache_expiration=timedelta(days=30)
)
def large_computation(small_int):
    """A task that benefits from """
    for i in range(1000000):
        j = i + small_int
    print('Done large computation!')
    return small_int * 5

@task(
    name="Follows Large Computation",
    )
def follows_large_computation(result_from_lc, succeed=True):
    if succeed == True:
        output = result_from_lc / 2
        return output
    else:
        raise Exception("I am bad task")

@task(
    name="Second After Large Computation",
    )
def second_after_large_computation(result_from_flc):
    output = result_from_flc
    return output

@task(
    name="Task with Tag",
    tags=['Specific_Tag']
)
def task_with_tag():
    """A task that is called by virtue of its tag."""
    print("This is a task with a Specific Tag")

@task(name="Always Fails Task")
def always_fails_task():
    raise Exception("I am bad task")

@flow(name="Sub Flow")
def sub_flow():
    print("Sub Flow")

@flow(name="Demo Flow")
def demo_flow(desired_outcome='Success'):

    ast = always_succeeds_task()
    depends_on_ast(ast)

    sub_flow()

    often_fails_task()

    task_result_0 = large_computation(5)

    if desired_outcome == 'Fail':
        task_result_1 = follows_large_computation(task_result_0, False)
    
    else:
        task_result_1 = follows_large_computation(task_result_0)

    second_after_large_computation(task_result_1)
    


    with tags('Specific_Tag'):
        task_with_tag()
    
    if desired_outcome == 'Fail':
        always_fails_task()

    always_succeeds_task()