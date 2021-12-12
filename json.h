#pragma once
#include <iostream>
#include <fstream>
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include "json-develop/single_include/nlohmann/json.hpp"


Imagine::Matrix<double> getVictoryMatrix(std::ifstream file);

Imagine::Matrix<bool> getPlayMatrix(std::ifstream file);
