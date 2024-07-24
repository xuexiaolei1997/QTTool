import time
from common import thread_pool

def task_no_args():
    print("Task executed with no arguments\n")

def task_with_args(*args):
    print(f"Task executed with arguments: {args}")

if __name__ == "__main__":
    pool = thread_pool.ThreadPool(4)
    # help(thread_pool)
    pool.enqueue(task_no_args)
    # time.sleep(2)
    pool.enqueue_with_args(task_with_args, 1, 2, 3)
