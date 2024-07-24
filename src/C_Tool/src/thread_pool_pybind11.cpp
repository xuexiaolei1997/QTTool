#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include "thread_pool.h"

namespace py = pybind11;

PYBIND11_MODULE(thread_pool, m) {
    py::class_<ThreadPool>(m, "ThreadPool")
        .def(py::init<size_t>())
        .def("enqueue", [](ThreadPool &pool, std::function func) {
            pool.enqueue([func]() {
                func();
            });
        })
        .def("enqueue_with_args", [](ThreadPool &pool, py::function func, py::args args) {
            pool.enqueue([func, args]() {
                py::gil_scoped_acquire acquire; // Ensure GIL is acquired
                py::print("\n C++: Execute thread method with args.");
                try {
                    func(*args); // Call the Python function with arguments
                } catch (const py::error_already_set& e) {
                    py::print("Python exception occurred: ", e.what());
                    PyErr_Print(); // Print Python error
                } catch (const std::exception& e) {
                    py::print("Standard exception occurred: ", e.what());
                } catch (...) {
                    py::print("Unknown exception occurred.");
                }
            }).get(); // Wait for the task to complete
        });
}
