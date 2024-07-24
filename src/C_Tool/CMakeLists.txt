cmake_minimum_required(VERSION 3.12)
project(C_Tool)

set(CMAKE_CXX_STANDARD 14)

add_subdirectory(include/pybind11)

include_directories(include)

pybind11_add_module(thread_pool 
    src/thread_pool_pybind11.cpp 
    src/thread_pool.cpp
)