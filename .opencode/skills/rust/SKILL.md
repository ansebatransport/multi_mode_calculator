---
name: rust
description: Use when writing, compiling, debugging, or reviewing Rust code. Trigger on phrases like "Rust", "cargo", "compile Rust", "rustc", "ownership", "borrowing", "lifetime", "trait", "enum", "match", "Result", "Option", or when working with .rs files and Cargo.toml.
---

# Rust Language Skill

Systems programming with memory safety and zero-cost abstractions.

## Toolchain

```bash
# Install/update
rustup update

# Compiler
rustc --version

# Package manager
cargo --version

# Create project
cargo new calculator --bin
cargo new calculator --lib

# Build
cargo build
cargo build --release

# Run
cargo run
cargo run -- --arg value

# Check (fast compile check)
cargo check

# Test
cargo test
cargo test -- --nocapture

# Lint
cargo clippy

# Format
cargo fmt

# Audit dependencies
cargo audit
```

## Project Structure

```
calculator/
├── Cargo.toml
├── src/
│   ├── lib.rs          # Library root
│   ├── main.rs         # Binary entry point
│   ├── calculator.rs   # Calculator module
│   ├── error.rs        # Error types
│   └── financial.rs    # Financial module
├── tests/              # Integration tests
│   └── calculator_test.rs
├── benches/            # Benchmarks
│   └── calculation.rs
└── examples/           # Example usage
    └── basic.rs
```

## Cargo.toml Template

```toml
[package]
name = "calculator"
version = "0.1.0"
edition = "2021"
authors = ["Mulugeta"]
description = "Multi-mode calculator"
license = "MIT"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
thiserror = "1.0"
anyhow = "1.0"

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
proptest = "1.0"

[[bench]]
name = "calculation"
harness = false
```

## Ownership & Borrowing

```rust
// Ownership transfer
fn take_ownership(s: String) -> String {
    format!("{} modified", s)
}

// Borrowing (immutable)
fn calculate(expr: &str) -> Result<f64, Error> {
    // expr is borrowed, not owned
    parse_and_eval(expr)
}

// Borrowing (mutable)
fn append_history(history: &mut Vec<String>, entry: String) {
    history.push(entry);
}

// Lifetime annotations
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct Calculator<'a> {
    expression: &'a str,
    angle_mode: AngleMode,
}
```

## Error Handling

```rust
// Custom error type
#[derive(Debug, thiserror::Error)]
pub enum CalcError {
    #[error("Division by zero")]
    DivisionByZero,

    #[error("Invalid expression: {0}")]
    InvalidExpression(String),

    #[error("Overflow in calculation")]
    Overflow,

    #[error("Unknown function: {0}")]
    UnknownFunction(String),
}

pub type Result<T> = std::result::Result<T, CalcError>;

// Usage with Result
fn divide(a: f64, b: f64) -> Result<f64> {
    if b == 0.0 {
        Err(CalcError::DivisionByZero)
    } else {
        Ok(a / b)
    }
}

// Pattern matching
fn calculate(expr: &str) -> Result<f64> {
    match parse(expr) {
        Ok(parsed) => eval(parsed),
        Err(CalcError::InvalidExpression(e)) => {
            eprintln!("Parse error: {}", e);
            Err(CalcError::InvalidExpression(e))
        }
        Err(e) => Err(e),
    }
}

// ? operator for error propagation
fn complex_calculation(input: &str) -> Result<f64> {
    let parsed = parse(input)?;       // Returns early on error
    let result = eval(parsed)?;
    Ok(result)
}
```

## Enums & Pattern Matching

```rust
#[derive(Debug, Clone)]
enum Operation {
    Add(f64, f64),
    Subtract(f64, f64),
    Multiply(f64, f64),
    Divide(f64, f64),
    Power(f64, f64),
}

impl Operation {
    fn execute(&self) -> Result<f64> {
        match self {
            Operation::Add(a, b) => Ok(a + b),
            Operation::Subtract(a, b) => Ok(a - b),
            Operation::Multiply(a, b) => Ok(a * b),
            Operation::Divide(a, b) => {
                if *b == 0.0 {
                    Err(CalcError::DivisionByZero)
                } else {
                    Ok(a / b)
                }
            }
            Operation::Power(a, b) => Ok(a.powf(*b)),
        }
    }
}
```

## Traits

```rust
pub trait Calculable {
    fn calculate(&self) -> Result<f64>;
    fn description(&self) -> &str;
}

impl Calculable for Operation {
    fn calculate(&self) -> Result<f64> {
        self.execute()
    }

    fn description(&self) -> &str {
        match self {
            Operation::Add(_, _) => "Addition",
            Operation::Subtract(_, _) => "Subtraction",
            Operation::Multiply(_, _) => "Multiplication",
            Operation::Divide(_, _) => "Division",
            Operation::Power(_, _) => "Power",
        }
    }
}

// Trait bound syntax
fn process_all<T: Calculable>(items: &[T]) -> Vec<Result<f64>> {
    items.iter().map(|item| item.calculate()).collect()
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_divide() {
        assert_eq!(divide(10.0, 2.0).unwrap(), 5.0);
    }

    #[test]
    fn test_divide_by_zero() {
        assert!(matches!(
            divide(10.0, 0.0),
            Err(CalcError::DivisionByZero)
        ));
    }

    #[test]
    fn test_complex() {
        let result = complex_calculation("(2 + 3) * 4").unwrap();
        assert!((result - 20.0).abs() < 1e-10);
    }

    // Property-based testing
    proptest! {
        #[test]
        fn test_add_commutative(a: f64, b: f64) {
            let ab = add(a, b);
            let ba = add(b, a);
            prop_assert!((ab - ba).abs() < 1e-10);
        }
    }
}
```

## Debugging

```bash
# Debug build
cargo build
cargo run

# GDB
cargo build
gdb target/debug/calculator

# Logging
RUST_LOG=debug cargo run

# Backtrace on panic
RUST_BACKTRACE=1 cargo run

# Clippy lints
cargo clippy -- -W clippy::all

# Benchmarks
cargo bench
```

## Rules

- NEVER use `unwrap()` in production code — use `?` or `match`
- ALWAYS handle `Result` and `Option` explicitly
- Use `thiserror` for library errors, `anyhow` for applications
- Prefer `&str` over `String` in function parameters
- Use `impl Trait` for simple returns, named types for complex
- Use `clippy` before every commit
- Use `cargo fmt` for consistent formatting
