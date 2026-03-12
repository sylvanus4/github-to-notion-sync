# Cost Estimation

**Formula:**
```
Total Cost = (Hours of runtime) × (Cost per hour)
```

## Example Calculations

**Quick test:**
- Hardware: cpu-basic ($0.10/hour)
- Time: 15 minutes (0.25 hours)
- Cost: $0.03

**Data processing:**
- Hardware: l4x1 ($2.50/hour)
- Time: 2 hours
- Cost: $5.00

**Batch inference:**
- Hardware: a10g-large ($5/hour)
- Time: 4 hours
- Cost: $20.00

## Cost Optimization Tips

1. **Start small** - Test on cpu-basic or t4-small
2. **Monitor runtime** - Set appropriate timeouts
3. **Use checkpoints** - Resume if job fails
4. **Optimize code** - Reduce unnecessary compute
5. **Choose right hardware** - Don't over-provision

See [references/hardware_guide.md](hardware_guide.md) for hardware costs and selection.
