# Embedded-Kalman-Filter

Deterministic scalar discrete Kalman filter implementation in C99 designed for resource-constrained microcontrollers.

## Design Constraints
* Zero dynamic memory allocation (`malloc` free).
* Constant time execution: $\mathcal{O}(1)$ runtime complexity.
* Static state footprint: 20 bytes on 32-bit architectures.

## Mathematical Formulation

### 1. State Prediction
$$\hat{x}_{k\vert{}k-1} = \hat{x}_{k-1\vert{}k-1}$$
$$P_{k\vert{}k-1} = P_{k-1\vert{}k-1} + Q$$

### 2. Measurement Update
$$K_k = \frac{P_{k\vert{}k-1}}{P_{k\vert{}k-1} + R}$$
$$\hat{x}_{k\vert{}k} = \hat{x}_{k\vert{}k-1} + K_k (z_k - \hat{x}_{k\vert{}k-1})$$
$$P_{k\vert{}k} = (1 - K_k) P_{k\vert{}k-1}$$

## Build & Run
```bash
cmake -B build
cmake --build build
./build/bench_kalman
```
