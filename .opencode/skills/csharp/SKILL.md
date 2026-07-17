---
name: csharp
description: Use when writing, compiling, debugging, or reviewing C# code. Trigger on phrases like "C#", "dotnet", "compile C#", ".NET", "NuGet", "LINQ", "async/await", "generics", "dependency injection", or when working with .cs, .csproj, .sln files.
---

# C# Language Skill

Modern .NET development with best practices.

## Toolchain

```bash
# SDK
dotnet --version

# Create project
dotnet new console -n Calculator
dotnet new classlib -n Calculator.Core
dotnet new xunit -n Calculator.Tests

# Build
dotnet build
dotnet build --configuration Release

# Run
dotnet run
dotnet run --project src/Calculator

# Test
dotnet test
dotnet test --logger "console;verbosity=detailed"

# Format
dotnet format

# Add package
dotnet add package Newtonsoft.Json

# Publish
dotnet publish -c Release -o ./publish
```

## Project Structure

```
Calculator.sln
├── src/
│   ├── Calculator.Core/          # Core library
│   │   ├── Calculator.Core.csproj
│   │   ├── Engine.cs
│   │   ├── Financial.cs
│   │   └── ExpressionParser.cs
│   └── Calculator.Web/           # ASP.NET web app
│       ├── Calculator.Web.csproj
│       ├── Program.cs
│       ├── Controllers/
│       └── Models/
├── tests/
│   └── Calculator.Tests/         # Unit tests
│       ├── Calculator.Tests.csproj
│       ├── EngineTests.cs
│       └── FinancialTests.cs
└── Calculator.sln
```

## Project File Template

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>

</Project>
```

## Modern C# Patterns

### Records (Immutable Data)
```csharp
// Record type — immutable, value-based equality
public record CalculationResult(
    double Value,
    string Expression,
    bool Success,
    string? Error = null
);

// Usage
var result = new CalculationResult(
    Value: 42.0,
    Expression: "6 * 7",
    Success: true
);

// Pattern matching
if (result is { Success: true, Value: > 0 })
{
    Console.WriteLine($"Positive result: {result.Value}");
}
```

### Pattern Matching
```csharp
// Switch expression
public string GetOperationSymbol(Operation op) => op switch
{
    Operation.Add => "+",
    Operation.Subtract => "-",
    Operation.Multiply => "*",
    Operation.Divide => "/",
    Operation.Power => "^",
    _ => throw new ArgumentOutOfRangeException(nameof(op))
};

// Property pattern
if (result is { Success: true, Value: var v } && v > 100)
{
    Console.WriteLine("Large result");
}
```

### LINQ
```csharp
// Query syntax
var results = from expr in expressions
              where expr.Length > 0
              select Calculate(expr);

// Method syntax
var results = expressions
    .Where(e => e.Length > 0)
    .Select(Calculate)
    .Where(r => r.Success)
    .OrderBy(r => r.Value)
    .ToList();

// Aggregation
double sum = results.Sum(r => r.Value);
double avg = results.Average(r => r.Value);
```

### async/await
```csharp
// Async method
public async Task<CalculationResult> CalculateAsync(
    string expression,
    CancellationToken cancellationToken = default)
{
    return await Task.Run(() =>
    {
        cancellationToken.ThrowIfCancellationRequested();
        return Calculate(expression);
    }, cancellationToken);
}

// HTTP call
public async Task<double> FetchExchangeRateAsync(string currency)
{
    using var client = new HttpClient();
    var response = await client.GetStringAsync(
        $"https://api.example.com/rates/{currency}");
    return JsonConvert.DeserializeObject<double>(response);
}
```

### Dependency Injection
```csharp
// Service interface
public interface ICalculator
{
    CalculationResult Calculate(string expression);
}

// Implementation
public class MathCalculator : ICalculator
{
    private readonly ExpressionParser _parser;

    public MathCalculator(ExpressionParser parser)
    {
        _parser = parser;
    }

    public CalculationResult Calculate(string expression)
    {
        var parsed = _parser.Parse(expression);
        var value = Evaluate(parsed);
        return new CalculationResult(value, expression, true);
    }
}

// Registration (Program.cs)
builder.Services.AddScoped<ICalculator, MathCalculator>();
```

### Nullable Reference Types
```csharp
#nullable enable

public class Calculator
{
    // Warning if not initialized
    private readonly ExpressionParser _parser;

    public Calculator(ExpressionParser parser)
    {
        _parser = parser;
    }

    // Nullable parameter
    public CalculationResult? FindResult(string? expression)
    {
        if (string.IsNullOrEmpty(expression))
            return null;

        return Calculate(expression);
    }
}
```

## Error Handling

```csharp
// Custom exceptions
public class CalculatorException : Exception
{
    public string Expression { get; }

    public CalculatorException(string message, string expression)
        : base(message)
    {
        Expression = expression;
    }
}

public class DivisionByZeroException : CalculatorException
{
    public DivisionByZeroException(string expression)
        : base("Division by zero", expression)
    {
    }
}

// Usage
public double Divide(double a, double b)
{
    if (b == 0)
        throw new DivisionByZeroException($"{a} / {b}");
    return a / b;
}

// Try-catch
try
{
    var result = calculator.Calculate(expression);
}
catch (DivisionByZeroException ex)
{
    logger.LogError(ex, "Division by zero in: {Expression}", ex.Expression);
    return CalculationResult.Failure(ex.Expression, ex.Message);
}
```

## Testing (xUnit)

```csharp
using Xunit;

public class CalculatorTests
{
    private readonly ICalculator _calculator;

    public CalculatorTests()
    {
        _calculator = new MathCalculator(new ExpressionParser());
    }

    [Fact]
    public void Add_TwoNumbers_ReturnsSum()
    {
        var result = _calculator.Calculate("2 + 3");
        Assert.True(result.Success);
        Assert.Equal(5.0, result.Value, precision: 10);
    }

    [Theory]
    [InlineData("2 + 3", 5.0)]
    [InlineData("10 / 2", 5.0)]
    [InlineData("3 * 4", 12.0)]
    public void Calculate_Expressions(string expr, double expected)
    {
        var result = _calculator.Calculate(expr);
        Assert.Equal(expected, result.Value, precision: 10);
    }

    [Fact]
    public void Divide_ByZero_ReturnsError()
    {
        var result = _calculator.Calculate("10 / 0");
        Assert.False(result.Success);
        Assert.Contains("Division by zero", result.Error);
    }
}
```

## ASP.NET Minimal API

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<ICalculator, MathCalculator>();

var app = builder.Build();

app.MapPost("/api/calculate", (CalculationRequest req, ICalculator calc) =>
{
    var result = calc.Calculate(req.Expression);
    return Results.Ok(result);
});

app.MapGet("/api/health", () => Results.Ok(new { Status = "Healthy" }));

app.Run();
```

## Debugging

```bash
# Run with debugger
dotnet run --project src/Calculator

# VS Code launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Calculator",
            "type": "coreclr",
            "request": "launch",
            "program": "${workspaceFolder}/src/Calculator/bin/Debug/net8.0/Calculator.dll"
        }
    ]
}

# Logging
dotnet run --verbosity detailed

# Coverlet for code coverage
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura
```

## Rules

- Use `nullable` enable for null safety
- Prefer records for immutable data
- Use `ILogger` for logging, never `Console.WriteLine` in production
- Use dependency injection, not static methods
- Use `CancellationToken` for async operations
- Format with `dotnet format` before commits
- Treat warnings as errors in project file
