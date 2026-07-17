---
name: c-lang
description: Use when writing, compiling, debugging, or reviewing C code. Trigger on phrases like "C code", "compile C", "gcc", "clang", "makefile", "C project", "pointer", "malloc", "segfault", "valgrind", or when working with .c and .h files.
---

# C Language Skill

Write, compile, and debug C code with best practices.

## Toolchain

```bash
# Compiler
gcc --version
clang --version

# Build
gcc -Wall -Wextra -Werror -O2 -o output source.c
clang -Wall -Wextra -Werror -O2 -o output source.c

# Debug build
gcc -g -O0 -fsanitize=address -o output source.c

# Memory check
valgrind --leak-check=full --track-origins=yes ./output

# Format
clang-format -i file.c
```

## Project Structure

```
project/
├── src/
│   ├── main.c
│   ├── calculator.c
│   └── calculator.h
├── include/
│   └── shared.h
├── tests/
│   └── test_calculator.c
├── Makefile
└── README.md
```

## Makefile Template

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c11 -Iinclude
LDFLAGS = -lm
DEBUG_FLAGS = -g -O0 -fsanitize=address

SRC = $(wildcard src/*.c)
OBJ = $(SRC:.c=.o)
BIN = calculator

.PHONY: all clean debug test

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

debug: CFLAGS += $(DEBUG_FLAGS)
debug: clean all

test: CFLAGS += -DTESTING
test: clean all
	./tests/run_tests.sh

clean:
	rm -f $(OBJ) $(BIN)
```

## Memory Management Patterns

```c
// Safe malloc with NULL check
void *safe_malloc(size_t size) {
    void *ptr = malloc(size);
    if (!ptr) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    return ptr;
}

// Safe realloc
void *safe_realloc(void *ptr, size_t size) {
    void *new_ptr = realloc(ptr, size);
    if (!new_ptr && size > 0) {
        fprintf(stderr, "Memory reallocation failed\n");
        free(ptr);
        exit(EXIT_FAILURE);
    }
    return new_ptr;
}

// Safe string duplicate
char *safe_strdup(const char *s) {
    if (!s) return NULL;
    char *dup = malloc(strlen(s) + 1);
    if (!dup) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    strcpy(dup, s);
    return dup;
}
```

## Error Handling

```c
// Return codes pattern
typedef enum {
    CALC_OK = 0,
    CALC_ERR_NULL_PTR,
    CALC_ERR_DIVISION_BY_ZERO,
    CALC_ERR_OVERFLOW,
    CALC_ERR_INVALID_INPUT,
    CALC_ERR_MEMORY
} CalcError;

const char *calc_error_string(CalcError err) {
    switch (err) {
        case CALC_OK: return "Success";
        case CALC_ERR_NULL_PTR: return "Null pointer";
        case CALC_ERR_DIVISION_BY_ZERO: return "Division by zero";
        case CALC_ERR_OVERFLOW: return "Overflow";
        case CALC_ERR_INVALID_INPUT: return "Invalid input";
        case CALC_ERR_MEMORY: return "Memory error";
        default: return "Unknown error";
    }
}

// Usage
CalcError calculate(double a, double b, double *result) {
    if (!result) return CALC_ERR_NULL_PTR;
    if (b == 0.0) return CALC_ERR_DIVISION_BY_ZERO;
    *result = a / b;
    return CALC_OK;
}
```

## String Safety

```c
// Always use snprintf, never sprintf
char buffer[256];
snprintf(buffer, sizeof(buffer), "Result: %f", result);

// Safe string copy
void safe_strcpy(char *dest, const char *src, size_t dest_size) {
    if (dest_size == 0) return;
    strncpy(dest, src, dest_size - 1);
    dest[dest_size - 1] = '\0';
}

// Safe string concatenation
void safe_strcat(char *dest, const char *src, size_t dest_size) {
    size_t len = strlen(dest);
    if (len >= dest_size - 1) return;
    snprintf(dest + len, dest_size - len, "%s", src);
}
```

## Debugging

```c
// GDB
gcc -g program.c -o program
gdb ./program

// Common GDB commands
// break main      - set breakpoint
// run             - start program
// next            - step over
// step            - step into
// print variable  - print value
// backtrace       - show call stack
// watch variable  - break on change

// Address sanitizer (runtime error detection)
gcc -fsanitize=address -g program.c -o program
./program  # Reports memory errors

// Undefined behavior sanitizer
gcc -fsanitize=undefined -g program.c -o program
```

## Rules

- NEVER use `gets()` — use `fgets()` with size limit
- ALWAYS check malloc/calloc return values
- Use `snprintf` instead of `sprintf`
- Initialize all variables before use
- Free memory in reverse order of allocation
- Use `const` wherever possible
- Compile with `-Wall -Wextra -Werror`
