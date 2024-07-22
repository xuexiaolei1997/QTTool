#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "data_processing.h"

namespace py = pybind11;

PYBIND11_MODULE(data_processing, m) {
    m.def("process_data", &process_data, "A function that processes data");
}