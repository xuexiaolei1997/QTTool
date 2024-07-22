#include "data_processing.h"

std::vector<double> process_data(const std::vector<double>& data) {
    // 简单示例：计算每个元素的平方
    std::vector<double> result;
    for (const auto& value : data) {
        result.push_back(value * value);
    }
    return result;
}