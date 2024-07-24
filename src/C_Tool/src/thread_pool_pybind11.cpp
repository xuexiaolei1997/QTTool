#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include "thread_pool.h"

namespace py = pybind11;

PYBIND11_MODULE(thread_pool, m) {
    py::class_<ThreadPool>(m, "ThreadPool")
        .def(py::init<size_t>())
        .def("enqueue", [](ThreadPool &pool, std::function<void()> f) {
            pool.enqueue(f);
        });
}
