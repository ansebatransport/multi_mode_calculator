---
name: cpp
description: Use when writing, compiling, debugging, or reviewing C++ code. Trigger on phrases like "C++", "compile C++", "g++", "clang++", "cmake", "C++ project", "STL", "templates", "RAII", "smart pointers", or when working with .cpp, .hpp, .cc files.
---

# C++ Language Skill

Modern C++ development with best practices.

## Toolchain

```bash
# Compiler
g++ --version
clang++ --version

# Build
g++ -std=c++17 -Wall -Wextra -Werror -O2 -o output source.cpp

# Debug build
g++ -std=c++17 -g -O0 -fsanitize=address,undefined -o output source.cpp

# Memory check
valgrind --leak-check=full ./output

# Format
clang-format -i file.cpp
```

## CMake Project Structure

```
project/
├── CMakeLists.txt
├── src/
│   ├── main.cpp
│   ├── calculator.cpp
│   └── calculator.hpp
├── include/
│   └── project/
│       └── calculator.hpp
├── tests/
│   ├── CMakeLists.txt
│   └── test_calculator.cpp
├── extern/
│   └── catch2/
└── README.md
```

## CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.16)
project(Calculator VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Compiler warnings
add_compile_options(-Wall -Wextra -Wpedantic -Werror)

# Main executable
add_executable(calculator
    src/main.cpp
    src/calculator.cpp
)

target_include_directories(calculator PRIVATE include)

# Math library
target_link_libraries(calculator PRIVATE m)

# Tests
option(BUILD_TESTS "Build tests" ON)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
```

## Modern C++ Patterns

### Smart Pointers (RAII)
```cpp
// NEVER raw new/delete — use smart pointers
#include <memory>

// Unique ownership
auto calc = std::make_unique<Calculator>();

// Shared ownership
auto engine = std::make_shared<MathEngine>();

// Factory function
std::unique_ptr<Calculator> create_calculator() {
    return std::make_unique<Calculator>();
}
```

### Move Semantics
```cpp
class DataBuffer {
    std::vector<double> data_;
public:
    // Move constructor
    DataBuffer(DataBuffer&& other) noexcept
        : data_(std::move(other.data_)) {}

    // Move assignment
    DataBuffer& operator=(DataBuffer&& other) noexcept {
        if (this != &other) {
            data_ = std::move(other.data_);
        }
        return *this;
    }
};
```

### Optional (C++17)
```cpp
#include <optional>

std::optional<double> safe_divide(double a, double b) {
    if (b == 0.0) return std::nullopt;
    return a / b;
}

// Usage
auto result = safe_divide(10.0, 3.0);
if (result) {
    std::cout << *result << std::endl;
}
```

### Variadic Templates
```cpp
template<typename... Args>
double calculate(Args... args) {
    // Process variable number of arguments
}

// Fold expressions (C++17)
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);
}
```

### constexpr (Compile-time)
```cpp
constexpr double pi = 3.14159265358979323846;

constexpr double square(double x) {
    return x * x;
}

// Computed at compile time
constexpr double pi_squared = square(pi);
```

## Error Handling

```cpp
// Exception-based
class CalculatorError : public std::runtime_error {
public:
    explicit CalculatorError(const std::string& msg)
        : std::runtime_error(msg) {}
};

class DivisionByZeroError : public CalculatorError {
public:
    DivisionByZeroError()
        : CalculatorError("Division by zero") {}
};

// Usage
double divide(double a, double b) {
    if (b == 0.0) throw DivisionByZeroError();
    return a / b;
}

// noexcept for functions that won't throw
void swap_values(double& a, double& b) noexcept {
    std::swap(a, b);
}
```

## Template Patterns

```cpp
// Type traits
#include <type_traits>

template<typename T>
typename std::enable_if<std::is_arithmetic_v<T>, T>::type
safe_add(T a, T b) {
    return a + b;
}

// Concepts (C++20)
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
T add(T a, T b) {
    return a + b;
}
```

## Debugging

```cpp
// GDB
g++ -g source.cpp -o program
g gdb ./program

// ASAN (Address Sanitizer)
g++ -fsanitize=address -g source.cpp -o program
./program

// UBSAN (Undefined Behavior Sanitizer)
g++ -fsanitize=undefined -g source.cpp -o program

// TSAN (Thread Sanitizer)
g++ -fsanitize=thread -g source.cpp -o program

// Profiling
g++ -pg source.cpp -o program
./program
gprof program gmon.out > analysis.txt
```

## Rules

- Use `nullptr` instead of `NULL` or `0`
- Use `auto` when type is obvious
- Prefer range-based for loops
- Use `std::string` instead of `char*`
- Use smart pointers, not raw `new`/`delete`
- Mark functions `const` when they don't modify state
- Use `enum class` instead of plain `enum`
- Compile with `-Wall -Wextra -Wpedantic -Werror`
