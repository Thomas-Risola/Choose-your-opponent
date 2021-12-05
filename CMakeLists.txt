cmake_minimum_required(VERSION 3.15)
project(Choose_your_opponent)
set(CMAKE_CXX_STANDARD 14)


add_subdirectory(extern/pybind11)
pybind11_add_module(Choose_your_opponent_python main.cpp tools.cpp DoubleTree.cpp algo_to_python.cpp)


add_executable(Choose_your_opponent main.cpp tools.cpp DoubleTree.cpp algo_to_python.cpp)