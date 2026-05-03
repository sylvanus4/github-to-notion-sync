"""
vLLM loading sanity check for the smoke NVFP4 artifact.

Loads the partial-quantized model and generates 1 token. Smoke test only —
the model is not expected to produce coherent output (only 2 layers quantized).
"""
import argparse
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="/workspace/output/nvfp4")
    parser.add_argument("--quant", default="modelopt_fp4")
    parser.add_argument("--prompt", default="Hello")
    parser.add_argument("--max-tokens", type=int, default=4)
    args = parser.parse_args()

    t0 = time.time()
    print(f"[{time.time()-t0:.1f}s] importing vllm...", flush=True)
    from vllm import LLM, SamplingParams

    print(f"[{time.time()-t0:.1f}s] LLM(model={args.model!r}, quantization={args.quant!r})", flush=True)
    try:
        llm = LLM(
            model=args.model,
            quantization=args.quant,
            dtype="auto",
            max_model_len=512,
            enforce_eager=True,
            gpu_memory_utilization=0.85,
            trust_remote_code=True,
        )
    except Exception as e:
        print(f"[FAIL] vLLM constructor: {e!r}", flush=True)
        sys.exit(1)

    print(f"[{time.time()-t0:.1f}s] generating...", flush=True)
    sp = SamplingParams(max_tokens=args.max_tokens, temperature=0.0)
    out = llm.generate([args.prompt], sp)
    txt = out[0].outputs[0].text if out and out[0].outputs else ""
    print(f"  generated text: {txt!r}", flush=True)
    print(f"DONE in {time.time()-t0:.1f}s. (any non-empty output = PASS)")


if __name__ == "__main__":
    main()
