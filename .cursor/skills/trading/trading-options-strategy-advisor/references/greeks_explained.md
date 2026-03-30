# Greeks Deep Dive

Option price sensitivity metrics. For position Greeks, sum across all legs (long positive, short negative).

## Greeks Interpretation Table

| Greek | Meaning | Example |
|-------|---------|---------|
| **Delta** | Directional exposure | Δ = 0.50 → $50 profit if stock +$1 |
| **Gamma** | Delta acceleration | Γ = 0.05 → Delta increases by 0.05 if stock +$1 |
| **Theta** | Daily time decay | Θ = -$5 → Lose $5/day from time passing |
| **Vega** | Volatility sensitivity | ν = $10 → Gain $10 if IV increases 1% |
| **Rho** | Interest rate sensitivity | ρ = $2 → Gain $2 if rates increase 1% |

## Position Greeks Formula

```python
# For each leg: multiply by quantity (+ for long, - for short)
delta_position = sum(qty * delta for each leg)
gamma_position = sum(qty * gamma for each leg)
theta_position = sum(qty * theta for each leg)
vega_position = sum(qty * vega for each leg)
```

Example (Bull Call Spread: long 1x $180 call, short 1x $185 call):
```python
delta_position = (1 * delta_long) + (-1 * delta_short)
```

## Greeks Formulas (Black-Scholes)

### Delta (Δ)
```python
def delta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.cdf(d1)

def delta_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * (norm.cdf(d1) - 1)
```

### Gamma (Γ)
```python
def gamma(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
```

### Theta (Θ) — per day
```python
def theta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    theta = (-S*norm.pdf(d1)*sigma*np.exp(-q*T)/(2*np.sqrt(T))
             - r*K*np.exp(-r*T)*norm.cdf(d2)
             + q*S*norm.cdf(d1)*np.exp(-q*T))
    return theta / 365
```

### Vega (ν) — per 1% IV change
```python
def vega(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S * np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T) / 100
```

### Rho (ρ) — per 1% rate change
```python
def rho_call(S, K, T, r, sigma, q=0):
    d2 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T)) - sigma*np.sqrt(T)
    return K * T * np.exp(-r*T) * norm.cdf(d2) / 100
```

## Portfolio Greeks Guidelines

- **Delta:** -10 to +10 for neutral portfolio
- **Theta:** Positive preferred (seller advantage)
- **Vega:** Monitor if >$500 (IV risk); reduce short premium if VIX rising
