def run_models(args):
    action = args.action
    
    if action == "list":
        print("Installed models:")
        print(" - whisper: ggml-base.en.bin")
        print(" - vosk: vosk-model-small-en-us-0.15")
    elif action == "download":
        if not args.model:
            print("Error: Please specify a model name to download.")
            return
        print(f"Downloading model {args.model} for {args.engine}...")
        # Placeholder for download logic
        print("Download complete.")
    elif action == "remove":
        if not args.model:
            print("Error: Please specify a model name to remove.")
            return
        print(f"Removing model {args.model}...")
        # Placeholder for remove logic
        print("Model removed.")
