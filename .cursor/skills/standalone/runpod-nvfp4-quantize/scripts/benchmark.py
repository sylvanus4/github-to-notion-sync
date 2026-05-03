"""Inference benchmark: BF16 original vs NVFP4 quantized."""
import json, time, sys, os


def bench_vllm(model_path, label, quant=None, n_prompts=20, max_tokens=128):
    from vllm import LLM, SamplingParams
    print(f"\n=== Benchmark: {label} ===", flush=True)

    kwargs = dict(
        model=model_path, dtype="auto", max_model_len=2048,
        enforce_eager=True, gpu_memory_utilization=0.90,
        trust_remote_code=True,
    )
    if quant:
        kwargs["quantization"] = quant

    t0 = time.time()
    llm = LLM(**kwargs)
    load_time = time.time() - t0

    import torch
    mem_alloc = torch.cuda.memory_allocated() / 1e9
    mem_reserved = torch.cuda.memory_reserved() / 1e9

    prompts = [
        "Explain quantum computing in simple terms.",
        "서울에서 부산까지 여행 계획을 세워줘.",
        "Write a Python function to sort a list.",
        "What are the key differences between TCP and UDP?",
        "한국의 경제 성장 역사를 요약해줘.",
    ] * (n_prompts // 5 + 1)
    prompts = prompts[:n_prompts]

    sp = SamplingParams(max_tokens=max_tokens, temperature=0.7)
    t1 = time.time()
    outputs = llm.generate(prompts, sp)
    gen_time = time.time() - t1

    total_tokens = sum(len(o.outputs[0].token_ids) for o in outputs)
    throughput = total_tokens / gen_time if gen_time > 0 else 0

    result = {
        "label": label,
        "load_time_sec": round(load_time, 1),
        "gpu_mem_alloc_gb": round(mem_alloc, 2),
        "gpu_mem_reserved_gb": round(mem_reserved, 2),
        "n_prompts": n_prompts,
        "total_output_tokens": total_tokens,
        "generation_time_sec": round(gen_time, 2),
        "throughput_tok_per_sec": round(throughput, 1),
        "sample_output": outputs[0].outputs[0].text[:200] if outputs else "",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False), flush=True)

    del llm
    torch.cuda.empty_cache()
    time.sleep(5)
    return result


results = {}

# 1) NVFP4 benchmark
results["nvfp4"] = bench_vllm(
    "/workspace/output/nvfp4-full", "NVFP4-W4A4",
    quant="modelopt_fp4"
)

# 2) BF16 original (30B MoE needs ~60GB, B200 has 192GB — should fit)
try:
    results["bf16"] = bench_vllm(
        os.environ.get("MODEL_ID", "Qwen/Qwen3-30B-A3B"), "BF16-Original"
    )
except Exception as e:
    print(f"BF16 benchmark failed (expected if OOM): {e}", flush=True)
    results["bf16"] = {"label": "BF16-Original", "error": str(e)}

# Summary
print("\n=== BENCHMARK SUMMARY ===", flush=True)
print(json.dumps(results, indent=2, ensure_ascii=False), flush=True)

out_path = "/workspace/output/benchmark_results.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"Saved to {out_path}")
